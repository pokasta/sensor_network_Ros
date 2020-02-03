#!/usr/bin/env python 

import rospy
from sensor_msgs.msg import Joy
import serial
global ser

ser = serial.Serial("/dev/ttyACM0",115200)
class JoystickInterface(serial.Serial):
    def __init__(self):
        
        rospy.init_node('joystick_node')
        self.sub = rospy.Subscriber('joy_throttle',Joy , self.callback,queue_size=1)
        self.buttons_map = ['A','B','X','Y','LB','RB','back','start','power','stick_button_left','stick_button_right','extra']

        self.axes_map = ['hotizontal','verticle','upward','extra','manipulator','extra1','extra2']
        
        

    def callback(self , msg):
        
        buttons = {}
        axes = {}
        print("working ?")

        for i in range(len(msg.buttons)):
            buttons[self.buttons_map[i]] = msg.buttons[i]
        for j in range(len(msg.axes)):
            axes[self.axes_map[j]] = msg.axes[j]
        print(axes['hotizontal'])
        data = axes['hotizontal']
        
        return data
    

        
    
        

if __name__ == "__main__":
    try:
        joystick_node = JoystickInterface()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass