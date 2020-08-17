import time 
import paho.mqtt.publish as publish

counter = 1
while(True):
    msg = 'Num is ' + str(counter)
    #作法三：使用publish函式發布訊息
    publish.single('myTopic', msg, qos=1, hostname='127.0.0.1')
    counter = counter + 1
    time.sleep(2)