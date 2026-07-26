import cv2
import os

from detection.camera import Camera
from detection.face_detector import FaceDetector


class FaceCapture:

    def __init__(self):
        self.camera = Camera()
        self.detector = FaceDetector()

    def capture(self, student_roll):

        folder = os.path.join("dataset", str(student_roll))
        os.makedirs(folder, exist_ok=True)

        count = 0

        while count < 100:

            frame = self.camera.read()

            if frame is None:
                break

            faces = self.detector.detect(frame)

            if faces is not None:

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                for face in faces:

                    x, y, w, h = map(int, face[:4])

                    face_img = gray[y:y+h, x:x+w]

                    if face_img.size == 0:
                        continue

                    face_img = cv2.resize(face_img, (200, 200))

                    count += 1

                    cv2.imwrite(
                        os.path.join(folder, f"{count}.jpg"),
                        face_img
                    )

                    cv2.rectangle(
                        frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )

            cv2.putText(
                frame,
                f"Images : {count}/100",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow("Face Capture", frame)

            if cv2.waitKey(1) == 27:
                break

        self.camera.release()
        cv2.destroyAllWindows()

        print(f"{count} images captured.")