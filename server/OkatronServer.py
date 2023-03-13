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

e = 0.000001 # ゼロ割対策

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
        if self.state.status == Status.IDLE: # 画像取得のみ
            img = self.captorWork()
        elif self.state.status == Status.WORKING: # AI処理
            st_time = time.time()
            img = self.captorWork()
            sendable = self.state.adjustContSpan()
            if sendable:
                det, img = self.inferencerWork(img)
                motion, x, y, z = self.postProcDet(det)
                msg = self.createContMessage(None, motion, x, y, z)
                await self.motorcontrollerWork(msg)
            fps = (time.time()-st_time+e)**-1
            # print("FPS:\t{:.2f}".format(fps))
        return img

    async def manualMode(self) -> np.ndarray:
        """マニュアルモードの動作"""
        # 画像取得
        img = self.captorWork()
        q_size = self.state.q_user_req.qsize()
        if q_size == 0:
            pass
        else:
            user_msg = await self.state.q_user_req.get()
            msg = self.createContMessage(user_msg[0], user_msg[1], None, None, None)
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
        """物体検出結果から座標を算出する"""
        if det["center"][0] == None:
            return None, None, None, None
        move_ratio = 50
        camera_ratio = 50
        x = 2*det["center"][0]/self.state.width # 0~2
        x = (x-1)*move_ratio # -1~1
        y = 1*move_ratio # とりあえず固定値 det["size"]から推定
        z = 2*det["center"][1]/self.state.height # 0~2
        z = (z-1)*camera_ratio # -1~1
        return "coord", x, y, z

    def createContMessage(self, device, motion, x, y, z):
        """コントローラ用のメッセージ作成"""
        msg_list = []
        if self.state.mode == Mode.AUTO:
            if motion == None: # 物体が検出できなかった場合
                print("Can't Detection")
                self.state.adjustLostCount(False)
                if self.state.lost: # 対象ロスト -> 検索処理
                    print("Object Lost")
                    msg = self.searchObject()
                    msg_list.append(msg)
                else:
                    return None # 物体がないのでMessageは無し
            else:
                coord = [int(x)+self.state.camera_coord[0], int(y)] # Cameraの座標を足す
                msg = ["move", motion, coord]
                self.state.adjustLostCount(True)
                msg_list.append(msg)
                msg = ["camera", motion, [0, int(z)]] # 物体を検出しているのでカメラを中心に戻す
                msg_list.append(msg)
        elif self.state.mode == Mode.MANUAL: # Manualモードでは方向で指示
            coord = [None, None]
            msg = [device, motion, coord]
            msg_list.append(msg)
        elif self.state.mode == Mode.PROGRAM:
            pass
        return msg_list

    async def motorcontrollerWork(self, msg: list) -> bool:
        """モータを制御する"""
        if msg == None:
            return False

        for _msg in msg:
            print("Send to Controller[Server]:\t{}".format(_msg))
            if _msg[0] == "camera" and _msg[1] == "coord":
                self.state.camera_coord = _msg[2] # Cameraの座標を保持する
            q_size = self.state.q_cont_msg.qsize()
            if q_size == 0:
                await self.state.q_cont_msg.put(_msg) # OkatronControllerへ渡す
            else:
                pass

        return True

    def searchObject(self):
        search_seq = [["camera", "top", [-50, 0]],
                      ["camera", "left", [-50, 0]],
                      ["camera", "coord", [-50, 0]],
                      ["camera", "coord", [0, 0]]]
        msg = search_seq[self.state.search_step]
        self.state.search_step += 1
        if self.state.search_step > len(search_seq)-1:
            self.state.search_step = 0
        return msg
