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
    def __init__(self, state) -> None:
        self.state: OkatronState = state

    async def run(self) -> None:
        # ループの開始はAppが担う
        asyncio.create_task(self.state.cont.run())
        asyncio.create_task(self.main())

    async def main(self):
        while True:
            if self.state.mode == Mode.AUTO:
                img = await self.autoMode()
            elif self.state.mode == Mode.MANUAL:
                img = await self.manualMode()
            elif self.state.mode == Mode.PROGRAM:
                img = self.programMode()
            else:
                pass

            self.state.img = img.copy()
            await asyncio.sleep(0)


    async def autoMode(self) -> np.ndarray:
        """自動追従モードの動作"""
        if self.state.status == Status.IDLE:
            # 画像取得
            img = self.captorWork()

        elif self.state.status == Status.WORKING:
            # AI処理
            img = self.captorWork()
            det, img = self.inferencerWork(img)
            msg = self.postProcDet(det)
            await self.motorcontrollerWork(msg)

        return img

    async def manualMode(self) -> np.ndarray:
        """マニュアルモードの動作"""
        # 画像取得
        img = self.captorWork()

        q_size = self.state.q_user_req.qsize()
        if q_size == 0:
            pass
        else:
            msg = await self.state.q_user_req.get()
            print("Recv[Server]:{}".format(msg))
            await self.motorcontrollerWork(msg)
        return img

    def programMode(self) -> np.ndarray:
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
        # img, center = self.state.facecascade.detect(img, det)
        return det, img

    def postProcDet(self, det: np.ndarray):
        """YOLOの検出結果から距離・角度を算出する"""
        # タイヤの動作決定
        move_direction = "top"
        move_val = [5, 5]

        # カメラの動作決定
        camera_direction = "top"
        camera_deg = 5
        msg = [{"move": [move_direction, move_val]}]
        return msg

    async def motorcontrollerWork(self, msg: list) -> bool:
        """
        モータを制御する
        オートモードの場合はここで左右の出力値を決める
        """
        for _msg in msg:
            await self.state.q_cont_msg.put(_msg) # OkatronControllerへ渡す
