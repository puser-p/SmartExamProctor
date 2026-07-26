import os
import cv2
import numpy as np

DATASET_PATH = "dataset"
MODEL_PATH = "models/face_model.yml"

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
ids = []

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

for student_id in os.listdir(DATASET_PATH):

    student_folder = os.path.join(DATASET_PATH, student_id)

    if not os.path.isdir(student_folder):
        continue

    for image_name in os.listdir(student_folder):

        image_path = os.path.join(student_folder, image_name)

        image = cv2.imread(image_path)

        if image is None:
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detected = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5
        )

        for (x, y, w, h) in detected:

            faces.append(gray[y:y+h, x:x+w])
            ids.append(int(student_id))

recognizer.train(faces, np.array(ids))
recognizer.save(MODEL_PATH)

print("Model trained successfully!")