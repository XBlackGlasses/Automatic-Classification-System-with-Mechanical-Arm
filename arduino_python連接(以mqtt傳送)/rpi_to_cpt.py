import paho.mqtt.client as mqtt
import serial
import sys

Broker = '10.10.10.165'
Topic2 = 'To_rpi'
Topic = 'from_rpi'
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# 當地端程式連線伺服器得到回應時要做的動作
try:
    def on_connect(client, userdata, flags, rc):
        print("connected with result code " + str(rc))
        #將訂閱主題寫在on_connect中
        #失去連線或重新連線時，地端程式會重新訂閱
        #訂閱from_rpi => 接收來自rpi的訊息
        client.subscribe(Topic2)
        
    #收到訊息時要做的動作    
    def on_message(client, userdata, msg):
        msgs = msg.payload.decode("utf8")
        if msgs == "g":
            ser.write(b's\n')   # # 訊息必須是位元組類型
            response = ser.readall().decode("utf8")
            print("接收到的數值為:"+response)
            client.publish(Topic, response)
        elif msgs == "n":
            print("結束連線")
            ser.close()
            client.disconnect()
            sys.exit()
    
    # 連線設定
    # 初始化地端資料
    client = mqtt.Client()
    
    client.on_connect = on_connect
    
    client.on_message = on_message
    
    client.connect(Broker, 1883, 60)
    
    client.loop_forever()
except:
    ser.close();
    
    
    
