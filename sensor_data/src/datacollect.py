#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
import serial
global buttons_map
global axes_map
global ser
global pub 

import numpy as np
from time import sleep
from std_msgs.msg import String


ser = serial.Serial("/dev/ttyACM2", 9600)


def rescale(val , in_min , in_max , out_min , out_max):
    i = 0 
    data = []
    for i in range(len(val[0])):
        data.append(out_min + (float(val[0][i])- in_min) *((out_max-out_min)/(in_max-in_min)))
        i += 1
    return data 

def listtostring(x):
    str1 = ""
    str1 += "$,"
    for ele in x:
        str1 += str(ele)
        str1 += ","
    str1 += "#"
    str1 += "\t"
    return str1

def callback(msg):
    buttons_map = ['A','B','X','Y','LB','RB','back','start','power','stick_button_left','stick_button_right','extra']
    axes_map = ['horizontal','verticle','upward','extra','manipulator','extra1','extra2']

    buttons = {}
    axes = {}
    print("working ?")

    for i in range(len(msg.buttons)):
        buttons[buttons_map[i]] = msg.buttons[i]
    for j in range(len(msg.axes)):
        axes[axes_map[j]] = msg.axes[j]
    

    hor = axes['horizontal']
    ver = axes['verticle']
    upw = axes['upward']
    yaw = axes['extra']
    mani= axes['manipulator'] 
    print(hor,ver , upw ,yaw, mani)


    Thrust_matrix = np.transpose(np.array([[1,1,-1,-1,0,0],[0,0,0,0,0,0],[0,0,0,0,1,1],[1,-1,1,-1,0,0]]))

    joystic_vector = np.transpose(np.array([[ver],[hor],[upw],[yaw]]))

    thrust_vector = np.inner(joystic_vector,Thrust_matrix)

    data = thrust_vector.tolist()
    values = rescale(data,-1,1,1200,1800)
    new_list = []
    for item in values:
        new_list.append(int(item))
    data_string = listtostring(new_list)
    print(data_string)

    print(bytearray(data_string ,encoding='utf-8'))
    ser.write(bytearray(data_string ,encoding='utf-8'))
    
    
    
    sleep(1)


def datawer():
    rospy.init_node('joystick_node')
    sub = rospy.Subscriber('joy_throttle',Joy ,callback,queue_size=1)
    

    

    
if __name__ == "__main__":
    datawer()
    rospy.spin()
    


        