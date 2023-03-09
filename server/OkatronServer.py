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

e = 0.000001

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
            st_time = time.time()
            img = self.captorWork()
            det, img = self.inferencerWork(img)
            sendable = self.state.adjustContSpan()
            if sendable:
                msg = self.postProcDet(det)
                await self.motorcontrollerWork(msg)
            fps = (time.time()-st_time+e)**-1
            print("FPS:\t{:.2f}".format(fps))
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
            print("Recv[Server]:\t{}".format(msg))
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
        center, size, img = self.state.facecascade.detect(img, det)
        det = {"center": center, "size": size}
        return det, img

    def postProcDet(self, det: np.ndarray):
        """YOLOの検出結果から距離・角度を算出する
        物体が中心に来るようにカメラを動かす"""
        msg_list = []
        if det["center"][0] == None:
            return None

        move_ratio = 50
        camera_ratio = 50

        x = 2*det["center"][0]/self.state.width # 0~2
        x = (x-1)*move_ratio # -1~1

        y = 1*move_ratio # とりあえず固定値

        z = 2*det["center"][1]/self.state.height # 0~2
        z = (z-1)*camera_ratio # -1~1

        # 座標推定
        msg = ["move", "coord", [int(x), int(y)]] # [機器, 方向, 座標(x, y)]
        msg_list.append(msg)

        # # カメラの動作決定
        msg = ["camera", "coord", [int(x), int(z)]] # [機器, 方向, 座標(x, z)]
        msg_list.append(msg)

        print("Det[Server]\t{}".format(msg_list))
        return msg_list

    async def motorcontrollerWork(self, msg: list) -> bool:
        """モータを制御する"""
        if msg == None:
            print("None Det")
            self.state.adjustLostCount(False)
            if self.state.lost: # 対象ロスト -> 検索処理
                msg = [self.searchObject()]
            else:
                return False
        else:
            self.state.adjustLostCount(True)

        for _msg in msg:
            await self.state.q_cont_msg.put(_msg) # OkatronControllerへ渡す
        return True

    def searchObject(self):
        search_seq = [["camera", "left", [None, None]],
                      ["camera", "top", [None, None]],
                      ["camera", "right", [None, None]],
                      ["camera", "bottom", [None, None]]]
        msg = search_seq[self.state.search_step]
        self.state.search_step += 1
        if self.state.search_step > len(search_seq)-1:
            self.state.search_step = 0
        return msg
