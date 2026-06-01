from ultralytics import YOLO
import supervision as sv
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

# Camera 3 video
video_path = r"C:\Users\Admin\Downloads\CAM 3.mp4"

cap = cv2.VideoCapture(video_path)

# Initialize ByteTrack
tracker = sv.ByteTrack()

while True:
    success, frame = cap.read()

    if not success:
        break

    # YOLO detection
    results = model(frame)[0]

    # Convert to Supervision detections
    detections = sv.Detections.from_ultralytics(results)

    # Keep only PERSON class (class 0)
    detections = detections[detections.class_id == 0]

    # Track people
    detections = tracker.update_with_detections(detections)
    print("Tracker IDs:", detections.tracker_id)
    print("Boxes:", len(detections.xyxy))

    

    # Draw boxes + IDs
    for bbox, track_id in zip(
        detections.xyxy,
        detections.tracker_id
    ):
        print("Drawing ID:", track_id)
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

    cv2.imshow("ByteTrack Visitor Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()