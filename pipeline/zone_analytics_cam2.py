from ultralytics import YOLO
import supervision as sv
import cv2
from database_storage import insert_visitor
# Load YOLO
model = YOLO("yolov8n.pt")

# Camera 2
video_path = r"C:\Users\Admin\Downloads\CAM 2.mp4"

cap = cv2.VideoCapture(video_path)


fps = cap.get(cv2.CAP_PROP_FPS)

tracker = sv.ByteTrack()

# SKINCARE ROI
ZONE_NAME = "MAKEUP"

ROI_X1 = 180
ROI_Y1 = 140

ROI_X2 = 1910
ROI_Y2 = 1080

visitor_start_frame = {}
visitor_last_frame = {}

zone_visitors = {
    ZONE_NAME: set()
}

zone_dwell_times = {
    ZONE_NAME: []
}

frame_number = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    results = model(frame)[0]

    detections = sv.Detections.from_ultralytics(results)

    # Person only
    detections = detections[detections.class_id == 0]

    detections = tracker.update_with_detections(detections)

    # Draw ROI
    cv2.rectangle(
        frame,
        (ROI_X1, ROI_Y1),
        (ROI_X2, ROI_Y2),
        (255, 0, 0),
        3
    )

    if detections.tracker_id is not None:

        for bbox, track_id in zip(
            detections.xyxy,
            detections.tracker_id
        ):

            x1, y1, x2, y2 = map(int, bbox)

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            inside_zone = (
                ROI_X1 <= center_x <= ROI_X2
                and
                ROI_Y1 <= center_y <= ROI_Y2
            )

            if inside_zone:

                zone_visitors[ZONE_NAME].add(track_id)

                if track_id not in visitor_start_frame:
                    visitor_start_frame[track_id] = frame_number

                visitor_last_frame[track_id] = frame_number

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID {track_id}",
                    (x1, y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

    cv2.imshow(
        "Store Insights",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# ==========================
# DWELL CALCULATION
# ==========================

for track_id in visitor_start_frame:

    dwell_seconds = (
        visitor_last_frame[track_id]
        -
        visitor_start_frame[track_id]
    ) / fps

    # Ignore very short visits
    if dwell_seconds >= 5:

        zone_dwell_times[ZONE_NAME].append(
            dwell_seconds
        )

print("\n===== STORE INSIGHTS =====\n")

# ==========================
# TOTAL VISITORS
# ==========================

qualified_visitors = set()

for track_id in visitor_start_frame:

    dwell_seconds = (
        visitor_last_frame[track_id]
        -
        visitor_start_frame[track_id]
    ) / fps

    if dwell_seconds >= 5:
        qualified_visitors.add(track_id)

total_visitors = len(qualified_visitors)

# Save qualified visitors to database

for track_id in qualified_visitors:

    dwell_seconds = (
        visitor_last_frame[track_id]
        -
        visitor_start_frame[track_id]
    ) / fps

    insert_visitor(
        int(track_id),
        ZONE_NAME,
        round(dwell_seconds, 2),
        "CAM2"
    )
print("Analytics saved successfully.")

print(
    f"Total Visitors: {total_visitors}"
)

print()

# ==========================
# ZONE REPORT
# ==========================

for zone in zone_visitors:

    qualified_zone_visitors = set()

    for track_id in zone_visitors[zone]:

        if track_id in visitor_start_frame:

            dwell_seconds = (
                visitor_last_frame[track_id]
                -
                visitor_start_frame[track_id]
            ) / fps

            if dwell_seconds >= 5:
                qualified_zone_visitors.add(track_id)

    visitors = len(
        qualified_zone_visitors
    )

    dwell_list = zone_dwell_times[zone]

    if len(dwell_list) > 0:

        avg_dwell = (
            sum(dwell_list)
            /
            len(dwell_list)
        )

    else:

        avg_dwell = 0

    print(
        f"{zone}"
    )

    print(
        f"Visitors: {visitors}"
    )

    print(
        f"Average Dwell: "
        f"{avg_dwell:.2f} sec"
    )

    print()

# ==========================
# BEST ZONES
# ==========================

most_visited_zone = max(
    zone_visitors,
    key=lambda z:
    len(zone_visitors[z])
)

highest_dwell_zone = max(
    zone_dwell_times,
    key=lambda z:
    (
        sum(zone_dwell_times[z])
        /
        len(zone_dwell_times[z])
    )
    if len(zone_dwell_times[z]) > 0
    else 0
)

print(
    f"Most Visited Zone: "
    f"{most_visited_zone}"
)

print(
    f"Highest Dwell Zone: "
    f"{highest_dwell_zone}"
)