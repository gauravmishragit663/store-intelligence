from ultralytics import YOLO
import supervision as sv
import cv2

# =========================
# STORE ROI
# =========================
ROI_X1 = 180
ROI_Y1 = 120

ROI_X2 = 1500
ROI_Y2 = 950

# =========================
# LOAD MODEL
# =========================
model = YOLO("yolov8n.pt")

video_path = r"C:\Users\Admin\Downloads\CAM 3.mp4"

cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)

# =========================
# BYTETRACK
# =========================
tracker = sv.ByteTrack()

visitor_start_frame = {}
visitor_last_frame = {}

frame_number = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    # Draw ROI
    cv2.rectangle(
        frame,
        (ROI_X1, ROI_Y1),
        (ROI_X2, ROI_Y2),
        (255, 0, 0),
        3
    )

    # YOLO
    results = model(frame)[0]

    detections = sv.Detections.from_ultralytics(results)

    detections = detections[detections.class_id == 0]

    detections = tracker.update_with_detections(
        detections
    )

    if detections.tracker_id is not None:

        for bbox, track_id in zip(
            detections.xyxy,
            detections.tracker_id
        ):

            x1, y1, x2, y2 = map(int, bbox)

            # Center point
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # Ignore outside ROI
            if not (
                ROI_X1 <= center_x <= ROI_X2
                and
                ROI_Y1 <= center_y <= ROI_Y2
            ):
                continue

            # First appearance
            if track_id not in visitor_start_frame:
                visitor_start_frame[track_id] = frame_number

            # Last appearance
            visitor_last_frame[track_id] = frame_number

            # Draw visitor
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
        "Visitor Dwell Time Tracking V2",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("\n===== VISITOR DWELL TIMES =====\n")

MIN_DWELL_SECONDS = 3

for track_id in visitor_start_frame:

    start_frame = visitor_start_frame[track_id]
    end_frame = visitor_last_frame[track_id]

    dwell_frames = end_frame - start_frame

    dwell_seconds = dwell_frames / fps

    if dwell_seconds < MIN_DWELL_SECONDS:
        continue

    print(
        f"Visitor {track_id} stayed "
        f"{dwell_seconds:.2f} seconds"
    )