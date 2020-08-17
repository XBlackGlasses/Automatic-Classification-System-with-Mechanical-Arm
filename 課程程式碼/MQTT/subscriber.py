# import MQTT需要的函式庫
import paho.mqtt.client as mqtt

mqtt_broker = '127.0.0.1'
mqtt_port = 1883
mqtt_in_topic = 'myTopic'

# 當連接成功時，所觸發function
# 可在連線成功後，進行Topic的訂閱
def on_connect(client, userData, flags, rc):
    print("connected with result code " + str(rc))
    #訂閱Topic
    client.subscribe(mqtt_in_topic)

# 當接收到訊息時，所觸發function
# 基本上最複雜的部份都在這邊
# 其他的函式都只要設定好就行了
def on_message(client, userData, msg):
    msgs = msg.payload.decode("utf8")
    print(msgs)

if __name__ == '__main__':
    # 建立MQTT的連接物件
    client = mqtt.Client()

    # 設定物間的連接事件會觸發哪一個function
    client.on_connect = on_connect

    # 設定物件當接收到訊息事件會觸發哪一個function
    client.on_message = on_message

    # 與broker建立連線，輸入IP、PORT及Keepalive
    # Keepalive為確保連線，固定時間向boroker進行訪問
    # 這邊以每60秒1次為例
    client.connect(mqtt_broker, mqtt_port, 60)

    # 使client保持連線
    # 若斷線會持續嘗試連線
    client.loop_forever()

