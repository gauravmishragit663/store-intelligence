from ultralytics import YOLO
import supervision as sv
import cv2

from database_storage import insert_visitor

# =========================
# CONFIG
# =========================

VIDEO_PATH = r"C:\Users\Admin\Downloads\billing_area.mp4"

ZONE_NAME = "BILLING_QUEUE"

# Increased to reduce ID fragmentation noise
MIN_QUEUE_SECONDS = 15

# Full billing area ROI
ROI_X1 = 250
ROI_Y1 = 120

ROI_X2 = 1150
ROI_Y2 = 900

# =========================
# LOAD MODEL
# =========================

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO_PATH)

fps = cap.get(cv2.CAP_PROP_FPS)

tracker = sv.ByteTrack()

visitor_start_frame = {}
visitor_last_frame = {}

frame_number = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    cv2.rectangle(
        frame,
        (ROI_X1, ROI_Y1),
        (ROI_X2, ROI_Y2),
        (255, 0, 0),
        3
    )

    results = model(frame)[0]

    detections = sv.Detections.from_ultralytics(results)

    detections = detections[
        detections.class_id == 0
    ]

    detections = tracker.update_with_detections(
        detections
    )

    if detections.tracker_id is not None:

        for bbox, track_id in zip(
            detections.xyxy,
            detections.tracker_id
        ):

            x1, y1, x2, y2 = map(
                int,
                bbox
            )

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            inside_roi = (
                ROI_X1 <= center_x <= ROI_X2
                and
                ROI_Y1 <= center_y <= ROI_Y2
            )

            if not inside_roi:
                continue

            if track_id not in visitor_start_frame:

                visitor_start_frame[
                    track_id
                ] = frame_number

            visitor_last_frame[
                track_id
            ] = frame_number

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
        "Billing Queue Analytics",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("\n===== BILLING ANALYTICS =====\n")

qualified_visitors = 0

for track_id in visitor_start_frame:

    start_frame = visitor_start_frame[
        track_id
    ]

    end_frame = visitor_last_frame[
        track_id
    ]

    queue_seconds = (
        end_frame - start_frame
    ) / fps

    # Ignore fragmented tracks
    if queue_seconds < MIN_QUEUE_SECONDS:
        continue

    qualified_visitors += 1

    print(
        f"Visitor {track_id}"
        f" | Queue Time:"
        f" {queue_seconds:.2f} sec"
    )

    insert_visitor(
        int(track_id),
        ZONE_NAME,
        round(queue_seconds, 2),
        "STORE2_BILLING"
    )

print()

print(
    f"Total Billing Visitors: "
    f"{qualified_visitors}"
)

print(
    "Billing Analytics Saved Successfully."
)