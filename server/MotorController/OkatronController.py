"""Okatron用モータ制御"""
import os
import sys
# import RPi.GPIO as GPIO
# import wiringpi as pi

import asyncio
import threading
import numpy as np
import queue
import time

try:
    import RPi.GPIO as GPIO # ラズパイか判断する
    from MotorController.BaseController import DCController, ServoController
except:
    from MotorController.BaseController import NullDCController as DCController
    from MotorController.BaseController import NullServoController as ServoController

class OkatronController():
    """Okatron用モータ制御のクラス"""
    def __init__(self, q_msg: asyncio.Queue) -> None:
        self.dc = DCController()
        self.servo = ServoController()

        self.q_msg = q_msg

    async def run(self):
        """
        検出結果の処理はここで行う
        """
        print("Okatron Controller Start")
        q_dc = asyncio.Queue()
        q_servo = asyncio.Queue()
        asyncio.create_task(self.dcControl(q_dc))
        asyncio.create_task(self.servoControl(q_servo))

        while True:
            msg: dict = await self.q_msg.get()

            if "move" in msg.keys():
                await q_dc.put(msg["move"])
            elif "camera" in msg.keys():
                await q_servo.put(msg["camera"])
            await asyncio.sleep(0.01)

    async def dcControl(self, q_dc: asyncio.Queue):
        """DCモータ制御"""
        while True:
            msg = await q_dc.get() # キューに格納されるまでブロック
            motion = msg[0] # 動作を取得
            val_right = msg[1][0] # 左出力値を取得
            val_left = msg[1][1] # 右出力値を取得

            if motion == "stop":
                self.dc.stop()
            elif motion == "forward":
                self._subdcControl(self.dc.forward, val_right, val_left)
            elif motion == "left":
                self._subdcControl(self.dc.left, val_right, val_left)
            elif motion == "right":
                self._subdcControl(self.dc.right, val_right, val_left)
            elif motion == "back":
                self._subdcControl(self.dc.back, val_right, val_left)

    def _subdcControl(self, func, val_right: int, val_left: int):
        """DCモータ制御サブ"""
        func() # ON
        if val_right == -1: # 値が-1の場合はONして終わり
            pass
        else:
            time.sleep(val_right[0]) # 0以上の場合は、停止
            self.dc.stop()

    async def servoControl(self, q_servo: asyncio.Queue):
        while True:
            msg = await q_servo.get() # キューに格納されるまでブロック
            motion = msg[0] # 動作を取得
            value = msg[1] # 値を取得

            if motion == "stop":
                self.dc.stop()
            elif motion == "top":
                self.servo.up()
            elif motion == "left":
                self.servo.left()
            elif motion == "right":
                self.servo.right()
            elif motion == "bottom":
                self.servo.down()

