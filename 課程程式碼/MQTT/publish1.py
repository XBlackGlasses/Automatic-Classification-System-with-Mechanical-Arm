import paho.mqtt.client as mqtt
import threading 
import time

mqtt_broker = '127.0.0.1'
mqtt_port = 1883
mqtt_topic = 'myTopic'

def on_connect(client, userData, flags, rc):
    print("Connect with result code " + str(rc))
    client.subscribe('anotherTopic')

    # 若監聽跟發布訊息需要在同程式，
    # 則需要開Thread來負責發布的功能，
    # 因為client.loop_forever()的緣故，
    # 會使程式完全卡住在client.loop_forever()這行
    publish = threading.Thread(target=publish_function, args=[client])
    publish.start()

def publish_function(mqttClient):
    counter = 1
    while( True ):
        msg = 'Num is ' + str(counter)
        # 作法一：使用原client物件發布訊息
        mqttClient.publish(mqtt_topic, msg)
        counter = counter + 1
        time.sleep(2)

def on_message(client, userData, msg):
    msgs = msg.payload.decode("utf8")
    print(msgs)

if __name__ == '__main__':
    client = mqtt.client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()