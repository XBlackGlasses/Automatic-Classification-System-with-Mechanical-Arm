import paho.mqtt.client as mqtt
import json

# 當地端程式連線伺服器得到回應時要做的動作
def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    
    #將訂閱主題寫在on_connect中
    #失去連線或重新連線時，地端程式會重新訂閱
    client.subscribe("HeightWeight")
    
# 接收到伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉utf-8才看得懂中文
    print(msg.topic + " " + msg.payload.decode('utf-8'))
    bmi = BMI(msg.payload.decode('utf-8'))
    
    # 發布BMI主題資料
    client.publish("BMI", "計算後的BMI為 : " + str(bmi))
    
def BMI(data):
    data = json.loads(data)
    height = data["Height"]
    weight = data["Weight"]
    
    bmi = weight / ((height/100)**2)
    return bmi

# 連線設定
# 初始化地端資料
client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.connect("10.10.10.163", 1883, 60)

client.loop_forever()






