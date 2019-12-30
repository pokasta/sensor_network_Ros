#! /usr/bin/env python3

import tsys01
import ms5837
from time import sleep
from sensor_connect.msg import sensor
from brping import Ping1D

sensor3 = Ping1D("/dev/ttyUSB0",115200)
import rospy

data = sensor3.get_distance_simple()
print(type(data))
key = list(data)
print(type(data.get("distance")))
sensor_data = tsys01.TSYS01()
pressure_data = ms5837.MS5837_02BA(0)

if not sensor_data.init():
    print("Error initializing sensor")
    exit(1)
if not pressure_data.init():
    print("Sensor could not be initialized")
    exit(1)



pub = rospy.Publisher('Temperature',sensor,queue_size=20)



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
    if data:
        print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
    else:
        print("Failed to get distance data")


    

    print("Temperature:",data)
    sens =sensor()
    sens.sensor1 = data1
    sens.sensor2 = pressure_data_send
    sens.sensor3 = data.get("distance")
    pub.publish(sens)
    sleep(.1)