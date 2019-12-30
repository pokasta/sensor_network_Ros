import ms5837
import tsys01
from time import sleep
import serial 
import threading
import pygame



def portIsUsable():
    try:
       ser = serial.Serial("/dev/ttyACM0",9600)
       return ser
    except:
       return False
sensor1 = tsys01.TSYS01()
sensor2 = ms5837.MS5837_02BA(0)

if not sensor2.init():
    print("sensor cant be initialized")
    exit(1)

if not sensor2.read():
    print("sensor read failed")
    exit(1)

if not sensor1.init():
    print("Error Initialiazing Sensor")
    exit(1)

if pygame.joystick.get_count() == 0:
    print("connect joystick")
    pygame.joystick.quit()
    pygame.joystick.init()

def Get_Joystick():
    joystick_1 = pygame.joystick.Joystick(0)
    joystick_1_name = joystick_1.get_name()
    joystick_1.init()
    return joystick_1 , joystick_1_name

print("I Got an Joystick with name {} and no of axis ".format(joystick_1_name ))


print("Pressure: %.2f atm  %.2f Torr  %.2f psi") % (
sensor2.pressure(ms5837.UNITS_atm),
sensor2.pressure(ms5837.UNITS_Torr),
sensor2.pressure(ms5837.UNITS_psi))

print("Temperature: %.2f C  %.2f F  %.2f K") % (
sensor2.temperature(ms5837.UNITS_Centigrade),
sensor2.temperature(ms5837.UNITS_Farenheit),
sensor2.temperature(ms5837.UNITS_Kelvin))

freshwaterDepth = sensor2.depth() # default is freshwater
sensor2.setFluidDensity(ms5837.DENSITY_SALTWATER)
saltwaterDepth = sensor2.depth() # No nead to read() again
sensor2.setFluidDensity(1000) # kg/m^3
print("Depth: %.3f m (freshwater)  %.3f m (saltwater)") % (freshwaterDepth, saltwaterDepth)

# fluidDensity doesn't matter for altitude() (always MSL air density)
print("MSL Relative Altitude: %.2f m") % sensor2.altitude() # relative to Mean Sea Level pressure in air

def instTemp():
    if not sensor1.read():
        print("Error reading sensor")
        exit(1)
    print("Temperature: %.2f C") % (sensor1.temperature())
    sleep(0.2)

def Current_pressure():

    if sensor2.read():
        print("P: %0.1f mbar  %0.3f psi\tT: %0.2f C  %0.2f F") % (
        sensor2.pressure(), # Default is mbar (no arguments)
        sensor2.pressure(ms5837.UNITS_psi), # Request psi
        sensor2.temperature(), # Default is degrees C (no arguments)
        sensor2.temperature(ms5837.UNITS_Farenheit)) # Request Farenheit
    else:
        print("Sensor read failed!")
        exit(1)


def joystic_value():
    joystic_1 , joystic_1_name  = Get_Joystick()
    pygame.event.pump()
    Throttle_value = joystic_1.get_axis(0)
    Yaw_value = joystic_1.get_axis(1)
    roll_value = joystic_1.get_axis(2)
    pitch_value = joystic_1.get_axis(3)
    return Throttle_value,Yaw_value,roll_value,pitch_value


def Get_data():
    X , Y , Z , T = joystic_value()
    X = 200
    d1 = int(1500 + x * X)
    d2 = int(1500 + x * Y)
    d3 = int(1500 + x * Z)
    d4 = int(1500 + x * X)
    d5 = int(1500 + x * T)
    d6 = int(1500 + x * T)
    string =' '
    string ="$,"+  str(d1) +"," + str(d2) + "," +str(d3) + "," + str(d4) + ","+ str(d5) +"," + str(d6) + ",#"

    string += "\t"
    return string

def Send_data():
    ser = portIsUsable()
    if ser == False:
        print("serial port not available cant able to send data")
    else:
        string = Get_data()
        ser.write(bytearray(string,encoding = 'utf-8'))

if __name__ == "__main__":
    while 1:
        Send_data()
        Current_pressure()
        instTemp()
        print("hII")
     
        