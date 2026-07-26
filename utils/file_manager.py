import os

def create_student_folder(roll):
    folder = os.path.join("dataset", str(roll))
    os.makedirs(folder, exist_ok=True)
    return folder