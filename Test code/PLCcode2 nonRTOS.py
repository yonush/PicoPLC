# basic template for using the Pico as a Programmable Logic controller
import time
import struct
from microcontroller import cpu
import usb_cdc
import simpleio
import adafruit_ssd1306
import adafruit_dht
#from adafruit_motor import servo

# Pico digital I/O mapping file as per the diagram Pico-OpenPLC-A4-Pinout.pdf
import iomapping as IO

# uart = usb_cdc.console
uart = usb_cdc.data

# attach an oled = adafruit_ssd1306.SSD1306_I2C(128, Y, IO.I2C, addr=0x3C)
# change the 32 to 64 for the larger oled
# YRES 32 for the smaller thin OLED display
# YRES 64 for the larger square OLED display
oled = adafruit_ssd1306.SSD1306_I2C(128, 64,IO.I2C)

# attach dht to the single wire on GPIO22
dht = adafruit_dht.DHT11(IO.ONEWIRE)

# roll through the outputs and toggle the respective output
def pollOut(delay):
    for i in range(8):
        port = f"IO.QX{i}"
        fnc = eval(port)
        fnc.value = True
        time.sleep(delay)
        fnc.value = False

def pollIn():
# scan inputs and toggle the respective output twice
    toggle = False
    # scan through the inputs
    for i in range(8):
        port = f"IO.IX{i}"
        fnc = eval(port)
        # if the input is high toggle the out twice
        if fnc.value:
            port = f"IO.QX{i}"
            fnc = eval(port)
            fnc.value = True
            time.sleep(0.5)
            fnc.value = False
            toggle = True
            time.sleep(0.2)
    return toggle

def dispOLED():
    oled.text("Ambient T & H", 0, 0, 1)
    txt = ""   
   #txt = "T:%d, H:%d, C:%.2f"% (dht.temperature, dht.humidity,cpu.temperature)
    try:
        txt = f"T:{dht.temperature}', H:{dht.humidity}%, C:{cpu.temperature:.0f}'"
    except:
        return
    time.sleep(0.02)
    oled.text(txt, 0, 10, 1)

def sendDHT():
    try:
      #pass
        buffer = struct.pack("<iii",int(dht.humidity), dht.temperature, int(cpu.temperature))        
        uart.write(buffer)
    except RuntimeError as error:
        print("Transmission or data error")
        return
    except Exception as error:
        dht.exit()
        raise error

def doAnalog():
    value1 = IO.IW0.value * (IO.IW0.reference_voltage /65535)
    value2 = IO.IW1.value * (IO.IW1.reference_voltage /65535)
    dc1 = int(simpleio.map_range(value1, 0, 2.45 , 0, 65535))
    dc2 = int(simpleio.map_range(value2, 0, 2.45 , 0, 65535))
    v = f'voltage: {value1:.2f},{value2:.2f}V'
    dc = f'dc: {dc1},{dc2}'
    print(v,dc)
    #servo.angle = simpleio.map_range(value, 0, 2.5, 0, 100)
    IO.QW0.duty_cycle = dc1
    IO.QW1.duty_cycle = dc2
    oled.text(v,0,20,1)
    oled.text(dc,0,30,1)
    
# ========== main ==========
flag = True
while True:
    oled.fill(False)  
    dispOLED()
# keep scanning whilst there is an input
    flag = pollIn()

    if not flag:
        pollOut(0.1)
    
    sendDHT()
    doAnalog()
    oled.show()
    
# these lines used to confirm code is running in the loop
    IO.LED.value = not IO.LED.value
    time.sleep(0.02)
    