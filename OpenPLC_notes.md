# Notes on using OpenPLC with the Raspberry Pico 1, Pico W and Pico 2

Other variants of the pico board work too. This may require changes or additions to the editor\arduino\examples\Baremetal\hals.json file.

An additional .cpp & .hal file might be requried in the editor\arduino\src\hal folder to support new pico hardware.

## OpenPLC hal definitions for the Pico 1, Pico 1 W, and Pico 2

The Hardard 3 cores in the Pico 2 are also supported by OpenPLC

**Note, the mapping of the digital out pins in OpenPLC differ to the physical pins on the picoPLC.**

``` json
  "Raspberry Pico": {
    "core": "rp2040:rp2040",
    "default_ain": "26, 27, 28",
    "default_aout": "4,5",
    "default_din": "6, 7, 8, 9, 10, 11, 12, 13",
    "default_dout": "14, 15, 16, 17, 18, 19, 20, 21",
    "last_update": 0,
    "platform": "rp2040:rp2040:rpipico",
    "source": "rp2040pico.cpp",
    "version": "4.2.0"
  },
  "Raspberry Pico 2": {
    "core": "rp2040:rp2040",
    "default_ain": "26, 27, 28",
    "default_aout": "4,5",
    "default_din": "6, 7, 8, 9, 10, 11, 12, 13",
    "default_dout": "14, 15, 16, 17, 18, 19, 20, 21",
    "last_update": 0,
    "platform": "rp2040:rp2040:rpipico2",
    "source": "rp2040pico.cpp",
    "version": "4.2.0"
  },
  "Raspberry Pico 2 (RISCV)": {
    "arch": "riscv",
    "core": "rp2040:rp2040",
    "default_ain": "26, 27, 28",
    "default_aout": "4,5",
    "default_din": "6, 7, 8, 9, 10, 11, 12, 13",
    "default_dout": "14, 15, 16, 17, 18, 19, 20, 21",
    "last_update": 0,
    "platform": "rp2040:rp2040:rpipico2:arch=riscv",
    "source": "rp2040pico.cpp",
    "version": "4.2.0"
  },
  "Raspberry Pico W": {
    "core": "rp2040:rp2040",
    "default_ain": "26, 27, 28",
    "default_aout": "4,5",
    "default_din": "6, 7, 8, 9, 10, 11, 12, 13",
    "default_dout": "14, 15, 16, 17, 18, 19, 20, 21",
    "define": "BOARD_PICOW",
    "last_update": 0,
    "platform": "rp2040:rp2040:rpipicow",
    "source": "rp2040pico.cpp",
    "version": "4.2.0"
  },
```
## RP2040/RP2350 notes for the picoPLC pinout

Raspberry Pi Pico PINOUT (RP2040)
Digital In:  6, 7 ,8, 9, 10, 11, 12, 13     (%IX0.0 - %IX0.7)
Digital Out: 21, 20, 19, 18, 17, 16, 15, 14 (%QX0.0 - %QX0.7) (this is opposite to the list in OpenPLC)
Analog In: A1, A2, A3 (26,27,28)            (%IW0 - %IW2)
Analog Out: 4,5                             (%QW0 - %QW1)

The onboard LED (GPIO25) is not used but can be accessed from OpenPLC for the Pico or Pico 2 NOT the Pico W!!

## updated modbus addressing

The Modbus address space was expanded to include memory locations %MW (16-bit words) %MD (32-bit double words) and %ML (64-bit long words). These extra memory locations are available as Modbus holding registers. Here is the breakdown of the address space:
 
%QW0 - %QW31 -> Modbus holding registers 0 - 31
%MW0 - %MW19 -> Modbus holding registers 32 - 51
%MD0 - %MD19 -> Modbus holding registers 52 - 91 (each MD takes up two Modbus registers)
%ML0 - %ML19 -> Modbus holding registers 92 - 171 (each ML takes up four Modbus registers)
 
This means can also read/write REAL and LREAL variables on Modbus registers. You can locate the REAL variable on any %MD location or LREAL variable on any %ML location. Larger integers are also possible using these expanded locations. On the modbus master side, you just need to configure your application to concatenate Modbus registers to form an IEEE float (two registers in case of REAL or four registers in case of LREAL).

### Typical Modbus ranges
Discrete Output Coils      00001-09999
Discrete Input Contacts    10001-19999
Analog Input Registers     30001-39999
Holding Registers          40001-49999
 

The following location prefixes are supported:
    I for input
    Q for output
    M for memory

The following size prefixes are supported:

    X for bit (1 bit)
    B for byte (8 bits)
    W for word (16 bits)
    D for double word (32 bits)
    L for long word (64 bits)

The following are invalid examples of PLC addresses in OpenPLC for the stated reason:

    %IX0.8 The least significant index is greater than 7.
    %QX0.0.1 Three part hierarchy is not permitted address.
    %IB1.1 Two part hierarchy is only permitted for X data size.

### Modbus functions

OpenPLC supports the following Modbus functions:

    Read discrete output coil (0x01)
    Write discrete output coil (0x05)
    Write multiple discrete output coils (0x0F)
    Read discrete input contacts (0x02)
    Read analog input registers (0x04)
    Read analog output holding registers (0x03)
    Write analog output holding register (0x06)
    Write multiple analog output registers (0x10)

Discrete output coil and discrete input contact binding are based on the the two-part PLC address, without unused Modbus data addresses. The least-significant part of the PLC address has a range 0 to 7, therefore, a little math is needed to translate between PLC addresses and Modbus data addresses. Given the Modbus data address, the PLC address is determined as:

    msp := int(modbus_data_address / 8)
    lsp := modbus_data_address mod 8
    final address = msp.lsp

    For example, if the Modbus address for a discrete output coil is 22, then the most significant part is 2 (22 / 8) and the least significant part is 6 (22 mod 8). Therefore, the PLC address is %QX2.6.

## Avoiding the "error: implicit declaration of function" in OpenPLC

This error happens when you declare variables in the **Res0** file and not the **Program** file.

There are two toolchains that you can use in OpenPLC:

    Board FQBN: rp2040:rp2040:rpipico (currently used in OpenPLC)
    Board FQBN:- arduino:mbed_rp2040:pico

The #1 is from [earlephilhower on Github](https://github.com/earlephilhower/arduino-pico/) and #2 Arduino mbed toolchain.

The board types are set in the *editor\arduino\examples\Baremetal\hals.json* file.
If you compile your code with #1 you will get the "implicit declaration of function" because the code has moved from the POU.c to Res0.c and this compiler does not like you using functions before declaring them. The globals can be moved to the project. If you use the #2 toolcahain then the error disappears. I have not found a safer way of solving the Res0 issue.
 
Using the following will be required to install the additional toolchain. the bin can be found in the 
editor\arduino\bin or downloaded directly from [arduino-cli](https://arduino.github.io/arduino-cli/1.1/installation/#latest-packages)
``` sh
arduino-cli-w64.exe core install arduino:mbed_rp2040
```

 
## Research
Tangible Learning for IoT and Automation ... in a Lunchbox

