# basic template for using the Pico as a Programmable Logic controller
import time
import struct
from microcontroller import cpu
import simpleio
import adafruit_ssd1306
import adafruit_dht
#from adafruit_motor import servo

# Pico digital I/O mapping file as per the diagram Pico-OpenPLC-A4-Pinout.pdf
import iomapping as IO
import pyRTOS as OS

MSG_FLAG = 128
MSG_DISP = 129
MSG_NULL = 130


# attach an oled = adafruit_ssd1306.SSD1306_I2C(128, Y, IO.I2C, addr=0x3C)
# change the 32 to 64 for the larger oled
# YRES 32 for the smaller thin OLED display
# YRES 64 for the larger square OLED display
oled = adafruit_ssd1306.SSD1306_I2C(128, 64,IO.I2C)

# attach dht to the single wire on GPIO22
dht = adafruit_dht.DHT11(IO.ONEWIRE)

# roll through the outputs and toggle the respective output

def pollOut(self):
    # Pass control back to RTOS
    yield

    while True:
        msgs = self.recv()

        for msg in msgs:
            if msg.type == MSG_FLAG and msg.message:
                print('MSG_FLAG')
                for i in range(8):
                    port = f"IO.QX{i}"
                    fnc = eval(port)
                    fnc.value = True            
                    yield [OS.timeout(1)]
                    fnc.value = False
        yield [OS.timeout(0.1)]

def pollIn(self):
    yield

    while True:
        flag = False
        # scan inputs and toggle the respective output twice
        for i in range(8):
            port = f"IO.IX{i}"
            fnc = eval(port)
            # if the input is high toggle the out twice
            if fnc.value:                
                port = f"IO.QX{i}"
                fnc = eval(port)
                fnc.value = True
                yield [OS.timeout(1)]
                fnc.value = False                
                flag = True
        if flag:                
            self.send(OS.Message(MSG_FLAG, self, "pollout",flag))
        flag = False    
        yield [OS.timeout(0.1)]

def dispOLED(self):
    yield
    
    # updating the OLED display is vey slow and blocks IO
    while True:
        msgs = self.recv()
        for msg in msgs:
            if msg.type == MSG_DISP:
                print(f'MSG_DISP {msg.type}')
                oled.fill(0)
                oled.text("Ambient T & H", 0, 0, 1)
                if  msg.source == "telem":                 
                    oled.text(msg.message, 0, 10, 1)
                elif msg.source == "analog":
                    oled.text(msg.message, 0, 20, 1)
                elif msg.source == "pwm":                    
                    oled.text(msg.message, 0, 30, 1)
                oled.show()              
                
        yield [OS.timeout(0.1)]

def doTelemetry(self):
    yield

    while True:
        txt = None
        try:
            txt = f"T:{dht.temperature}', H:{dht.humidity}%, C:{cpu.temperature:.0f}'"

        except:
            pass 
        if txt != None:
            self.send(OS.Message(MSG_DISP, "telem", "dispoled",txt))             

        yield [OS.timeout(1.0)]

def sendDHT(self):
    yield

    while True:
        try:
        #pass
            buffer = struct.pack("<iii",int(dht.humidity), dht.temperature, int(cpu.temperature))        
            IO.UART.write(buffer)
        except RuntimeError as error:
            print("Transmission or data error")
            return
        except Exception as error:
            dht.exit()
            raise error
        yield [OS.timeout(1.0)]

def doAnalog(self):
    yield

    while True:
        value1 = IO.IW0.value * (IO.IW0.reference_voltage /65535)
        value2 = IO.IW1.value * (IO.IW1.reference_voltage /65535)
        dc1 = int(simpleio.map_range(value1, 0, 2.45 , 0, 65535))
        dc2 = int(simpleio.map_range(value2, 0, 2.45 , 0, 65535))
        IO.QW0.duty_cycle = dc1
        IO.QW1.duty_cycle = dc2
        self.send(OS.Message(MSG_DISP, "analog", "dispoled",f'{value1:.2f},{value2:.2f}V')) 
        self.send(OS.Message(MSG_DISP, "pwm", "dispoled",f'dc: {dc1},{dc2}')) 
        yield [OS.timeout(0.2)]

def blinkLED(self):
    yield

    while True:
        IO.LED.value = not IO.LED.value
        yield [OS.timeout(0.1)]

# ========== main ==========

OS.add_task(OS.Task(blinkLED, priority=0,))
OS.add_task(OS.Task(pollIn, priority=2, name="pollin", mailbox=True))
OS.add_task(OS.Task(pollOut, priority=1, name="pollout", mailbox=True))

OS.add_task(OS.Task(doAnalog, priority=6, name="analog", mailbox=True))
OS.add_task(OS.Task(doTelemetry, priority=6, name="telem", mailbox=True))
# the OLED display is a very slow device and can cause slow IO
#OS.add_task(OS.Task(dispOLED, priority=10, name="dispoled", mailbox=True))


#OS.add_task(OS.Task(sendDHT))
OS.start()

