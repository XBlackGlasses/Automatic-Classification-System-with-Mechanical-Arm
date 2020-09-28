# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 17:58:28 2020

@author: guava
"""

import cv2
import numpy as np
import math
import json
import time
import paho.mqtt.client as mqtt
client = None
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #client.subscribe("position")
    client.subscribe("fix")

def on_message(client, userdata, msg):
  if msg.topic=='fix':
    Text = msg.payload.decode('utf8')   
    Text=json.loads(Text)
    print(Text)
    if Text[0]['fix']=='start':
        main()
def myKey(e):
    return e[1]
def main():
  on_public=True
  catch=False
  catchTimes=0
  while(on_public):   
    global client
    times = time.time()
    while(not catch and on_public):
        if catchTimes==3:
            client.publish("fix_angle", json.dumps([{"angle":0}]), qos=1)
            print("not catch")
            on_public=False
            break
        while (True):   
            ip1 = 'http://10.10.10.182:8090/?action=stream'
            #ip2 = 'http://192.168.43.235:8090/?action=stream'
            cap = cv2.VideoCapture(ip1)    
            ret ,frame = cap.read()
            #cv2.imshow('frame', frame)  #
            now = time.time()
            if now - times > 0.3:
                cv2.imwrite('capture.jpg',frame)
                break 
        
        cap.release()
        #cv2.destroyAllWindows()
        img = cv2.imread('capture.jpg')
        img = cv2.resize(img,(640,480))
        height, width, channels = img.shape
        net = cv2.dnn.readNet("objv3.weights", "obj.cfg")
        classes = []
        print(1)
        with open("obj.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        print(2)
        #**************************
    
    
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id) 
                    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                    font = cv2.FONT_HERSHEY_PLAIN
        if len(boxes) <= 0:
            catchTimes+=1
            break
                #************************
        print(2.1)
        boxes.sort(key=myKey)
        #for i in range(len(boxes)):
            #if i in indexes:
        x, y, w, h = boxes[0]
        print(boxes)
        mask = cv2.imread('mask.jpg')
        mask = cv2.resize(mask,(640,480))

        img = cv2.absdiff(mask,img) #計算並得出兩張影像的差異圖形
        
        deltaX=40
        deltaY=20
        if x<40:
            if x<0:
                x=0
            deltaX=x
        if y<20:
            if y<0:
                y=0
            deltaY=y
    
        
        heightImg=y+h+deltaY
        if heightImg > 480:
            heightImg = 480
        widthImg=x+w+deltaX
        if widthImg > 640:
            widthImg = 640
        img = img[y-deltaY:heightImg, x-deltaX:widthImg]
    
        print(3)
        
       
        
        """img1 = cv2.imread('4.jpg')
        img1 = cv2.resize(img1,(640,480))
        mask = cv2.imread('mask.jpg')
        mask = cv2.resize(mask,(640,480))
        img = cv2.absdiff(mask,img)"""

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
        #梯度轉換
        # subtract the y-gradient from the x-gradient

        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)    #需要用convertScaleAbs()函數將其轉回原來的uint8形式，否則將無法顯示圖像，
        #cv2.imwrite('g',gradient)
        #模糊後填入空白

        blurred = cv2.blur(gradient, (9, 9))
        _, thresh = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  #先膨脹，後腐蝕，去黑噪點，淺色成分有利

        closed = cv2.erode(closed, None, iterations=4)      # 腐蝕：在窗中，只要含有０，則窗內全變為０，可以去淺色噪點
        closed = cv2.dilate(closed, None, iterations=4)     #膨脹：在窗中，只要含有１，則窗內全變為１，可以增加淺色成分   
    

        cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = sorted(cnts, key=cv2.contourArea, reverse=True)
        list=[]
        for t in c :
            # compute the rotated bounding box of the largest contour
            rect = cv2.minAreaRect(t)
            box = np.int0(cv2.boxPoints(rect))

            # draw a bounding box arounded the detected barcode and display the image
            cv2.drawContours(img, [box], -1, (0, 255, 0), 3)
            cv2.imwrite('save.jpg',img)
            for i in range(0,len(box)):
                if i % 4 !=0:
                    list.append(box[i])
        angle=[]
        for i in range(0,len(list),3) :
            x1,y1 = list[i]
            x2,y2 = list[i+1]
            x3,y3 = list[i+2]
            length1=math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
            length1=round(length1,2)
            length2=math.sqrt(math.pow(x2-x3,2)+math.pow(y2-y3,2))
            length2=round(length2,2)
            print("({x1},{y1}),({x2},{y2}),({x3},{y3})".format(x1=x1,y1=y1,x2=x2,y2=y2,x3=x3,y3=y3))
            print(" 1->2:{length1}, 2->3:{length2}\n".format(length1=length1,length2=length2))
            if x2-x1==0:
                if length1>=length2:
                    angle.append(90)
                else:
                    angle.append(0)
            else:
                m = math.atan(-1*(y2-y1)/(x2-x1))*180/math.pi
                if length1>=length2:
                    angle.append(round(m,2))
                else:
                    angle.append(round(m-90,2))
                    #print(math.atan(m*-1)*180/math.pi)
                    #angle.append(round(math.atan(-1*(y2-y1)/(x2-x1))*180/math.pi,2))
            #if i == len(list)-1:
        #break
        print(angle[0])
        fix_angle=0          
        if angle[0]>0:
            fix_angle = round(90-angle[0],2)
        elif angle[0]<0:
            fix_angle = round(-1*(90+angle[0]),2)
        print('fix:',fix_angle)
    
        MQTT_TOPIC1 = "fix_angle"
        #print ( MQTT_TOPIC1 
        cv2.imshow("Image", img)
        if on_public :    
            client.publish(MQTT_TOPIC1, json.dumps([{"angle":fix_angle}]), qos=1)      
            on_public = False
        #cv2.imwrite("contoursImage.jpg", img1)   
            cv2.destroyAllWindows()

    
if __name__=='__main__':
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("10.10.10.182", 1883, 60)
    client.loop_forever()
    
    #main()
    