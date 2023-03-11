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
        self.OUTPUT_PIN_STBY = 4
        self.OUTPUT_PIN_LF = 5
        self.OUTPUT_PIN_LR = 6
        self.OUTPUT_PIN_LPWM = 7
        self.OUTPUT_PIN_RF = 8
        self.OUTPUT_PIN_RR = 9
        self.OUTPUT_PIN_RPWM = 10

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.OUTPUT_PIN_STBY, GPIO.OUT)
        GPIO.setup(self.OUTPUT_PIN_LF, GPIO.OUT)
        GPIO.setup(self.OUTPUT_PIN_LR, GPIO.OUT)
        GPIO.setup(self.OUTPUT_PIN_RF, GPIO.OUT)
        GPIO.setup(self.OUTPUT_PIN_RR, GPIO.OUT)

        pi.wiringPiSetupGpio()
        pi.pinMode(self.OUTPUT_PIN_LPWM, pi.OUTPUT)
        pi.pinMode(self.OUTPUT_PIN_RPWM, pi.OUTPUT)
        pi.softPwmCreate(self.OUTPUT_PIN_LPWM, 0, 100)
        pi.softPwmCreate(self.OUTPUT_PIN_RPWM, 0, 100)
        
        #初期値はSTBYのみON状態
        GPIO.output(self.OUTPUT_PIN_STBY, GPIO.HIGH)
        GPIO.output(self.OUTPUT_PIN_LF, GPIO.LOW)
        GPIO.output(self.OUTPUT_PIN_LR, GPIO.LOW)
        GPIO.output(self.OUTPUT_PIN_RF, GPIO.LOW)
        GPIO.output(self.OUTPUT_PIN_RR, GPIO.LOW)
        pi.softPwmWrite(self.OUTPUT_PIN_LPWM, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RPWM, 0)

        time.sleep(0.05)

    def left(self):
        """左に向く"""
        print("Left")
        GPIO.output(self.OUTPUT_PIN_LF, GPIO.LOW)
        GPIO.output(self.OUTPUT_PIN_LR, GPIO.HIGH)
        pi.softPwmWrite(self.OUTPUT_PIN_LPWM, 50)
        GPIO.output(self.OUTPUT_PIN_RF, GPIO.HIGH)
        GPIO.output(self.OUTPUT_PIN_RR, GPIO.LOW)
        pi.softPwmWrite(self.OUTPUT_PIN_RPWM, 50)
        pass

    def right(self):
        """右に向く"""
        print("Right")
        GPIO.output(self.OUTPUT_PIN_LF, GPIO.HIGH)
        GPIO.output(self.OUTPUT_PIN_LR, GPIO.LOW)
        pi.softPwmWrite(self.OUTPUT_PIN_LPWM, 50)
        GPIO.output(self.OUTPUT_PIN_RF, GPIO.LOW)
        GPIO.output(self.OUTPUT_PIN_RR, GPIO.HIGH)
        pi.softPwmWrite(self.OUTPUT_PIN_RPWM, 50)
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
        GPIO.output(self.OUTPUT_PIN_LF, GPIO.HIGH)
        GPIO.output(self.OUTPUT_PIN_LR, GPIO.LOW)
        pi.softPwmWrite(self.OUTPUT_PIN_LPWM, 50)
        GPIO.output(self.OUTPUT_PIN_RF, GPIO.HIGH)
        GPIO.output(self.OUTPUT_PIN_RR, GPIO.LOW)
        pi.softPwmWrite(self.OUTPUT_PIN_RPWM, 50)
        pass

    def back(self):
        """後進する"""
        GPIO.output(self.OUTPUT_PIN_LF, GPIO.LOW)
        GPIO.output(self.OUTPUT_PIN_LR, GPIO.HIGH)
        pi.softPwmWrite(self.OUTPUT_PIN_LPWM, 50)
        GPIO.output(self.OUTPUT_PIN_RF, GPIO.LOW)
        GPIO.output(self.OUTPUT_PIN_RR, GPIO.HIGH)
        pi.softPwmWrite(self.OUTPUT_PIN_RPWM, 50)
        pass

    def stop(self):
        pi.softPwmWrite(self.OUTPUT_PIN_LPWM, 0)
        pi.softPwmWrite(self.OUTPUT_PIN_RPWM, 0)
        """止まる(ショートストップ)"""

class ServoController():
    """サーボモータ制御"""
    def __init__(self) -> None:
        #サーボモーターの初期設定
        print("サーボsetting...")
        GPIO.setmode(GPIO.BCM)
        self.OUTPUT_PIN_CAMV = 11
        self.OUTPUT_PIN_CAMH = 12
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
        degree = -60
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
        degree = 60
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
        degree = 15
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
        degree = -15
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