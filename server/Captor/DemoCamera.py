"""demo"""

import os
import sys

import cv2
import time

import numpy as np

class DemoCamera():
    """demo"""
    def __init__(self, info: dict) -> None:
        self.cap = cv2.VideoCapture("../resource/demo/demo.mp4")
        self.width = info["width"]
        self.height = info["height"]

        # フォーマット・解像度・FPSの取得
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        self.null_img = np.zeros((info["height"], info["width"], 3),
                                  dtype="uint8") # 初期画像

    def capture(self):
        """画像取得処理"""
        ret, frame = self.cap.read()

        if ret == True:
            frame = cv2.resize(frame, (self.width, self.height))
            img = frame
        elif ret == False:
            self.cap = cv2.VideoCapture("../resource/demo/demo.mp4")
            ret, frame = self.cap.read()
            frame = cv2.resize(frame, (self.width, self.height))
            img = frame

        time.sleep(1/self.fps)
        return img

    def decode_fourcc(self, v):
        """拡張子取得処理"""
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])