import cv2
import os

from detection.camera import Camera
from detection.face_detector import FaceDetector


class DatasetCreator:

    def __init__(self):

        self.camera = Camera()

        self.detector = FaceDetector()

    def capture(self, roll):

        folder = os.path.join("dataset", str(roll))

        os.makedirs(folder, exist_ok=True)

        count = 0

        while True:

            frame = self.camera.read()

            if frame is None:
                break

            faces = self.detector.detect(frame)

            if faces is not None:

                for face in faces:

                    x = int(face[0])
                    y = int(face[1])
                    w = int(face[2])
                    h = int(face[3])

                    # Small padding
                    pad = 20

                    x = max(0, x - pad)
                    y = max(0, y - pad)

                    w = w + pad * 2
                    h = h + pad * 2

                    crop = frame[y:y+h, x:x+w]

                    if crop.size == 0:
                        continue

                    crop = cv2.resize(crop, (200, 200))

                    count += 1

                    filename = os.path.join(
                        folder,
                        f"{count:03d}.jpg"
                    )

                    cv2.imwrite(filename, crop)

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x+w, y+h),
                        (0,255,0),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"{count}/100",
                        (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,0),
                        2
                    )

            cv2.imshow("Dataset Creator", frame)

            key = cv2.waitKey(1)

            if key == 27:
                break

            if count >= 100:
                break

        self.camera.release()

        return count