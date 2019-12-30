import serial
import warnings

import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
print(ports[0])
str = ""
int = 0

for p in serial.tools.list_ports_linux.comports():
    print(p.device)
if "ttyACM" in p.description:
    print("Yes its there")
    print(p.description)
    data = list(p.description)
    print(data[6])

else:
    print("what the hell are you printing")