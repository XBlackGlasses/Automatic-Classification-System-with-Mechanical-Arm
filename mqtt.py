# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:27:05 2020

@author: USER
"""
import paho.mqtt.client as mqtt
import json
import time
if __name__ == '__main__':
    MQTT_SERVER = '10.10.10.182'
    MQTT_PORT = 1883  
    MQTT_ALIVE = 60  
    MQTT_TOPIC1 = "finish"
    MQTT_TOPIC2 = "fix"
    MQTT_TOPIC3 = "carrier"
    MQTT_TOPIC4 = "position"
    data1 = json.dumps([{"finish":"finish"}])
    data2 = json.dumps([{"fix":"start"}])
    data3 = '0'
    data4 = json.dumps([{"obj": "tin_aluminum_can", "locx": 255.0, "x_len": -6.6, "height": 10.6, "depth": 30.2},{"obj": "plastic", "locx": 255.0, "x_len": -6.6, "height": 10.6, "depth": 30.2}])
    mqtt_client = mqtt.Client() 
    #print ( MQTT_TOPIC1 )
    mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
    mqtt_client.publish(MQTT_TOPIC1, data1, qos=1)
    '''while (1):
        mqtt_client.publish(MQTT_TOPIC3, "1", qos=1)
        print(1)
        time.sleep(5)
        
        mqtt_client.publish(MQTT_TOPIC3, "0", qos=1)
        print(0)
        time.sleep(5)'''
        