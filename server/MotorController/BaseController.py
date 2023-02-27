"""モータ用の制御"""
import sys
import time
import RPi.GPIO as GPIO
import wiringpi as pi

class DCController():
    """DCモータ制御"""
    def __init__(self) -> None:
        #DCモーターに関する設定
        #GPIOピンの初期化
        self.STBY = 4
        self.OUTPUT_PIN_LF = 5
        self.OUTPUT_PIN_LR = 6
        self.OUTPUT_PIN_RF = 7
        self.OUTPUT_PIN_RR = 8

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( self.STBY, GPIO.OUT )

        pi.wiringPiSetupGpio()
        pi.pinMode(self.OUTPUT_PIN_LF, pi.OUTPUT)
        pi.pinMode(self.OUTPUT_PIN_LR, pi.OUTPUT)
        pi.pinMode(self.OUTPUT_PIN_RF, pi.OUTPUT)
        pi.pinMode(self.OUTPUT_PIN_RR, pi.OUTPUT)
        pi.softPwmCreate(self.OUTPUT_PIN_LF, 0, 100)
        pi.softPwmCreate(self.OUTPUT_PIN_LR, 0, 100)
        pi.softPwmCreate(self.OUTPUT_PIN_RF, 0, 100)
        pi.softPwmCreate(self.OUTPUT_PIN_RR, 0, 100)
        #初期値はSTBYのみON状態
        GPIO.output( self.STBY, GPIO.HIGH )
        pi.softPwmWrite(self.OUTPUT_PIN_LF, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_LR, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RF, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RR, 0)

        time.sleep(0.05)

    def left(self):
        """左に向く"""
        print("Left")
        pi.softPwmWrite(self.OUTPUT_PIN_LF, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_LR, 50)
        pi.softPwmWrite(self.OUTPUT_PIN_RF, 50)
        pi.softPwmWrite(self.OUTPUT_PIN_RR, 0)
        pass

    def right(self):
        """右に向く"""
        print("Right")
        pi.softPwmWrite(self.OUTPUT_PIN_LF, 50)
        pi.softPwmWrite(self.OUTPUT_PIN_LR, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RF, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RR, 50)
        pass

    def up(self):
        """前or上に向く"""
        pass

    def down(self):
        """後ろor下に向く"""
        pass

    def forward(self):
        """前進する"""
        print("Foward")
        pi.softPwmWrite(self.OUTPUT_PIN_LF, 50)
        pi.softPwmWrite(self.OUTPUT_PIN_LR, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RF, 50)
        pi.softPwmWrite(self.OUTPUT_PIN_RR, 0)
        pass

    def back(self):
        """後進する"""
        pi.softPwmWrite(self.OUTPUT_PIN_LF, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_LR, 50)
        pi.softPwmWrite(self.OUTPUT_PIN_RF, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RR, 50)
        pass

    def stop(self):
        pi.softPwmWrite(self.OUTPUT_PIN_LF, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_LR, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RF, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RR, 0)
        """止まる"""

class ServoController():
    """サーボモータ制御"""
    def __init__(self) -> None:
        #サーボモーターの初期設定
        print("サーボsetting...")
        GPIO.setmode(GPIO.BCM)
        self.OUTPUT_PIN_CAMV = 9
        self.OUTPUT_PIN_CAMH = 10
        GPIO.setup(self.OUTPUT_PIN_CAMV, GPIO.OUT)
        GPIO.setup(self.OUTPUT_PIN_CAMH, GPIO.OUT)
        self.v = GPIO.PWM(self.OUTPUT_PIN_CAMV, 50) #PWM設定、周波数は50Hz
        self.h = GPIO.PWM(self.OUTPUT_PIN_CAMH, 50) #PWM設定、周波数は50Hz

        self.v.start(0.0)
        self.h.start(0.0)
        
        degree = 0
        dc = 2.5 + (12.0-2.5)/180*(degree+90)
        #DutyCycle dc%
        self.h.ChangeDutyCycle(dc)
        self.v.ChangeDutyCycle(dc)
        #最大180°回転を想定し、0.3sec以上待つ
        time.sleep(1)
        #回転終了したら一旦DutyCycle0%にする
        self.h.ChangeDutyCycle(0.0)
        self.v.ChangeDutyCycle(0.0)
        print("...done")
        pass

    def left(self):
        """左に向く"""
        print("CAM left")
        degree = -90
        dc = 2.5 + (12.0-2.5)/180*(degree+90)
        #DutyCycle dc%
        self.h.ChangeDutyCycle(dc)
        #最大180°回転を想定し、0.3sec以上待つ
        time.sleep(0.3)
        #回転終了したら一旦DutyCycle0%にする
        self.h.ChangeDutyCycle(0.0)
        pass

    def right(self):
        """右に向く"""
        print("CAM right")
        degree = 90
        dc = 2.5 + (12.0-2.5)/180*(degree+90)
        #DutyCycle dc%
        self.h.ChangeDutyCycle(dc)
        #最大180°回転を想定し、0.3sec以上待つ
        time.sleep(0.3)
        #回転終了したら一旦DutyCycle0%にする
        self.h.ChangeDutyCycle(0.0)
        pass

    def up(self):
        """前or上に向く"""
        print("CAM up")
        degree = 90
        dc = 2.5 + (12.0-2.5)/180*(degree+90)
        #DutyCycle dc%
        self.v.ChangeDutyCycle(dc)
        #最大180°回転を想定し、0.3sec以上待つ
        time.sleep(0.3)
        #回転終了したら一旦DutyCycle0%にする
        self.v.ChangeDutyCycle(0.0)
        pass

    def down(self):
        """後ろor下に向く"""
        print("CAM down")
        degree = -90
        dc = 2.5 + (12.0-2.5)/180*(degree+90)
        #DutyCycle dc%
        self.v.ChangeDutyCycle(dc)
        #最大180°回転を想定し、0.3sec以上待つ
        time.sleep(0.3)
        #回転終了したら一旦DutyCycle0%にする
        self.v.ChangeDutyCycle(0.0)
        pass

    def forward(self):
        """前進する"""
        pass

    def back(self):
        """後進する"""

class NullDCController():
    """机上テスト用クラス"""
    def __init__(self) -> None:
        pass

    def left(self):
        """左に向く"""
        print("Left")
        pass

    def right(self):
        """右に向く"""
        print("Right")
        pass

    def up(self):
        """前or上に向く"""
        pass

    def down(self):
        """後ろor下に向く"""
        pass

    def forward(self):
        """前進する"""
        print("Foward")
        pass

    def back(self):
        """後進する"""
        print("Back")
        pass

    def stop(self):
        """止まる"""
        print("Stop")

class NullServoController():
    """机上テスト用クラス"""
    def __init__(self) -> None:
        pass

    def left(self):
        """左に向く"""
        print("Left")
        pass

    def right(self):
        """右に向く"""
        print("Right")
        pass

    def up(self):
        """前or上に向く"""
        pass

    def down(self):
        """後ろor下に向く"""
        pass

    def forward(self):
        """前進する"""
        print("Foward")
        pass

    def back(self):
        """後進する"""
        print("Back")
        pass

    def stop(self):
        """止まる"""
        print("Stop")