import cv2

from detection.camera import Camera
from detection.face_detector import FaceDetector


camera = Camera()

detector = FaceDetector()

while True:

    frame = camera.read()

    if frame is None:
        break

    faces = detector.detect(frame)

    if faces is not None:

        for face in faces:

            x = int(face[0])
            y = int(face[1])
            w = int(face[2])
            h = int(face[3])

            confidence = face[-1]

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"{confidence:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    cv2.imshow("Face Detector", frame)

    key = cv2.waitKey(1)

    if key == 27:
        break

camera.release()