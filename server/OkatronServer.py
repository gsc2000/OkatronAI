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

from OkatronState import OkatronState, Mode, Status

class OkatronServer():
    """アプリ本体
    GUIから届くユーザリクエストの処理や
    内部状態に応じて行う処理を変更
    """
    def __init__(self, state, q_recv_msg: queue.Queue, q_send_msg: queue.Queue) -> None:
        self.state: OkatronState = state
        self.q_recv_msg = q_recv_msg # FastAPI <-> OkatronServer
        self.q_send_msg = q_send_msg # OkatronServer <-> OkatronController

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
        if self.state.status == Status.IDLE:
            # 画像取得
            img = self.captorWork()

        elif self.state.status == Status.WORKING:
            # AI処理
            img = self.captorWork()
            det, img = self.inferencerWork(img)
            msg = self.postProcDet(det)
            self.motorcontrollerWork(msg)

        return img

    def manualMode(self):
        """マニュアルモードの動作"""
        # 画像取得
        img = self.captorWork()
        try:
            msg = self.q_recv_msg.get(False)
            print("Recv[Server]:{}".format(msg))
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

    def captorWork(self) -> None:
        """画像を取得する"""
        img = self.state.captor.capture()
        return img

    def inferencerWork(self, img) -> np.ndarray:
        """AI処理する"""
        det = self.state.yolov5.detect(img)
        img = self.state.yolov5.showResult(img, det)
        return det, img

    def postProcDet(self, det: np.ndarray):
        """YOLOの検出結果から距離・角度を算出する"""
        # タイヤの動作決定
        move_direction = "top"
        move_length = 5

        # カメラの動作決定
        camera_direction = "top"
        camera_deg = 5
        msg = {"move": [move_direction, move_length],
               "camera": [camera_direction, camera_deg]}
        return msg

    def motorcontrollerWork(self, msg: dict) -> bool:
        """
        モータを制御する
        Args:
            msg: 動作を指示するメッセージ
                 0: ON
                 数字: 動作する距離・角度
        """
        if msg["move"][0] == None and msg["camera"][0] == None:
            pass
        else:
            self.q_send_msg.put(msg) # OkatronControllerへ渡す
