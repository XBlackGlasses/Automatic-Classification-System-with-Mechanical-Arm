#import raspberry的IO控制函式庫
import RPi.GPIO as GPIO
import time

# 定義馬達驅動器所連接的腳位
frontR1_pin = 38
frontR2_pin = 40
frontL1_pin = 35
frontL2_pin = 36
backR1_pin = 32
backR2_pin = 33
backL1_pin = 29
backL2_pin = 31

# 定義腳位模式，分為GPIO.BOARD及GPIO.BCM
# GPIO.BOARD 是使用電路板上接腳的號碼
# GPIO.BCM是使用GPIO後面的號碼
GPIO.setmode(GPIO.BOARD)

#設定各腳位為輸出腳位
GPIO.setup(frontR1_pin, GPIO.OUT)
GPIO.setup(frontR2_pin, GPIO.OUT)
GPIO.setup(frontL1_pin, GPIO.OUT)
GPIO.setup(frontL2_pin, GPIO.OUT)
GPIO.setup(backR1_pin, GPIO.OUT)
GPIO.setup(backR2_pin, GPIO.OUT)
GPIO.setup(backL1_pin, GPIO.OUT)
GPIO.setup(backL2_pin, GPIO.OUT)

# 設定各腳位預設PWN頻率，並將各腳位物件使用變數儲存
motorFR1 = GPIO.PWN(frontR1_pin, 500)
motorFR2 = GPIO.PWN(frontR2_pin, 500)
motorFL1 = GPIO.PWN(frontL1_pin, 500)
motorFL2 = GPIO.PWN(frontL2_pin, 500)
motorBR1 = GPIO.PWN(backR1_pin, 500)
motorBR2 = GPIO.PWN(backR2_pin, 500)
motorBL1 = GPIO.PWN(backL1_pin, 500)
motorBL2 = GPIO.PWN(backL2_pin, 500)

# 啟動各腳位輸出(0~100),起始0為停止馬達
motorFR1.start(0)
motorFR2.start(0)
motorFL1.start(0)
motorFL2.start(0)
motorBR1.start(0)
motorBR2.start(0)
motorBL1.start(0)
motorBL2.start(0)

# 全速運行
motorFR1.ChangeDutyCycle(100)
motorFR2.ChangeDutyCycle(0)
motorFL1.ChangeDutyCycle(100)
motorFL2.ChangeDutyCycle(0)
motorBR1.ChangeDutyCycle(100)
motorBR2.ChangeDutyCycle(0)
motorBL1.ChangeDutyCycle(100)
motorBL2.ChangeDutyCycle(0)

#使馬達轉動5秒
time.sleep(5)

#停止
motorFR1.ChangeDutyCycle(0)
motorFR2.ChangeDutyCycle(0)
motorFL1.ChangeDutyCycle(0)
motorFL2.ChangeDutyCycle(0)
motorBR1.ChangeDutyCycle(0)
motorBR2.ChangeDutyCycle(0)
motorBL1.ChangeDutyCycle(0)
motorBL2.ChangeDutyCycle(0)