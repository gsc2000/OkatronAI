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
    def __init__(self) -> None:
        self.dc = DCController()
        self.servo = ServoController()

    def run(self, q_msg: queue.Queue):
        """
        検出結果の処理はここで行う
        """
        print("Okatron Controller Start")
        # 平行処理
        q_dc = queue.Queue(maxsize=1) # DC用キュー
        q_servo = queue.Queue(maxsize=1) # SERVO用キュー
        thread_dc = threading.Thread(target=self.dcControl, args=(q_dc, ))
        thread_dc.daemon = True
        thread_servo = threading.Thread(target=self.servoControl, args=(q_servo, ))
        thread_servo.daemon = True

        thread_dc.start()
        thread_servo.start()

        while True:
            try:
                msg = q_msg.get()
                print("Recv[Controller]:{}".format(msg))

                if not q_dc.full(): # キューがいっぱいだったら捨てる
                    q_dc.put(msg["move"])
                if not q_servo.full(): # キューがいっぱいだったら捨てる
                    q_servo.put(msg["camera"])
            except:
                pass

    def dcControl(self, q_msg: queue.Queue):
        """DCモータ制御"""
        while True:
            msg = q_msg.get() # キューに格納されるまでブロック
            motion = msg[0] # 動作を取得
            value = msg[1] # 値を取得

            if motion == "stop":
                self.dc.stop()
            elif motion == "top":
                self.subdcControl(self.dc.forward, value)
            elif motion == "left":
                self.subdcControl(self.dc.left, value)
            elif motion == "right":
                self.subdcControl(self.dc.right, value)
            elif motion == "bottom":
                self.subdcControl(self.dc.back, value)

            time.sleep(0.01) # スリープ設けないと動作を占有する可能性あり

    def subdcControl(self, func, value: int):
        """DCモータ制御サブ"""
        func() # ON
        if value == -1: # 値が-1の場合はONして終わり
            pass
        else:
            time.sleep(value) # 0以上の場合は、停止
            self.dc.stop()

    def servoControl(self, q_msg: queue.Queue):
        while True:
            msg = q_msg.get() # キューに格納されるまでブロック
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

    def subservoControl(self, func, value):
        """サーボ制御サブ"""
        pass

