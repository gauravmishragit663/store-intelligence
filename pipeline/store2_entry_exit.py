from ultralytics import YOLO
import supervision as sv
import cv2

from database_storage import insert_visitor

# =========================
# CONFIG
# =========================

VIDEO_PATH = r"C:\Users\Admin\Downloads\entry 1.mp4"

ROI_X1 = 320
ROI_Y1 = 120

ROI_X2 = 980
ROI_Y2 = 620

LINE_Y = 430

# =========================
# MODEL
# =========================

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO_PATH)

tracker = sv.ByteTrack()

entered_ids = set()
exited_ids = set()

track_history = {}

# =========================
# PROCESS VIDEO
# =========================

while True:

    success, frame = cap.read()

    if not success:
        break

    cv2.rectangle(
        frame,
        (ROI_X1, ROI_Y1),
        (ROI_X2, ROI_Y2),
        (255, 0, 0),
        3
    )

    cv2.line(
        frame,
        (ROI_X1, LINE_Y),
        (ROI_X2, LINE_Y),
        (0, 0, 255),
        3
    )

    results = model(frame)[0]

    detections = sv.Detections.from_ultralytics(
        results
    )

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

            if not (
                ROI_X1 <= center_x <= ROI_X2
                and
                ROI_Y1 <= center_y <= ROI_Y2
            ):
                continue

            if track_id not in track_history:
                track_history[track_id] = []

            track_history[track_id].append(
                center_y
            )

            if len(
                track_history[track_id]
            ) < 2:
                continue

            prev_y = track_history[
                track_id
            ][-2]

            curr_y = track_history[
                track_id
            ][-1]

            # =====================
            # ENTRY
            # =====================

            if (
                prev_y < LINE_Y
                and
                curr_y >= LINE_Y
                and
                track_id not in entered_ids
            ):

                entered_ids.add(track_id)

                print(
                    f"Visitor {track_id} ENTERED"
                )

                insert_visitor(
                    int(track_id),
                    "ENTRY",
                    0,
                    "STORE2_ENTRY"
                )

            # =====================
            # EXIT
            # =====================

            if (
                prev_y > LINE_Y
                and
                curr_y <= LINE_Y
                and
                track_id not in exited_ids
            ):

                exited_ids.add(track_id)

                print(
                    f"Visitor {track_id} EXITED"
                )

                insert_visitor(
                    int(track_id),
                    "EXIT",
                    0,
                    "STORE2_ENTRY"
                )

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
        "Store 2 Entry Exit Analytics",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()

# =========================
# RESULTS
# =========================

print()
print("===== STORE 2 ENTRY EXIT =====")
print()

print(
    f"Total Entries : "
    f"{len(entered_ids)}"
)

print(
    f"Total Exits   : "
    f"{len(exited_ids)}"
)

print()
print(
    "Entry Exit Analytics Saved Successfully."
)