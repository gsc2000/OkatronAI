"""OkatronServer"""

import os
import sys

import asyncio

import DataBaseapi as db
from UserIO import UserIO, UserReq
from OkatronState import OkatronState, Mode, Status
from Captor.WebCamera import WebCamera
from Inferencer.YOLOv5Detector import YOLOv5Detector

class OkatronServer():
    """アプリ本体"""
    def __init__(self, state) -> None:
        self.state: OkatronState = state

        self.show_img = None
        self.setting()

    def setting(self):
        self.user_io = UserIO()
        self.captor = WebCamera(self.state.camera)
        self.inferencer = YOLOv5Detector(self.state.yolov5)

    def run(self):
        while True:
            if self.state.status == Status.IDLE:
                # 画像取得
                self.captor_work()
            elif self.state.status == Status.WORKING:
                # AI処理
                img = self.captor_work()
                det = self.inferencer_work(img)

            self.updateState()

    def updateState(self):
        """アプリの状態を更新する"""
        now_status = self.state.status

        msg = self.user_io_work()
        if msg == UserReq.START:
            self.state.status(Status.WORKING)

        if now_status == Status.IDLE:
            pass
        elif now_status == Status.WORKING:
            pass

        if now_status != self.state.status:
            print("State Change:\t[ {} -> {} ]".format(now_status.name, self.state.status.name))

    def user_io_work(self):
        """ユーザからのリクエストを処理する"""
        msg = self.user_io.recvMesse()
        return msg

    def captor_work(self):
        """画像を取得する"""
        img = self.captor.capture()
        print(img.shape)
        return img

    def inferencer_work(self, img):
        """AI処理する"""
        # det = self.inferencer.detect(img)
        # return det
        pass

    def motorcontroller_work(self, det):
        """モータを制御する"""
        pass