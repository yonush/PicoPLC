# The RP2340/RP2350 PLC - picoPLC

This repo is the design files and sample code for the diy PLC "picoPLC". It is robust PLC using the Raspberry Pi microcontroller boards as the main controller. Supported boards:

- Raspberry Pico (RP2040)
- Raspberry Pico W (RP2040)
- Raspberry Pico 2 (RP2350 using ARM cores)
- Raspberry Pico 2 (RP2350 using RISCV cores)

Other RP2040/RP2350 boards that follow the Raspberry Pico pinout are also support.ed

The picoPLC has the follwoing features 

- 5-12V power (connections are 12V tolerant. NO 24V)
- Has a 3.3, 5V and 12V breakout (if 12V power used)
- 8 digital outputs using relays
- 8 digital inputs
- 3 analog inputs
- 2 analog outputs (PWM or analog)
- 1 1-wire (Dallas/DHT22/DHT11, etc)
- 1 I2C, SPI, UART (shared pins)

The picoPLC was orignall designed to use the [OpenPLC](https://autonomylogic.com/) soft PLC but it has been tested with C/C++, MicroPython and CircuitPython. Sample code for the CircuitPython has been included. The demo CiruitPython code uses [pyRTOS](https://github.com/Rybec/pyRTOS) as a proof of concept for some asynchronous tasks. 

### Mutlicore operation

Multicore opertation is not supported in CircuitPython but is avaliable using MicroPython. Mutlicore operation can be achieved in OpenPLC by editing the HAL source files and using the mbed toolchain. More details on Using OpenPLC can be found in [OpenPLC Notes](OpenPLC_notes.md)

### TODO
- :white_check_mark: Fix PWM range and frequency (rev2)
- :white_large_square: Revison 3 to support 24V inputs
- :white_large_square: Additional sample code

## Schematic
Schematic was created in Kicad. The BoM can be found in **Schematic and PCB** folder.

![schematic](schematic_rev2.png)


### Physical device

**Revison 1**
![revison_1](Revision1.jpg)


**Revison 2**
![revison_2](Revision2.png)

