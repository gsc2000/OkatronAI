"""Okatron用モータ制御"""
import os
import sys
# import RPi.GPIO as GPIO
# import wiringpi as pi

import asyncio
import numpy as np

# from MotorController.BaseController import DCController, ServoController

class OkatronController():
    """Okatron用モータ制御のクラス"""
    def __init__(self) -> None:
        # self.dc = DCController()
        # self.servo = ServoController()
        pass

    def run(self, msg: dict):
        """
        検出結果の処理はここで行う
        """
        print("msg:{}".format(msg))
        # asyncio.sleep(0)
        # self.preprecess(det)
        pass

    def preprecess(self, det: np.ndarray) -> np.ndarray:
        """
        前処理
        """
        pass
