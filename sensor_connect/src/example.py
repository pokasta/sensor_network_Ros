#! /usr/bin/env python3

import tsys01
import ms5837
from time import sleep
from std_msgs.msg import Float32
from sensor_connect.msg import sensor
from brping import Ping1D
import rospy

sensor3 = Ping1D("/dev/ttyUSB0",115200)


data = sensor3.get_distance_simple()
sensor_data = tsys01.TSYS01()
pressure_data = ms5837.MS5837_02BA(0)

if not sensor_data.init():
    print("Error initializing sensor")
    exit(1)
if not pressure_data.init():
    print("Sensor could not be initialized")
    exit(1)



pub1 = rospy.Publisher('Altimeter',Float32,queue_size=1)
pub2 = rospy.Publisher('Pressure',Float32,queue_size=20)
pub3 = rospy.Publisher('Temperature',Float32,queue_size=20)
rospy.init_node('sender',anonymous=True)

rate = rospy.Rate(1)
while True:
    if not sensor_data.read():
        print("Error reading sensor")
        exit(1)
    data1 = sensor_data.temperature()
    if pressure_data.read():

        pressure_data_send = pressure_data.pressure()
        
    else:
        print("Sensor read failed!")
        exit(1)
    if data:#print(type(sensor_data.temperature()))
        print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
    else:
        print("Failed to get distance data")


    pub2.publish(pressure_data_send)
    pub3.publish(data1)
    sensor = data.get("distance")
    pub1.publish(sensor)
    sleep(.1)