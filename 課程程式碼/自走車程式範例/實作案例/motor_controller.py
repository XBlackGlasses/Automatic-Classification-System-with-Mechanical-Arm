# import 控制GPIO所需的函式庫
import RPi.GPIO as GPIO

#定義名為Motor的class
class Motor:

    #定義__init__建構子，輸入參數為當前與馬達驅動器所連接的各個腳位
    def __init__(self, frontR1_pin, frontR2_pin, frontL1_pin, frontL2_pin, backR1_pin, backR2_pin, backL1_pin, backL2_pin):
        self.frontR1_pin = frontR1_pin
        self.frontR2_pin = frontR2_pin
        self.frontL1_pin = frontL1_pin
        self.frontL2_pin = frontL2_pin
        self.backR1_pin = backR1_pin
        self.backR2_pin = backR2_pin
        self.backL1_pin = backL1_pin
        self.backL2_pin = backL2_pin

        GPIO.cleanup()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.frontR1_pin, GPIO.OUT)
        GPIO.setup(self.frontR2_pin, GPIO.OUT)
        GPIO.setup(self.frontL1_pin, GPIO.OUT)
        GPIO.setup(self.frontL2_pin, GPIO.OUT)
        GPIO.setup(self.backR1_pin, GPIO.OUT)
        GPIO.setup(self.backR2_pin, GPIO.OUT)
        GPIO.setup(self.backL1_pin, GPIO.OUT)
        GPIO.setup(self.backL2_pin, GPIO.OUT)

        self.motorFR1 = GPIO.PWN(self.frontR1_pin, 500)
        self.motorFR2 = GPIO.PWN(self.frontR2_pin, 500)
        self.motorFL1 = GPIO.PWN(self.frontL1_pin, 500)
        self.motorFL2 = GPIO.PWN(self.frontL1_pin, 500)
        self.motorBR1 = GPIO.PWN(self.backR1_pin, 500)
        self.motorBR2 = GPIO.PWN(self.backR2_pin, 500)
        self.motorBL1 = GPIO.PWN(self.backL1_pin, 500)
        self.motorBL2 = GPIO.PWN(self.backL2_pin, 500)

        self.motorFR1.start(0)
        self.motorFR2.start(0)
        self.motorFL1.start(0)
        self.motorFL2.start(0)
        self.motorBR1.start(0)
        self.motorBR2.start(0)
        self.motorBL1.start(0)
        self.motorBL2.start(0)

    #定義停止函式，將所有腳位PWN設為0即可，所以不需要參數輸入
    def stop(self):
        self.motorFR1.ChangeDutyCycle(0)
        self.motorFR2.ChangeDutyCycle(0)
        self.motorFL1.ChangeDutyCycle(0)
        self.motorFL2.ChangeDutyCycle(0)
        self.motorBR1.ChangeDutyCycle(0)
        self.motorBR2.ChangeDutyCycle(0)
        self.motorBL1.ChangeDutyCycle(0)
        self.motorBL2.ChangeDutyCycle(0)
    
    #定義前進函式，多了一參數進入，可用來調整前進速度
    def forward(self, speed):
        self.motorFR1.ChangeDutyCycle(speed)
        self.motorFR2.ChangeDutyCycle(0)
        self.motorFL1.ChangeDutyCycle(speed)
        self.motorFL2.ChangeDutyCycle(0)
        self.motorBR1.ChangeDutyCycle(speed)
        self.motorBR2.ChangeDutyCycle(0)
        self.motorBL1.ChangeDutyCycle(speed)
        self.motorBL2.ChangeDutyCycle(0)

    #定義後退函式，多了一參數輸入，可用來調整後退速度
    def backword(self, speed):
        self.motorFR1.ChangeDutyCycle(0)
        self.motorFR2.ChangeDutyCycle(speed)
        self.motorFL1.ChangeDutyCycle(0)
        self.motorFL2.ChangeDutyCycle(speed)
        self.motorBR1.ChangeDutyCycle(0)
        self.motorBR2.ChangeDutyCycle(speed)
        self.motorBL1.ChangeDutyCycle(0)
        self.motorBL2.ChangeDutyCycle(speed)

    #定義右轉函式，多了一個參數輸入，可用來調整轉動速度
    #因四輪驅動關係，會使車輛似順時針轉動，固取clockwise
    def rotateClockwise(self, speed):
        self.motorFR1.ChangeDutyCycle(0)
        self.motorFR2.ChangeDutyCycle(speed)
        self.motorFL1.ChangeDutyCycle(speed)
        self.motorFL2.ChangeDutyCycle(0)
        self.motorBR1.ChangeDutyCycle(0)
        self.motorBR2.ChangeDutyCycle(speed)
        self.motorBL1.ChangeDutyCycle(speed)
        self.motorBL2.ChangeDutyCycle(0)

    #定義左轉函式，多了一個參數輸入，可用來調整轉動速度
    #因四輪驅動關係，會使車輛似逆時針轉動，固取counterclockwise
    def rotateCounterclockwise(self, speed):
        self.motorFR1.ChangeDutyCycle(speed)
        self.motorFR2.ChangeDutyCycle(0)
        self.motorFL1.ChangeDutyCycle(0)
        self.motorFL2.ChangeDutyCycle(speed)
        self.motorBR1.ChangeDutyCycle(speed)
        self.motorBR2.ChangeDutyCycle(0)
        self.motorBL1.ChangeDutyCycle(0)
        self.motorBL2.ChangeDutyCycle(speed)

    #可自訂左右輪轉速
    #逆轉直接帶入負號，於函式內判斷後再轉正即可
    def setSpeed(self, lSpeed, rSpeed):
        if lSpeed < 0:
            self.motorFL1.ChangeDutyCycle(0)
            self.motorFL2.ChangeDutyCycle(-lSpeed)
            self.motorBL1.ChangeDutyCycle(0)
            self.motorBL2.ChangeDutyCycle(-lSpeed)
        elif lSpeed >= 0:
            self.motorFL1.ChangeDutyCycle(lSpeed)
            self.motorFL2.ChangeDutyCycle(0)
            self.motorBL1.ChangeDutyCycle(lSpeed)
            self.motorBL2.ChangeDutyCycle(0)
        
        if rSpeed < 0:
            self.motorFR1.ChangeDutyCycle(0)
            self.motorFR2.ChangeDutyCycle(-rSpeed)
            self.motorBR1.ChangeDutyCycle(0)
            self.motorBR2.ChangeDutyCycle(-rSpeed)
        elif rSpeed >= 0:
            self.motorFR1.ChangeDutyCycle(rSpeed)
            self.motorFR2.ChangeDutyCycle(0)
            self.motorBR1.ChangeDutyCycle(rSpeed)
            self.motorBR2.ChangeDutyCycle(0)

    # 當程式結束時，停止各PWN輸出及清除GPIO使用
    def __delete__(self):
        self.motorFR1.stop()
        self.motorFR2.stop()
        self.motorFL1.stop()
        self.motorFL2.stop()
        self.motorBR1.stop()
        self.motorBR2.stop()
        self.motorBL1.stop()
        self.motorBL2.stop()
        GPIO.cleanup()