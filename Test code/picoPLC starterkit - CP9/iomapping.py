'''
    Pico I/O mapping as a Programmable Logic controller
    This file provides the digital input and output mapping 
    
    I/O mapping file as per the diagram Pico-OpenPLC-A4-Pinout.pdf
'''
import board
import digitalio
import pwmio
import analogio
import busio
import usb_cdc


# uart = usb_cdc.console
UART = usb_cdc.data

# ---- picoPLC addtional I/O MAPPING
ONEWIRE = board.GP22

# onboard led used for runtime activity
LED = digitalio.DigitalInOut(board.LED)
LED.direction = digitalio.Direction.OUTPUT


# analogue outputs & PWM - defaults to 1KHz
QW0 =  pwmio.PWMOut(board.GP5, duty_cycle=2 ** 15, frequency=1000)
QW1 = pwmio.PWMOut(board.GP4, duty_cycle=2 ** 15, frequency=1000)
PWM1 = AOUT1 = QW0
PWM2 = AOUT2 = QW1

# analogue inputs
IW0 = analogio.AnalogIn(board.GP26)
IW1 = analogio.AnalogIn(board.GP27)
IW2 = analogio.AnalogIn(board.GP28)
ADC0 = IW0
ADC1 = IW1
ADC2 = IW2

# I2C & UART
SDA = TX = board.GP0 # data out
SCL = RX = board.GP1 # data in
# SPI
SPI_RX  = board.GP0
SPI_CS  = board.GP1
SPI_SCK = board.GP2
SPI_TX  = board.GP3 

# setup the I2C interface - default 400KHz
try:
    I2C = busio.I2C(SCL, SDA, frequency=1000000)
    while not I2C.try_lock(): pass
    print("I2C addresses found:", [hex(device_address) for device_address in I2C.scan()])
    I2C.unlock()
except:
    print("No I2C device attached")

# ----- define the inputs and outputs
# INPUT I/O
IX0 = digitalio.DigitalInOut(board.GP6)
IX1 = digitalio.DigitalInOut(board.GP7)
IX2 = digitalio.DigitalInOut(board.GP8)
IX3 = digitalio.DigitalInOut(board.GP9)
IX4 = digitalio.DigitalInOut(board.GP10)
IX5 = digitalio.DigitalInOut(board.GP11)
IX6 = digitalio.DigitalInOut(board.GP12)
IX7 = digitalio.DigitalInOut(board.GP13)

IX0.direction = digitalio.Direction.INPUT
IX0.pull = digitalio.Pull.DOWN
IX1.direction = digitalio.Direction.INPUT
IX1.pull = digitalio.Pull.DOWN
IX2.direction = digitalio.Direction.INPUT
IX2.pull = digitalio.Pull.DOWN
IX3.direction = digitalio.Direction.INPUT
IX3.pull = digitalio.Pull.DOWN
IX4.direction = digitalio.Direction.INPUT
IX4.pull = digitalio.Pull.DOWN
IX5.direction = digitalio.Direction.INPUT
IX5.pull = digitalio.Pull.DOWN
IX6.direction = digitalio.Direction.INPUT
IX6.pull = digitalio.Pull.DOWN
IX7.direction = digitalio.Direction.INPUT
IX7.pull = digitalio.Pull.DOWN

# OUTPUT I/O
QX0 = digitalio.DigitalInOut(board.GP21)
QX1 = digitalio.DigitalInOut(board.GP20)
QX2 = digitalio.DigitalInOut(board.GP19)
QX3 = digitalio.DigitalInOut(board.GP18)
QX4 = digitalio.DigitalInOut(board.GP17)
QX5 = digitalio.DigitalInOut(board.GP16)
QX6 = digitalio.DigitalInOut(board.GP15)
QX7 = digitalio.DigitalInOut(board.GP14)

QX0.direction = digitalio.Direction.OUTPUT
QX1.direction = digitalio.Direction.OUTPUT
QX2.direction = digitalio.Direction.OUTPUT
QX3.direction = digitalio.Direction.OUTPUT
QX4.direction = digitalio.Direction.OUTPUT
QX5.direction = digitalio.Direction.OUTPUT
QX6.direction = digitalio.Direction.OUTPUT
QX7.direction = digitalio.Direction.OUTPUT
