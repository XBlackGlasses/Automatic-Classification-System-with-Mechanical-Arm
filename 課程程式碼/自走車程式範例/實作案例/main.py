# 將馬達驅動器class引入
from motor_controller import Motor
# import 監聽鍵盤事件的函式庫
from pynput import kerboard

# 建立馬達控制物件
myMotor = Motor(38, 40, 35, 36, 32, 33, 29, 31)

# 定義預設速度
speed = 50

# 鍵盤按下時的觸發事件，按下時只會執行一次
def on_press(key):
    try:
        # 將鍵盤輸入格式為字元
        a = format(key.char)

        # wasd分別負責的馬達設定
        if a == 'w':    # 前進
            # 直接調用先前所設定完成的class函式
            #由8行簡化為1行
            myMotor.forward(speed)
        elif a == 'a':  # 左轉
            myMotor.rotateCounterclockwise(speed)
        elif a == 's':  #後退
            myMotor.backword(speed)
        elif a =='d':   #右轉
            myMotor.rotateClockwise(speed)
    #Ctrl + C 強制退出的例外
    except AttributeError:
        print('special key {0} press'.format(key))

# 當放開按鍵時的事件

def on_release(key):
    #放開時需要將自走車停下，所以需要加上stop()
    myMotor.stop()
    if key == keyboard.Key.esc:
        #Stop listner
        return False

# 主程式僅有這幾行 ,
# 設定鍵盤監聽事件。
with keyboard.Listner(
        on_press=on_press,
        on_release=on_release) as listner:
    listner.join()