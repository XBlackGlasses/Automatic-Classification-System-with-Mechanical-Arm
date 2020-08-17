import paho.mqtt.client as mqtt
import threading 
import time
# import MQTT的publish函式
import paho.mqtt.publish as publish


mqtt_broker = '127.0.0.1'
mqtt_port = 1883
mqtt_topic = 'myTopic'

def on_connect(client, userData, flags, rc):
    print("Connect with result code " + str(rc))
    client.subscribe('anotherTopic')
    publish = threading.Thread(target=publish_function)
    publish.start()

def publish_function():
    counter = 1
    while( True ):
        msg = 'Num is ' + str(counter)
        # 作法二：使用publish函式發布訊息
        publish.signal(mqtt_topic, msg, qos=1, hostname=mqtt_broker)
        counter = counter + 1
        time.sleep(2)

def on_message(client, userData, msg):
    msgs = msg.payload.decode("utf8")
    print(msgs)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()