import paho.mqtt.client as mqtt
import threading
import time

mqtt_broker = '10.10.10.163'
mqtt_port = 1883
mqtt_in_topic = 'myTopic'

#連線成功時觸發的function
def on_connect(client, userData, flag, rc):
    print("connect with result code "+ str(rc))
    #訂閱
    client.subscribe(mqtt_in_topic)

#接收到訊息時觸發的finction
def on_message(client, userData, msg):
    msgs = msg.payload.decode("utf8")
    print(msgs)
    
if __name__ == '__main__':
    #設定連線
    #初始化地端程式
    client = mqtt.Client()
    
    #設定連線時的動作 
    client.on_connect = on_connect
   
    #設定接收訊息的動作
    client.on_message = on_message
  
    #設定登入帳號密碼
    client.username_pw_set("try","1111")
    
    #設定連線資訊(IP,Port,連線時間)
    client.connect(mqtt_broker, mqtt_port, 60)
    
    #開始連線,執行設定的動作和處理重新連線問題
    #也可以手動使用其他loop函式進行
    client.loop_forever()
    
    
    