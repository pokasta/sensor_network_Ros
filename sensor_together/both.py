import ms5837
import tsys01
from time import sleep
import serial 
import threading



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



if __name__ == "__main__":
    while 1:
        
        Current_pressure()
        instTemp()
     
        