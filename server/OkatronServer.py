"""OkatronServer"""

import os
import sys

import time
import cv2
import numpy as np
import websockets
import asyncio
import json

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
    def __init__(self, state) -> None:
        self.state: OkatronState = state
        self._message_lock = asyncio.Lock()
        self.q_command = asyncio.Queue()

        # self.show_img = None

        # テスト
        # cv2.namedWindow("Test", cv2.WINDOW_NORMAL)

    def run(self) -> None:
        """メインループ"""
        if self.state.mode == Mode.AUTO:
            img = self.autoMode()
        elif self.state.mode == Mode.MANUAL:
            img = self.manualMode()
        elif self.state.mode == Mode.PROGRAM:
            img = self.programMode()

        return img

    # async def websocketioWork(self, sock) -> str:
    #     """WebSocketからのリクエストを処理する"""
    #     while True:
    #         try:
    #             msg = await sock.recv()
    #             msg = json.loads(msg)
    #             await self.dispatchMsg(sock, msg)
    #         except:
    #             pass

    # async def dispatchMsg(self, sock, msg):
    #     # print("Dispatch Message")
    #     for key in msg.keys():
    #         if key == "img":
    #             # print("Recv Img Req")
    #             await self.proc(sock)
    #         elif key == "user":
    #             await self.updateState()


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
            res = self.motorcontrollerWork(det)

        return img

    def manualMode(self):
        """マニュアルモードの動作"""
        pass

    def programMode(self):
        """プログラムモードの動作"""
        pass

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

    def motorcontrollerWork(self, det) -> bool:
        """モータを制御する"""
        return True