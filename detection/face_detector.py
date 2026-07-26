import cv2
import os


class FaceDetector:

    def __init__(self):

        model = os.path.join(
            "models",
            "face_detection_yunet_2023mar.onnx"
        )

        self.detector = cv2.FaceDetectorYN.create(
            model,
            "",
            (320, 320),
            score_threshold=0.8,
            nms_threshold=0.3,
            top_k=5000
        )

    def detect(self, frame):

        h, w = frame.shape[:2]

        self.detector.setInputSize((w, h))

        _, faces = self.detector.detect(frame)

        return faces