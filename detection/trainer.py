import os
import cv2
import numpy as np


class FaceTrainer:

    def __init__(self):

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def train(self):

        faces = []

        ids = []

        dataset_path = "dataset"

        for student in os.listdir(dataset_path):

            folder = os.path.join(dataset_path, student)

            if not os.path.isdir(folder):
                continue

            student_id = int(student)
           

            for image in os.listdir(folder):

                path = os.path.join(folder, image)
                print("Training:", student_id, path)

                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

                if img is None:
                    continue

                faces.append(img)

                ids.append(student_id)

        ids = np.array(ids)

        os.makedirs("trained_model", exist_ok=True)

        self.recognizer.train(faces, ids)

        self.recognizer.save(
            "trained_model/face_trainer.yml"
        )

        print("Training Completed Successfully!")

        print("Total Images :", len(faces))

        print("Total Students :", len(set(ids)))