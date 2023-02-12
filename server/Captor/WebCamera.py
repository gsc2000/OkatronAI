# 画像関係

import os
import sys

import cv2

import numpy as np

class WebCamera():
    def __init__(self, config: dict) -> None:
        self.cap = cv2.VideoCapture(config["id"])
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        # self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["width"])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["height"])
        self.cap.set(cv2.CAP_PROP_FPS, config["fps"])

        # フォーマット・解像度・FPSの取得
        fourcc = self.decode_fourcc(self.cap.get(cv2.CAP_PROP_FOURCC))
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)

        # self.resize_size = (config["width"], config["height"])

        self.null_img = np.zeros((config["height"], config["width"], 3),
                                  dtype="uint8") # 初期画像

    def capture(self):
        ret, frame = self.cap.read()

        if ret == True:
            img = frame
        elif ret == False:
            img = self.null_img

        return img

    def decode_fourcc(self, v):
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])
