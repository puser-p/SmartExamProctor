import cv2

from detection.camera import Camera
from detection.recognizer import FaceRecognizer


camera = Camera()
recognizer = FaceRecognizer()

while True:

    frame = camera.read()

    if frame is None:
        break

    frame, recognized_roll, faces = recognizer.recognize(frame)

    cv2.imshow("Face Recognition Test", frame)

    if recognized_roll is not None:
        print("Recognized Roll:", recognized_roll)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()