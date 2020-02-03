#! /usr/bin/env python 

import roslib
import rospy 
from std_msgs.msg import String
import serial 
from time import sleep


ser = serial.Serial("/dev/ttyACM0" , 115200)

def callback(data):
    print(data.data)
    new_string = data.data
    ser.write(new_string)
    
    

def listener():
    rospy.init_node('receive' , anonymous= True)
    rospy.Subscriber('Thrust_values',String,callback)
    #rate = rospy.Rate(10)
    rospy.spin()
    #sleep(.001)


if __name__ == "__main__":
    listener()