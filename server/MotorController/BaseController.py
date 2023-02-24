"""モータ用の制御"""
import sys
import time
import RPi.GPIO as GPIO
import wiringpi as pi

class DCController():
    """DCモータ制御"""
    def __init__(self) -> None:
        MOTOR_L1 = 18
        MOTOR_L2 = 23
        MOTOR_R1 = 24
        MOTOR_R2 = 25

        OUTPUT_PIN_L = 13
        OUTPUT_PIN_R = 19

        GPIO.setmode( GPIO.BCM )
        GPIO.setup( MOTOR_L1, GPIO.OUT )
        GPIO.setup( MOTOR_L2, GPIO.OUT )
        GPIO.setup( MOTOR_R1, GPIO.OUT )
        GPIO.setup( MOTOR_R2, GPIO.OUT )

        pi.wiringPiSetupGpio()
        pi.pinMode(OUTPUT_PIN_L, pi.OUTPUT)
        pi.pinMode(OUTPUT_PIN_R, pi.OUTPUT)

        pi.softPwmCreate(OUTPUT_PIN_L, 0, 100)
        pi.softPwmCreate(OUTPUT_PIN_R, 0, 100)

    def left(self):
        """左に向く"""
        print("Left")
        stop_motor()
        GPIO.output( MOTOR_L1, GPIO.HIGH )
        GPIO.output( MOTOR_L2, GPIO.LOW )
        GPIO.output( MOTOR_R1, GPIO.HIGH )
        GPIO.output( MOTOR_R2, GPIO.LOW )

        pi.softPwmWrite(OUTPUT_PIN_L, 30)
        pi.softPwmWrite(OUTPUT_PIN_R, 15)
        pass

    def right(self):
        """右に向く"""
        print("Right")
        stop_motor()
        GPIO.output( MOTOR_L1, GPIO.HIGH )
        GPIO.output( MOTOR_L2, GPIO.LOW )
        GPIO.output( MOTOR_R1, GPIO.HIGH )
        GPIO.output( MOTOR_R2, GPIO.LOW )

        pi.softPwmWrite(OUTPUT_PIN_L, 15)
        pi.softPwmWrite(OUTPUT_PIN_R, 30)
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
        stop_motor()
        GPIO.output( MOTOR_L1, GPIO.HIGH)
        GPIO.output( MOTOR_L2, GPIO.LOW )
        GPIO.output( MOTOR_R1, GPIO.HIGH )
        GPIO.output( MOTOR_R2, GPIO.LOW )

        pi.softPwmWrite(OUTPUT_PIN_L, 5)
        pi.softPwmWrite(OUTPUT_PIN_R, 5)
        pass

    def back(self):
        """後進する"""
        stop_motor()
        GPIO.output( MOTOR_L1, GPIO.LOW )
        GPIO.output( MOTOR_L2, GPIO.HIGH )
        GPIO.output( MOTOR_R1, GPIO.LOW )
        GPIO.output( MOTOR_R2, GPIO.HIGH )

        pi.softPwmWrite(OUTPUT_PIN_L, 15)
        pi.softPwmWrite(OUTPUT_PIN_R, 15)
        pass

    def stop(self):
        """止まる"""
        GPIO.output( MOTOR_L1, GPIO.LOW )
        GPIO.output( MOTOR_L2, GPIO.LOW )
        GPIO.output( MOTOR_R1, GPIO.LOW )
        GPIO.output( MOTOR_R2, GPIO.LOW )

        pi.softPwmWrite(OUTPUT_PIN_L, 0)
        pi.softPwmWrite(OUTPUT_PIN_R, 0)

        time.sleep(0.05)

class ServoController():
    """サーボモータ制御"""
    def __init__(self) -> None:
        pass

    def left(self):
        """左に向く"""
        pass

    def right(self):
        """右に向く"""
        pass

    def up(self):
        """前or上に向く"""
        pass

    def down(self):
        """後ろor下に向く"""
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