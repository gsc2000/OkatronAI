"""Face"""
import os
import sys

import cv2
import numpy as np

class FaceDetector():
    def __init__(self) -> None:
        path = "../resource/model/haarcascades/haarcascade_frontalface_default.xml"
        self.model = cv2.CascadeClassifier(path)

    def detect(self, img: np.ndarray):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.model.detectMultiScale(img_gray)

        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return img