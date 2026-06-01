from ultralytics import YOLO
import supervision as sv
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

# Camera 3 video
video_path = r"C:\Users\Admin\Downloads\CAM 3.mp4"

cap = cv2.VideoCapture(video_path)

# Video FPS
fps = cap.get(cv2.CAP_PROP_FPS)

# ByteTrack
tracker = sv.ByteTrack()

# Tracking dictionaries
visitor_start_frame = {}
visitor_last_frame = {}

frame_number = 0

while True:
    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    # YOLO detection
    results = model(frame)[0]

    # Convert to supervision detections
    detections = sv.Detections.from_ultralytics(results)

    # Keep only persons
    detections = detections[detections.class_id == 0]

    # Track persons
    detections = tracker.update_with_detections(detections)

    # Process tracked visitors
    if detections.tracker_id is not None:

        for bbox, track_id in zip(
            detections.xyxy,
            detections.tracker_id
        ):

            # First appearance
            if track_id not in visitor_start_frame:
                visitor_start_frame[track_id] = frame_number

            # Update last appearance
            visitor_last_frame[track_id] = frame_number

            x1, y1, x2, y2 = map(int, bbox)

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

    cv2.imshow("Visitor Dwell Time Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("\n===== VISITOR DWELL TIMES =====\n")

for track_id in visitor_start_frame:

    start_frame = visitor_start_frame[track_id]
    end_frame = visitor_last_frame[track_id]

    dwell_frames = end_frame - start_frame
    dwell_seconds = dwell_frames / fps

    print(
        f"Visitor {track_id} stayed "
        f"{dwell_seconds:.2f} seconds"
    )