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
    def __init__(self, state, q_messe: queue.Queue) -> None:
        self.state: OkatronState = state
        self._message_lock = asyncio.Lock()
        self.q_messe = q_messe

    def run(self) -> None:
        """メインループ"""
        if self.state.mode == Mode.AUTO:
            img = self.autoMode()
        elif self.state.mode == Mode.MANUAL:
            img = self.manualMode()
        elif self.state.mode == Mode.PROGRAM:
            img = self.programMode()

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
            messe = {}
            messe["key"] = det
            res = self.motorcontrollerWork(messe)

        return img

    def manualMode(self):
        """マニュアルモードの動作"""
        # 画像取得
        img = self.captorWork()
        try:
            messe = self.q_messe.get(False)
            res = self.motorcontrollerWork(messe)
        except:
            pass
        return img

    def programMode(self):
        """プログラムモードの動作"""
        if self.state.status == Status.IDLE:
            # 画像取得
            img = self.captorWork()

        return img

    def updateState(self) -> None:
        """アプリの状態を更新する"""
        now_status = self.state.status

        # if msg == UserReq.START.value:
        #     self.state.status = Status.WORKING

        if now_status == Status.IDLE:
            pass
        elif now_status == Status.WORKING:
            pass

        if now_status != self.state.status:
            print("State Change:\t[ {} -> {} ]".format(now_status.name, self.state.status.name))

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

    def motorcontrollerWork(self, messe: dict) -> bool:
        """モータを制御する"""
        if messe["key"] == None:
            return False

        if self.state.mode == Mode.AUTO:
            det = messe["key"]
            # print("server get:{}".format(det))
        elif self.state.mode == Mode.MANUAL:
            det = messe["key"]
            print("server get:{}".format(det))
        elif self.state.mode == Mode.PROGRAM:
            det = messe["key"]
            print("server get:{}".format(det))
        return True