"""OkatronServer"""

import os
import sys

import cv2
import numpy as np

import DataBaseapi as db
from UserIO import UserIO, UserReq
from OkatronState import OkatronState, Mode, Status
from Captor.WebCamera import WebCamera
from Inferencer.YOLOv5Detector import YOLOv5Detector

class OkatronServer():
    """アプリ本体
    Serverを介してGUIから届くユーザリクエストの処理や
    内部状態に応じて行う処理を変更
    """
    def __init__(self, state) -> None:
        self.state: OkatronState = state

        self.show_img = None

        # テスト
        cv2.namedWindow("Test", cv2.WINDOW_NORMAL)

    def run(self) -> None:
        """メインループ"""
        while True:
            if self.state.status == Status.IDLE:
                # 画像取得
                img = self.captor_work()
            elif self.state.status == Status.WORKING:
                # AI処理
                img = self.captor_work()
                det, img = self.inferencer_work(img)
                res = self.motorcontroller_work(det)

            cv2.imshow("Test", img)
            cv2.waitKey(1)
            self.updateState()

    def updateState(self) -> None:
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

    def user_io_work(self) -> None:
        """ユーザからのリクエストを処理する"""
        msg = self.state.user_io.recvMesse()
        return msg

    def captor_work(self) -> None:
        """画像を取得する"""
        img = self.state.captor.capture()
        # print(img.shape)
        return img

    def inferencer_work(self, img) -> np.ndarray:
        """AI処理する"""
        det = self.state.yolov5.detect(img)
        img = self.state.yolov5.showResult(img, det)
        return det, img

    def motorcontroller_work(self, det) -> bool:
        """モータを制御する"""
        return True