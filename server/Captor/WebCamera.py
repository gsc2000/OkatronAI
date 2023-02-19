"""WebCamera"""

import os
import sys

import cv2

import numpy as np

class NullCamera():
    """Win上での開発用"""
    def __init__(self, info:dict) -> None:
        self.test_img = cv2.imread("Captor/test.jpg")

    def capture(self):
        """画像取得処理"""
        return self.test_img

class WebCamera():
    """WebCamera"""
    def __init__(self, info: dict) -> None:
        self.cap = cv2.VideoCapture(info["id"])
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, info["width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, info["height"])
        self.cap.set(cv2.CAP_PROP_FPS, info["fps"])

        # フォーマット・解像度・FPSの取得
        fourcc = self.decode_fourcc(self.cap.get(cv2.CAP_PROP_FOURCC))
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)

        self.null_img = np.zeros((info["height"], info["width"], 3),
                                  dtype="uint8") # 初期画像

    def capture(self):
        """画像取得処理"""
        ret, frame = self.cap.read()

        if ret == True:
            img = frame
        elif ret == False:
            img = self.null_img

        return img

    def decode_fourcc(self, v):
        """拡張子取得処理"""
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])
