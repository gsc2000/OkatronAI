"""OkatronServer"""

import os
import sys

import time
import cv2
import numpy as np
import websockets
import asyncio
import json
import queue

import DataBaseapi as db
from UserIO import UserIO, UserReq
from OkatronState import OkatronState, Mode, Status
# from Captor.WebCamera import WebCamera
from Captor.WebCamera import NullCamera as WebCamera
from Inferencer.YOLOv5Detector import YOLOv5Detector

class OkatronServer():
    """アプリ本体
    GUIから届くユーザリクエストの処理や
    内部状態に応じて行う処理を変更
    """
    def __init__(self, state, q_msg: queue.Queue) -> None:
        self.state: OkatronState = state
        self._message_lock = asyncio.Lock()
        # self.q_img = q_img
        self.q_msg = q_msg

    def run(self) -> None:
        """メインループ"""
        if self.state.mode == Mode.AUTO:
            img = self.autoMode()
        elif self.state.mode == Mode.MANUAL:
            img = self.manualMode()
        elif self.state.mode == Mode.PROGRAM:
            img = self.programMode()

        # self.q_img.put(img)
        # print("Put image")
        return img

    def autoMode(self):
        """自動追従モードの動作"""
        # print("Auto Mode")
        if self.state.status == Status.IDLE:
            # 画像取得
            img = self.captorWork()

        elif self.state.status == Status.WORKING:
            # AI処理
            img = self.captorWork()
            det, img = self.inferencerWork(img)
            msg = {}
            msg["key"] = det
            self.motorcontrollerWork(msg)

        return img

    def manualMode(self):
        """マニュアルモードの動作"""
        # 画像取得
        img = self.captorWork()
        try:
            msg = self.q_msg.get(False)
            self.motorcontrollerWork(msg)
        except:
            pass
        return img

    def programMode(self):
        """プログラムモードの動作"""
        if self.state.status == Status.IDLE:
            # 画像取得
            img = self.captorWork()

        return img

    # def updateState(self) -> None:
    #     """アプリの状態を更新する"""
    #     now_status = self.state.status

    #     if now_status == Status.IDLE:
    #         pass
    #     elif now_status == Status.WORKING:
    #         pass

    #     if now_status != self.state.status:
    #         print("State Change:\t[ {} -> {} ]".format(now_status.name, self.state.status.name))

    def captorWork(self) -> None:
        """画像を取得する"""
        img = self.state.captor.capture()
        # print(img.shape)
        return img

    def inferencerWork(self, img) -> np.ndarray:
        """AI処理する"""
        det = self.state.yolov5.detect(img)
        img = self.state.yolov5.showResult(img, det)
        return det, img

    def postProcDet(self, det: np.ndarray):
        msg = {"move": ["top", 10], "camera": ["top", 10]}
        return msg

    def motorcontrollerWork(self, msg: dict) -> bool:
        """
        モータを制御する
        Args:
            msg: 動作を指示するメッセージ
                 0: ON
                 数字: 動作する距離・角度
        """
        if msg["move"] == None and msg["camera"] == None:
            pass
        else:
            self.state.cont.run(msg)
