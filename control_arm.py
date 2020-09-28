# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 15:08:01 2020

@author: USER
"""
###

import sys
import os
import time
import threading
import json
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from kortex_api.autogen.client_stubs.BaseCyclicClientRpc import BaseCyclicClient

from kortex_api.autogen.messages import Base_pb2, BaseCyclic_pb2, Common_pb2

# Position of the protection zone (in meters)
PROTECTION_ZONE_POS =  [0.33, -0.35, -0.35]

# Size of the protection zone (in meters)
PROTECTION_ZONE_DIMENSIONS = [1.21, 0.78, 0.61]

# Theta values of the protection zone movement (in degrees)
PROTECTION_ZONE_MOVEMENT_THETAS = [0, 0, 0]

# Waiting time between actions (in milliseconds)
ACTION_WAITING_TIME = 1
# Maximum allowed waiting time during actions (in seconds)
TIMEOUT_DURATION = 20
import paho.mqtt.client as mqtt
Text = ''
client = None
x = None
y = None
z = None
theta_x = None
theta_y = None
theta_z = None 
def on_connect(client, userdata, flags, rc):
    #global client
    print("Connected with result code "+str(rc))
    client.subscribe("position")
    client.subscribe("fix_angle")
def on_message(client, userdata, msg):
  if msg.topic=='position':
    Text = msg.payload.decode('utf8')   
    print(type(json.loads(Text)))
    main(json.loads(Text),1)
  if msg.topic=='fix_angle':
    Text = msg.payload.decode('utf8')
    angle = json.loads(Text)[0]['angle']
    print(angle)
    main(angle,2)
    
# Create closure to set an event after an END or an ABORT
def create_protection_zone(base):

    zone = Base_pb2.ProtectionZone()

    zone.name = "Protection Zone"
    zone.is_enabled = True
    shape = zone.shape
    shape.shape_type = Base_pb2.RECTANGULAR_PRISM

    point = shape.origin
    point.x = PROTECTION_ZONE_POS[0]
    point.y = PROTECTION_ZONE_POS[1]
    point.z = PROTECTION_ZONE_POS[2]
    shape.dimensions.append(PROTECTION_ZONE_DIMENSIONS[0])
    shape.dimensions.append(PROTECTION_ZONE_DIMENSIONS[1])
    shape.dimensions.append(PROTECTION_ZONE_DIMENSIONS[2])

    shape.orientation.row1.column1 = 1.0
    shape.orientation.row2.column2 = 1.0
    shape.orientation.row3.column3 = 1.0

    return base.CreateProtectionZone(zone)
def create_protection_zone2(base):

    zone = Base_pb2.ProtectionZone()

    zone.name = "Protection Zone2"
    zone.is_enabled = True
    shape = zone.shape
    shape.shape_type = Base_pb2.RECTANGULAR_PRISM

    point = shape.origin
    point.x = PROTECTION_ZONE_POS[0]
    point.y = PROTECTION_ZONE_POS[1]
    point.z = PROTECTION_ZONE_POS[2]+0.65
    shape.dimensions.append(PROTECTION_ZONE_DIMENSIONS[0]-0.8)
    shape.dimensions.append(PROTECTION_ZONE_DIMENSIONS[1]-0.3)
    shape.dimensions.append(PROTECTION_ZONE_DIMENSIONS[2]-0.3)

    shape.orientation.row1.column1 = 1.0
    shape.orientation.row2.column2 = 1.0
    shape.orientation.row3.column3 = 1.0

    return base.CreateProtectionZone(zone)
def check_for_end_or_abort(e):
    """Return a closure checking for END or ABORT notifications
    Arguments:
    e -- event to signal when the action is completed
        (will be set when an END or ABORT occurs)
    """
    def check(notification, e = e):
        print("EVENT : " + \
              Base_pb2.ActionEvent.Name(notification.action_event))
        if notification.action_event == Base_pb2.ACTION_END \
        or notification.action_event == Base_pb2.ACTION_ABORT:
            e.set()
    return check
 
def example_move_to_home_position(base,name):
    # Make sure the arm is in Single Level Servoing mode
    base_servo_mode = Base_pb2.ServoingModeInformation()
    base_servo_mode.servoing_mode = Base_pb2.SINGLE_LEVEL_SERVOING
    base.SetServoingMode(base_servo_mode)
    
    # Move arm to ready position
    print("Moving the arm to a safe position")
    action_type = Base_pb2.RequestedActionType()
    action_type.action_type = Base_pb2.REACH_JOINT_ANGLES
    action_list = base.ReadAllActions(action_type)
    action_handle = None
    for action in action_list.action_list:
        if action.name == name:
            action_handle = action.handle

    if action_handle == None:
        print("Can't reach safe position. Exiting")
        return False

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    base.ExecuteActionFromReference(action_handle)
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Safe position reached")
    else:
        print("Timeout on action notification wait")
    return finished
def example_angular_trajectory_movement(base):
    
    constrained_joint_angles = Base_pb2.ConstrainedJointAngles()

    actuator_count = base.GetActuatorCount()

    # Place arm straight up
    for joint_id in range(actuator_count.count):
        joint_angle = constrained_joint_angles.joint_angles.joint_angles.add()
        joint_angle.joint_identifier = joint_id
        joint_angle.value = 0

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )
    
    base.PlayJointTrajectory(constrained_joint_angles)


    print("Waiting for movement to finish ...")
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Joint angles reached")
    else:
        print("Timeout on action notification wait")
    return finished
def cartesian_position(base, base_cyclic):
    constrained_position = Base_pb2.ConstrainedPosition()
    constrained_position  = constrained_position.target_position
    constrained_position.x = 0.399
    constrained_position.y = 0.006
    constrained_position.z = -0.162
    
    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )
    print("Reaching cartesian pose...")
    base.PlayCartesianTrajectory(constrained_position)

    print("Waiting for movement to finish ...")
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Angular movement completed")
    else:
        print("Timeout on action notification wait")
    return finished
def example_cartesian_trajectory_movement(base, base_cyclic,X,Y,Z,theta_x,theta_y,theta_z):
    #Speed

    constrained_pose = Base_pb2.ConstrainedPose()
    constrained_pose.constraint.speed.translation = 10
    constrained_pose.constraint.speed.orientation = 100  # deg/s
    feedback = base_cyclic.RefreshFeedback()
   
    cartesian_pose = constrained_pose.target_pose
    cartesian_pose.x = X        # (meters)
    cartesian_pose.y = Y # (meters)
    cartesian_pose.z = Z  # (meters)
    cartesian_pose.theta_x = theta_x # (degrees)
    cartesian_pose.theta_y = theta_y# (degrees)
    cartesian_pose.theta_z = theta_z#feedback.base.tool_pose_theta_z # (degrees)

    e = threading.Event()
    notification_handle = base.OnNotificationActionTopic(
        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    print("Reaching cartesian pose...")
    base.PlayCartesianTrajectory(constrained_pose)

    print("Waiting for movement to finish ...")
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Angular movement completed")
    else:
        print("Timeout on action notification wait")
    return finished

def grab_gripper(base,val):
       
        print("Performing gripper test in position...")
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()
        #print(position)
        position = 0
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 1
        while position < val:
            finger.value = position
            base.SendGripperCommand(gripper_command)
            position += 0.1
            time.sleep(0.2)
def release_gripper(base,val):
        print("Performing gripper test in position...")
        gripper_command = Base_pb2.GripperCommand()
        finger = gripper_command.gripper.finger.add()
        position = 1
        gripper_command.mode = Base_pb2.GRIPPER_POSITION
        finger.finger_identifier = 0
        while position > val:
            finger.value = position
            base.SendGripperCommand(gripper_command)
            position -= 0.15
            time.sleep(0.2)
def target_position(x,y,z,theta_x,theta_y,theta_z,name):
    if name == "plastic":
        return (-0.52,0.22,0.30,-90,-180,90,"Home2")
    if name ==  "drink_carton":
        return (-0.52,-0.22,0.30,-90,-180,90,"Home3")
    if name == "tin_aluminum_can":
        return (-0.58,-0.42,0.3,-90,-180,90,"Home3")
    if name == "building_block":
        return (-0.134,-0.535,0.107,-90,180,180,"Block")
def get_angular(base,joint_id):
    current_angle = base.GetMeasuredJointAngles()
    constrained_joint_angles = Base_pb2.ConstrainedJointAngles()
    for i in range (len(current_angle.joint_angles)):
       joint_angle = constrained_joint_angles.joint_angles.joint_angles.add()
       joint_angle.joint_identifier = i
       joint_angle.value = current_angle.joint_angles[i].value   
    e = threading.Event()
  
    notification_handle = base.OnNotificationActionTopic(

        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )
    return current_angle.joint_angles[joint_id].value

def angular_trajectory_movement(base,joint_id,degree):
    current_angle = base.GetMeasuredJointAngles()
    constrained_joint_angles = Base_pb2.ConstrainedJointAngles()
    for i in range (len(current_angle.joint_angles)):
       joint_angle = constrained_joint_angles.joint_angles.joint_angles.add()
       if i == joint_id:
          joint_angle.joint_identifier = i
          joint_angle.value = float(current_angle.joint_angles[i].value)+degree
          if joint_angle.value > 148:
              joint_angle.value-=180
          if joint_angle.value > 360:
              joint_angle.value-=360
          if joint_angle.value < 0:
              joint_angle.value+=360
       else:
          joint_angle.joint_identifier = i
          joint_angle.value = current_angle.joint_angles[i].value   
       #print(current_angle.joint_angles[i].value)
    e = threading.Event()
  
    notification_handle = base.OnNotificationActionTopic(

        check_for_end_or_abort(e),
        Base_pb2.NotificationOptions()
    )

    
    print("Reaching Angular..")
    base.PlayJointTrajectory(constrained_joint_angles)

    print("Waiting for movement to finish ...")
    finished = e.wait(TIMEOUT_DURATION)
    base.Unsubscribe(notification_handle)

    if finished:
        print("Angular movement completed")
    else:
        print("Timeout on action notification wait")
    return finished

def finish():
    global client
    client.publish("finish", json.dumps([{"finish":"Finish"}]), qos=1)

def fix_angle_publish():
    global client
    client.publish("fix", json.dumps([{"fix":"start"}]), qos=1)


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import utilities
args = utilities.parseConnectionArguments()
obj = None
obj_height = None
list = None

def main(text,step):
        global x
        global y
        global z
        global theta_x
        global theta_y
        global theta_z
        global obj
        global obj_height
        global list
        # Import the utilities helper module
        
        with utilities.DeviceConnection.createTcpConnection(args) as router:            
                # Create required services
            base = BaseClient(router)
            base_cyclic = BaseCyclicClient(router)
            success = True
        # Parse arguments
            if step==1:
                list = text
                print(text)
                #handle = create_protection_zone(base)
                #success = Trueon_message
                release_gripper(base,0)
                obj = list[0]['obj']
                print(obj)
                obj_height = (float(text[0]['height']))/100
                x = (float(text[0]['depth']))/100
                y = float((text[0]['x_len']))/100
                z = 0.25
                theta_x = 0
                theta_y = 180
                theta_z = 90
                
                # Create connection to the device and get the router
                success &= example_move_to_home_position(base,"Home")
                success &= example_move_to_home_position(base,"Home_Grab")
                
                success &= example_cartesian_trajectory_movement(base, base_cyclic,x,y,z,180,0,0)
                #router.__exit__()
                fix_angle_publish()
                print(get_angular(base,5))
            
            #return success
                
            if step==2:
                #handle = create
                angle = text
                success &= angular_trajectory_movement(base,5,angle)
               
                print("x:",x+0.12,"y:",y,'height',obj_height)
               
                current_pose = base.GetMeasuredCartesianPose()
   
                theta_x = current_pose.theta_x
                theta_y = current_pose.theta_y
                theta_z = current_pose.theta_z
                print(theta_z)
                if obj_height < 0.08:
                  obj_height = 0.06
                success &= example_cartesian_trajectory_movement(base, base_cyclic,x,y,obj_height-0.06,theta_x,theta_y,theta_z)
                grab_gripper(base,0.8)          
                success &= example_cartesian_trajectory_movement(base, base_cyclic,x,y,0.33,theta_x,theta_y,theta_z)
                x,y,z,theta_x,theta_y ,theta_z,home = target_position(x,y,z,theta_x,theta_y,theta_z,obj) 
                #success &= example_move_to_home_position(base,home)
                success &= example_move_to_home_position(base,"Home")
                success &= example_move_to_home_position(base,home) 
                      
                # target position
                success &= example_cartesian_trajectory_movement(base, base_cyclic,x,y,z,theta_x ,theta_y ,theta_z)
                release_gripper(base,0)
                #success &= example_move_to_home_position(base,"Home")
                #success &= example_cartesian_trajectory_movement(base, base_cyclic,0.426,-0.008,0.452,90,0,90)
                #success &= example_move_to_home_position(base,"Home")
                '''list.pop(0)
                print(list)
                '''
                list.pop(0)               
                if len(list)>0:
                   client.publish("position", json.dumps(list), qos=1)
                else:
                   finish()
                #return 0 
        #
def con(): 
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("10.10.10.182", 1883, 60)
    client.loop_forever()            
if __name__ == "__main__":
    con()
    #exit(main([{"obj": "plastic", "locx": 438.0, "x_len": 12.3, "height": 9.12, "depth": 36.0}],1))
