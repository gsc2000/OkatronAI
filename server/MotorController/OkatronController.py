"""Okatron用モータ制御"""
import os
import sys
# import RPi.GPIO as GPIO
# import wiringpi as pi

import asyncio
import numpy as np
import queue

# from MotorController.BaseController import DCController, ServoController

class OkatronController():
    """Okatron用モータ制御のクラス"""
    def __init__(self) -> None:
        # self.dc = DCController()
        # self.servo = ServoController()
        pass

    def run(self, q_msg: queue.Queue):
        """
        検出結果の処理はここで行う
        """
        print("Okatron Controller Start")
        while True:
            try:
                msg = q_msg.get()
                print("Recv[Controller]:{}".format(msg))

                self.dcControl(msg["move"])
            except:
                pass

    def dcControl(self, msg: list):
        """DCモータ制御"""
        motion = msg[0]
        value = msg[1]

        if motion == "stop":
            # STOP処理
            pass
        elif motion == "top":
            self.subdcControl(test_forward, value)
        elif motion == "left":
            self.subdcControl(test_forward, value)
        elif motion == "right":
            self.subdcControl(test_forward, value)
        elif motion == "bottom":
            self.subdcControl(test_forward, value)

    def subdcControl(self, method, value: int):
        """DCモータ制御サブ"""
        if value == 0:
            print("PIN ON処理")
        else:
            for i in range(value): # 必要回数繰り返す
                method()

    def servoControl(self, msg: list):
        pass


def test_forward():
    """テスト用"""
    print("forward")
