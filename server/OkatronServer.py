"""OkatronServer"""

import os
import sys

import time
import cv2
import numpy as np

import DataBaseapi as db
from UserIO import UserIO, UserReq
from OkatronState import OkatronState, Mode, Status
from Captor.WebCamera import WebCamera
from Inferencer.YOLOv5Detector import YOLOv5Detector

class OkatronServer():
    """アプリ本体
    GUIから届くユーザリクエストの処理や
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
            if self.state.mode == Mode.AUTO:
                self.autoMode()
            elif self.state.mode == Mode.MANUAL:
                self.manualMode()
            elif self.state.mode == Mode.PROGRAM:
                self.programMode()

            self.updateState()

    def autoMode(self):
        """自動追従モードの動作"""
        if self.state.status == Status.IDLE:
            # 画像取得
            img = self.captorWork()
            self.showImg(img)
        elif self.state.status == Status.WORKING:
            # AI処理
            img = self.captorWork()
            det, img = self.inferencerWork(img)
            res = self.motorcontroller_work(det)

            self.showImg(img)

    def manualMode(self):
        """マニュアルモードの動作"""
        pass

    def programMode(self):
        """プログラムモードの動作"""
        pass

    def updateState(self) -> None:
        """アプリの状態を更新する"""
        now_status = self.state.status

        # time.sleep(1)
        msg = self.userioWork()
        if msg == UserReq.START.value:
            self.state.status = Status.WORKING

        if now_status == Status.IDLE:
            pass
        elif now_status == Status.WORKING:
            pass

        if now_status != self.state.status:
            print("State Change:\t[ {} -> {} ]".format(now_status.name, self.state.status.name))

    def showImg(self, img: np.ndarray):
        """GUIに表示する画像の処理
        Args:
            img: 表示したい画像
        """
        # テスト用
        cv2.imshow("Test", img)

    def userioWork(self) -> str:
        """ユーザからのリクエストを処理する"""
        # テスト用
        msg = None
        key = cv2.waitKey(1)
        if key == ord("s"):
            msg = "Start"
        # msg = self.state.user_io.recvMesse()
        return msg

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

    def motorcontroller_work(self, det) -> bool:
        """モータを制御する"""
        return True