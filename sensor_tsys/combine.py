import tsys01
from time import sleep
import ms5837
import pygame
from brping import Ping1D
import serial


global ser
sensor1 = tsys01.TSYS01()
sensor2 = ms5837.MS5837_02BA(0)
sensor3 = Ping1D("/dev/ttyUSB0",115200)
sensor2.setFluidDensity(ms5837.DENSITY_FRESHWATER)
pygame.joystick.quit()
pygame.joystick.init()
pygame.init()
ser = serial.Serial("/dev/ttyACM0",9600)


if pygame.joystick.get_count() == 0:
    pygame.joystick.quit()
    pygame.joystick.init()

def joystickInit():
    js_1 = pygame.joystick.Joystick(0)
    js_1_name = js_1.get_name()
    #print(js_1_name)
    #print("I got the joystick")
    return js_1

if not sensor2.init():
    print("Pressure Sensor could not be initialized")
    exit(1)

if not sensor2.read():
    print("Pressure Sensor read failed!")
    exit(1)

if not sensor1.init():
    print("Error initializing Instant Temperature sensor")
    exit(1)
if sensor3.initialize() is False:
    print("Failed to initialize Ping Sensor!")
    exit(1)


def depth_measure():
    freshwaterDepth = sensor2.depth()
    MSL_relative_Altitude = sensor2.altitude()
    return freshwaterDepth , MSL_relative_Altitude

def measuredPressure():
    if sensor2.read():
        pressure = sensor2.pressure() 
        pressure_in_psi = sensor2.pressure(ms5837.UNITS_psi)
    else:
        print("sensor read failed")
    return pressure , pressure_in_psi

def measuredTemperature():
    if sensor2.read():
        temperature = sensor2.temperature()
    else:
        print("ohh i am able to read shit ...")
    return temperature


def InstTemp():
    if not sensor1.read():
        pritn("error oh my greturn dataod ")
        exit(1)
    else:
        pass
    return sensor1.temperature()


def pingSensorData():
    data = sensor3.get_distance_simple()
    if data:
        print("Distance: %s\tConfidence: %s%%" % (data["distance"], data["confidence"]))
    else:
        print("Failed to get distance data")


def joystickValue():
    js = joystickInit()
    js.init()
    pygame.event.pump()
    T = js.get_axis(0)
    X = js.get_axis(1)
    Y = js.get_axis(2)
    Z = js.get_axis(3)
    return T , X , Y , Z 

def StrintPrepare():
    a,b,c,d = joystickValue()
    string =' '
    k = 100
    Th1 = int(1500 + k * a)
    Th2 = int(1500 + k * a)
    Th3 = int(1500 + k * b)
    Th4 = int(1500 + k * b)
    Th5 = int(1500 + k * c)
    Th6 = int(1500 + k * d)

    string ="$,"+  str(Th1) +"," + str(Th2) + "," +str(Th3) + "," + str(Th4) + ","+ str(Th5) +"," + str(Th6) + ",#" 

    string += "\t"
    
    return string 

def sendString(ser):
    string = StrintPrepare()
    print(string)
    ser.write(bytearray(string,encoding = 'utf-8'))
    print(" I have written data")
    



if __name__ == "__main__":
    while 1:
        depth , depth_msl= depth_measure()
        temp = InstTemp()
        pressure ,pressure_in_psi = measuredPressure()
        print(depth , temp,pressure)
        print("The current pressure is : {} mBar ".format(pressure))
        pingSensorData()
        a, b,c,d = joystickValue()
        print(a)
        sendString(ser)
        #sleep(2)
