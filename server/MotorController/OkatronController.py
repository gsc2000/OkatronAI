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
            msg: list = await self.q_msg.get()
            print("Recv from Server[Controller]\t{}".format(msg))
            device = msg[0]
            if device == "move":
                await q_dc.put(msg[1:])
            elif device == "camera":
                await q_servo.put(msg[1:])
            await asyncio.sleep(0.001)

    async def dcControl(self, q_dc: asyncio.Queue):
        """DCモータ制御"""
        while True:
            msg: list = await q_dc.get() # キューに格納されるまでブロック
            print("Recv from Controller[DC]\t{}".format(msg))
            motion = msg[0] # 動作を取得
            val = msg[1]

            if motion == "coord":
                self.dc.each_control(val[0], val[1])
            else:
                if motion == "stop":
                    self.dc.stop()
                elif motion == "forward":
                    self._subdcControl(self.dc.forward, val[0], val[1])
                elif motion == "left":
                    self._subdcControl(self.dc.left, val[0], val[1])
                elif motion == "right":
                    self._subdcControl(self.dc.right, val[0], val[1])
                elif motion == "back":
                    self._subdcControl(self.dc.back, val[0], val[1])

    def _subdcControl(self, func, val_left: int, val_right: int):
        """DCモータ制御サブ"""
        func() # ON
        if val_left == None and val_right == None: # 値が-1の場合はONして終わり
            pass
        else:
            time.sleep(val_left[0]) # 0以上の場合は、停止
            self.dc.stop()

    async def servoControl(self, q_servo: asyncio.Queue):
        while True:
            msg = await q_servo.get() # キューに格納されるまでブロック
            print("Recv from Controller[Servo]\t{}".format(msg))
            motion = msg[0] # 動作を取得
            coord = msg[1] # 値を取得
            flg = True

            if motion == "stop":
                self.dc.stop()
                flg = False
                motion = None
            elif motion == "top":
                self.servo.up()
            elif motion == "left":
                self.servo.left()
            elif motion == "right":
                self.servo.right()
            elif motion == "bottom":
                self.servo.down()

