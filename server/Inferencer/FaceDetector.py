"""Face"""
import os
import sys

import cv2
import numpy as np

class FaceDetector():
    def __init__(self) -> None:
        path = "../resource/model/haarcascades/haarcascade_frontalface_default.xml"
        self.model = cv2.CascadeClassifier(path)

    def detect(self, img: np.ndarray, det: np.ndarray):
        if len(det) == 0:
            return img

        x1 = int(det[0][0])
        y1 = int(det[0][1])
        x2 = int(det[0][2])
        y2 = int(det[0][3])

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        trim_img = img_gray[y1:y2, x1:x2]
        faces = self.model.detectMultiScale(trim_img)

        center = (None, None)
        for x, y, w, h in faces:
            x = x+x1
            y = y+y1
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            center = (x+int(w/2), y+int(h/2))
            cv2.circle(img, center, 5, (255, 0, 0), thickness=-1, lineType=cv2.LINE_8, shift=0)
            break

        return img, center