import os

# =========================
# Project Paths
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "database", "exam.db")

DATASET_PATH = os.path.join(BASE_DIR, "dataset")

MODEL_PATH = os.path.join(
    BASE_DIR,
    "trained_model",
    "face_trainer.yml"
)

FACE_MODEL = os.path.join(
    BASE_DIR,
    "assets",
    "models",
    "face_detection_yunet_2023mar.onnx"
)

REPORT_PATH = os.path.join(BASE_DIR, "reports")

LOG_PATH = os.path.join(BASE_DIR, "logs")

# =========================
# Camera
# =========================

CAMERA_ID = 0

# =========================
# Face Recognition
# =========================

FACE_SIZE = (200, 200)

CONFIDENCE_THRESHOLD = 70

# =========================
# Exam
# =========================

DEFAULT_EXAM_DURATION = 60 * 60

# =========================
# AI
# =========================

PHONE_CONFIDENCE = 0.50

PERSON_CONFIDENCE = 0.50