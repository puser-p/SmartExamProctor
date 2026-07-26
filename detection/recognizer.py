import cv2
import os

from detection.face_detector import FaceDetector
from database.db_manager import DatabaseManager


class FaceRecognizer:

    def __init__(self):

        self.detector = FaceDetector()

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.db = DatabaseManager()
 
        model_path = os.path.join(
            "trained_model",
            "face_trainer.yml"
        )

        print("Loading model from:", os.path.abspath(model_path))

        self.recognizer.read(model_path)
     

    def recognize(self, frame):

        recognized_roll = None
        recognized_name = None

        faces = self.detector.detect(frame)

        if faces is None:
            return frame, None, None, None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        for face in faces:

            x, y, w, h = map(int, face[:4])

            face_img = gray[y:y+h, x:x+w]

            if face_img.size == 0:
                continue

            face_img = cv2.resize(face_img, (200, 200))

            student_id, confidence = self.recognizer.predict(face_img)
            print("--------------------")
            print("Predicted:", student_id)
            print("Confidence:", confidence)

            student = self.db.get_student_by_roll(student_id)
            print("Database:", student)

            if confidence < 65:

                student = self.db.get_student_by_roll(student_id)

                if student:

                    name = student[1]
                    roll = student[2]
                    recognized_name = name

                    recognized_roll = str(roll)

                    color = (0, 255, 0)

                    cv2.putText(
                        frame,
                        f"Name: {name}",
                        (x, y - 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2
                    )

                    cv2.putText(
                        frame,
                        f"Roll: {roll}",
                        (x, y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2
                    )

                else:

                    cv2.putText(
                        frame,
                        "Unknown",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

            else:

                cv2.putText(
                    frame,
                    "Unknown",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

        return frame,recognized_name, recognized_roll, faces