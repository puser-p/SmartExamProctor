from ultralytics import YOLO
import cv2


class PhoneDetector:

    def __init__(self):

        # Downloads yolov8n.pt automatically on first run
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):

        results = self.model.predict(
            frame,
            verbose=False,
            conf=0.45
        )

        phone_found = False

        for result in results:

            boxes = result.boxes

            for box in boxes:

                cls = int(box.cls[0])

                label = self.model.names[cls]

                if label == "cell phone":

                    phone_found = True

                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0]
                    )

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),
                        2
                    )

                    cv2.putText(
                        frame,
                        "PHONE",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

        return frame, phone_found