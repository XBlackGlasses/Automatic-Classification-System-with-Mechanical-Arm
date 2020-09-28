# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 17:20:52 2020

@author: user
"""
import pyrealsense2 as rs
import numpy as np
import cv2
#import move,time
import time
import paho.mqtt.client as mqtt
import json
import os
client = None
MQTT_SERVER = '10.10.10.165'
MQTT_PORT = 1883  
MQTT_ALIVE = 60 
def arm_distance():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
 
    # Start streaming
    pipeline.start(config)
    align_to = rs.stream.color
    align = rs.align(align_to)
    
    net = cv2.dnn.readNet("label_final.weights", "label.cfg")
    #print(cv2.dnn.DNN_TARGET_CUDA)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    classes = []
    with open("label.names", "r") as f:
         classes = [line.strip() for line in f.readlines()]    # line.strip()用再刪除字符，()內為空白默認刪除空白符 
    layer_names = net.getLayerNames()   #得到layer名稱
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]  #獲取網路輸出層訊息(所有輸出層名子)，設定forward propogation
                                                            #yolo在每個sacle都有輸出，output_layers是每个scale的名字信息，供net.forward使用          
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    while (True):  
        
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()     # 他會獲取一幀之後暫停串流，然後直到獲取下一幀
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
           continue
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
 
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)
        
        height, width, channels = color_image.shape
        # Detecting objects 0.00392
        resized=cv2.resize(color_image,(224,224))
        blob = cv2.dnn.blobFromImage(resized, 1/255, (224, 224), (0, 0, 0), True, crop=False) #對影像進行預先處理，調整解析度
                #cv2.dnn.blobFromImage(image, scalefactor, size, mean, swapRB, crop, ddepth)
                #scalefactor:圖像各channel數值的縮放比例  ; swapRB:交換RB channel，默認為False.  tensorflow模型要設true
                #crop:圖像裁剪,默認為False.當值為True時，先按比例縮放，然後從中心裁剪成size尺寸
        
        # run model
        net.setInput(blob)      
        outs = net.forward(output_layers)   #得到各個層的輸出、各個檢視框等信息，是二维結構。 
                                            #第0維表示哪個輸出層，第1維表示各個檢視框
        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:       #各輸出層
            for detection in out:   #各個框
                #前4個表示檢測到的矩形框資訊，第5位表示背景，從第6位開始代表檢測到的目標置信度及目標屬於哪個類
                scores = detection[5:]      #取得各類別的confidence
                class_id = np.argmax(scores)    #取得最高confidence的id
                confidence = scores[class_id]   
                if confidence > 0.5:
                    # Object detected
                    #將邊框放回圖片尺寸
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
                    #應用非最大值抑制 
                    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                    font = cv2.FONT_HERSHEY_PLAIN
                    
        list = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                #Subscribe
                #print((x+x+w)/2,label)
                
                cv2.rectangle(color_image, (x, y), (x + w, y + h), color, 2)
                
                depth = str(np.round(depth_frame.get_distance(int(x+w/2), int(y+h/2))*100, 4))  #該方法返回x的小數點四捨五入到n個數字
                depth1 = str(np.round(depth_frame.get_distance(int(320), int(300))*100, 4))
                list.append({'obj':label,'depth':depth})
                cv2.putText(color_image, label+":"+depth, (x, y-5), cv2.FONT_HERSHEY_PLAIN , 2, color, 2)   ## cv.FONT_HERSHEY_SIMPLEX字體、0.5字體大小、粗細2px
        print(list)
        color_image = cv2.circle(color_image,(320,300),1,(0,0,255),-1)  #cv2.circle(影像, 圓心座標, 半徑, 顏色, 線條寬度)
        
        images = color_image#np.vstack((color_image, depth_colormap))
 
        # Show images
        
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        #depth = (float(list[0]['depth'])+ float(list[1]['depth']))/2
        key = cv2.waitKey(1)
        if len(list)>=2:
            if key & 0xFF == ord('q') or key == 27:
                depth = (float(list[0]['depth'])+ float(list[1]['depth']))/2
                with open("./arm_distance/arm_distance.txt",'w+') as f:
                    f.write(str(depth))
                    f.close()
                    cv2.destroyAllWindows()
                    break
        
        #if key & 0xFF == ord('q') or key == 27:
            #cv2.destroyAllWindows()
           # break
        #time.sleep(0.1)
    return depth
Text = ''
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #client.subscribe("position")
    client.subscribe("speech")
    client.subscribe("finish")
    client.subscribe("end")
def on_message(client, userdata, msg):
    if msg.topic=='finish':
        Text = msg.payload.decode('utf8')   
        print(Text)
        #client.disconnect()
        detect(json.loads(Text))
  #if msg.topic=='end':
      
def test(Text):
    global client
    client = mqtt.Client()  
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE) 
    detect(Text)
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
def myKey(e):
    return e['locx']

def detect(Text):
    global client
    # Configure depth and color strreams
    print(Text[0]['finish'])
    #相機定位  => arm_distance  
    file = "./arm_distance/arm_distance.txt"
    if os.path.exists(file):
        with open(file,'r') as f:
            depth=float(f.read())
            f.close()
    else:
        depth = arm_distance()
    
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
 
    # Start streaming
    pipeline.start(config)
    align_to = rs.stream.color
    align = rs.align(align_to)
    
    net = cv2.dnn.readNet("objv3.weights", "obj.cfg")
    #print(cv2.dnn.DNN_TARGET_CUDA)
    #net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    classes = []
    with open("classes.names", "r") as f:
         classes = [line.strip() for line in f.readlines()]    # line.strip()用再刪除字符，()內為空白默認刪除空白符 
    layer_names = net.getLayerNames()   #得到layer名稱
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]  #getUnconnectedOutLayer() 獲得輸出層的索引
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

#http://192.168.43.235:8090/?action=stream')
     
    MQTT_TOPIC1 = "position"
    times = time.time()
    client = mqtt.Client()  
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE) 
    on_public = False
    imgid=1304
    
    sz = (640,480)
    fps = 10
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('./realsense.mp4', fourcc,fps,sz)
    while (True):  
        '''繼電器控制'''
        
        client.publish('carrier', '0', qos=1)
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
           continue        
        
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
 
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)
        
        #影片
        
        ###
        height, width, channels = color_image.shape
        # Detecting objects 0.00392
        resized=cv2.resize(color_image,(224,224))
        blob = cv2.dnn.blobFromImage(resized, 1/255, (224, 224), (0, 0, 0), True, crop=False) #對影像進行預先處理，調整解析度
        net.setInput(blob)      #blob = binary large object
        outs = net.forward(output_layers)
        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        indexes=[]
        for out in outs:
            for detection in out:
                scores = detection[5:]  #前4個(a[0~3])表示檢測到的矩形框資訊，第5位(a[4])表示背景，從第6位(a[5])開始代表檢測到的目標置信度及目標屬於哪個類
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

                    
        list = []
        #print(indexes)
        obj_depth=40
        '''繼電器控制'''
        t=0
        
        if len(boxes)>0:
            for i in boxes:
                if i[0]+i[2]/2 > t:
                    t = i[0]+i[2]/2
            print(t)
            if t > 430:
                client.publish('carrier', '1', qos=1)
                print("stop")
        
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                #print(len(colors))
                color = colors[class_ids[i]]
                #Subscribe
                #print((x+x+w)/2,label)
                
                cv2.rectangle(color_image, (x, y), (x + w, y + h), color, 2)
                
                depth1 = str(np.round(depth_frame.get_distance(int(x+w/2), int(y+h/2))*100,4))                
                #print(depth1)
                x_len=((x+w/2)-320)*float(depth1)/600
                #list.append({'obj':label,'locx':x+w/2,'locy':y+h/2,'depth':depth})
                
                obj_height = (0.07 + (float(depth1)-obj_depth)/1000) * h
                if label!='label':
                    list.append({'obj':label,'locx':(x+w/2),'x_len':round(x_len,1)+1,'height':round(obj_height,2),'depth':round((float(depth)-float(depth1)),3)+1})
                cv2.putText(color_image, label+":"+str(round(float(depth1),3)), (x, y-5), cv2.FONT_HERSHEY_PLAIN , 2, color, 2)
        ###
        
        ###
        #text_depth = "depth value of point (320,240) is "+str(np.round(depth_frame.get_distance(320, 300)*100,4))+"cm(s)"
        ###
        
        color_image = cv2.circle(color_image,(320,300),1,(0,0,255),-1) 
        
        #color_image=cv2.putText(color_image, text_depth, (10,20),  cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1, cv2.LINE_AA)        
        images = color_image#np.vstack((color_image, depth_colormap))
        #video.write(images)
        # Show images
        
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        """for a in list:
            if a['obj']=='label':
                list.remove(a)"""
        list.sort(reverse=True,key=myKey)
        
        print(json.dumps(list))
        #MQTT
        
        if on_public == False:
            if t>430 : #list 不為空
                #global client
                client.publish(MQTT_TOPIC1, json.dumps(list), qos=1)
                on_public = True
                cv2.destroyAllWindows()
                #break
                client.on_connect = on_connect
                client.on_message = on_message
                client.loop_forever() 
        elif Text[0]['finish']=="Finish":
            on_public = False
        #time.sleep(1)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('a'):
            cv2.imwrite(str(imgid)+'.jpg',images)
            print("save image "+str(imgid)+".jpg")
            imgid+=1
        if key & 0xFF == ord('q') or key == 27:
            client.publish(MQTT_TOPIC1, json.dumps(list), qos=1)
            cv2.destroyAllWindows()
            #video.release()
            client.publish('end', json.dumps([{'end':'end'}]), qos=1)
            break
        #time.sleep(0.1)
    
if __name__ == '__main__':
    """直接給予物件名稱"""
    #detect('bottle')
    #detect(".")
    """MQTT傳遞物件信息"""
    
    client = mqtt.Client()  
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
    client.on_connect = on_connect
    """
    client.on_message = on_message
    client.publish('finish',json.dumps([{"finish":"finish"}]),qos=1)
    client.loop_forever() """
    #test([{"finish":123}])
    detect([{"finish":123}])
   
    
