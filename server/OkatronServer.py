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

        self.user_io = False

        # テスト
        # cv2.namedWindow("Test", cv2.WINDOW_NORMAL)

    def run(self) -> None:
        """メインループ"""
        # while True:
        if self.state.mode == Mode.AUTO:
            img = self.autoMode()
        elif self.state.mode == Mode.MANUAL:
            self.manualMode()
        elif self.state.mode == Mode.PROGRAM:
            self.programMode()

        self.updateState()

        # self.show_img = img
        return img

    def autoMode(self):
        """自動追従モードの動作"""
        img = np.zeros((240, 320, 3), dtype="uint8")
        if self.state.status == Status.IDLE:
            # 画像取得
            img = self.captorWork()
            # self.showImg(img)
        elif self.state.status == Status.WORKING:
            # AI処理
            img = self.captorWork()
            lap_time = time.time()
            det, img = self.inferencerWork(img)
            print("YOLO FPS:\t{}".format((time.time()-lap_time+0.0001)**-1))
            res = self.motorcontroller_work(det)

            # self.showImg(img)
        return cv2.imencode('.jpg', img)[1].tobytes()

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
        # msg = self.userioWork()
        if self.user_io == UserReq.START:
            self.state.status = Status.WORKING
            self.user_io = UserReq.NONE
        elif self.user_io == UserReq.STOP:
            self.state.status = Status.IDLE

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
        img = cv2.imencode('.jpg', img)[1].tobytes()
        return img

    def userioWork(self) -> str:
        """ユーザからのリクエストを処理する"""
        # テスト用
        msg = None
        # key = cv2.waitKey(1)
        # if key == ord("s"):
        #     msg = "Start"
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