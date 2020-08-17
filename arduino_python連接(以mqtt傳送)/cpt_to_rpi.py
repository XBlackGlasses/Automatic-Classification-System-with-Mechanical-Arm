import paho.mqtt.client as mqtt
import threading
import sys
import time
Broker = '10.10.10.165'
Topic2 = 'To_rpi'
Topic = 'from_rpi'

# 當地端程式連線伺服器得到回應時要做的動作
def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    #將訂閱主題寫在on_connect中
    #失去連線或重新連線時，地端程式會重新訂閱
    #訂閱from_rpi => 接收來自rpi的訊息
    client.subscribe(Topic)
    
    publish = threading.Thread(target = publish_function, args = [client])
    publish.start()
    
def publish_function(client):
    print(1)
    while(True):
        ipt = input("輸入要執行的動作，g = 獲得CO數值; n = 離開\n")
        if ipt == "g":
            client.publish(Topic2, ipt)
        elif ipt == "n":
            client.publish(Topic2, ipt)
            print("離開連線")
            client.disconnect()
            sys.exit()
        else:
            print("不正確指令!")
        time.sleep(3)
#收到訊息時要做的動作    
def on_message(client, userdata, msg):
    # 轉utf-8才看得懂中文
    msgs = msg.payload.decode("utf8")
    print(msgs)
    num = int(msgs)
    print(num)
    if num > 350:
        print("Warning!! CO超標，目前為:" + msgs)
    else:
        print("CO數值:"+ msgs)
        

# 連線設定
# 初始化地端資料
client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.connect(Broker, 1883, 60)

client.loop_forever()
