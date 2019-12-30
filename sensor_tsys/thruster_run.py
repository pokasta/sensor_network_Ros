import pygame
import pygame.mixer
from pygame.locals import *
from time import sleep
import serial


pygame.joystick.quit()
pygame.joystick.init()
pygame.init()
ser = serial.Serial("/dev/ttyACM0",9600)

if pygame.joystick.get_count() == 0:
    print("plaese reconnect joystick")
    pygame.joystick.quit()
    pygame.joystick.init()


js = pygame.joystick.Joystick(0)
js_name = pygame.joystick.Joystick(0).get_name()
js.init()
print("i got the joystick")
print(js_name)

joy_count = pygame.joystick.get_count()
print(joy_count)
buttons =[]
buttons.append(js.get_button(0))
print(buttons)

#pygame.event.pump()

joy_axis = pygame.joystick.Joystick(0).get_numaxes()
print(joy_axis)
x =100

print(pygame.joystick.Joystick(0).get_axis(0))

while 1:
    pygame.event.pump()

    x1 = js.get_axis(0)
    y1 = js.get_axis(1)
    z1 = js.get_axis(2)

    d1 = int(1500 + x * x1)
    d2 = int(1500 + x * x1)
    d3 = int(1500 + x * y1)
    d4 = int(1500 + x * y1)
    d5 = int(1500 + x * z1)
    d6 = int(1500 + x * z1)
    string =' '
    string ="$,"+  str(d1) +"," + str(d2) + "," +str(d3) + "," + str(d4) + ","+ str(d5) +"," + str(d6) + ",#"

    string += "\t"

    ser.write(bytearray(string,encoding = 'utf-8'))
    sleep(1)
    print(string)