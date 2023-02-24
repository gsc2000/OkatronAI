"""Okatron用モータ制御"""
import os
import sys
import RPi.GPIO as GPIO
import wiringpi as pi

import numpy as np

from MotorController.BaseController import DCController, ServoController

class OkatronController():
    """Okatron用モータ制御のクラス"""
    def __init__(self) -> None:
        self.dc = DCController()
        self.servo = ServoController()

    def run(self, det):
        """
        検出結果の処理はここで行う
        """
        self.preprecess(det)
        pass

    def preprecess(self, det: np.ndarray) -> np.ndarray:
        """
        前処理 推論結果をモータ制御用に処理する
        Args:
            det: 検出結果
        Returns:
            np.ndarray: 成形後データ
        """
        pass
