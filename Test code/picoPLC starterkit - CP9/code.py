# basic template for using the Pico as a Programmable Logic controller
import time

# Pico digital I/O mapping file as per the diagram Pico-OpenPLC-A4-Pinout.pdf
import iomapping as IO


# roll through the outputs and toggle the respective output


def pollOut1(delay):
    for i in range(8):
        port = f"IO.QX{i}"
        fnc = eval(port)
        fnc.value = True
        time.sleep(delay)
        fnc.value = False

# roll through the outputs and toggle the respective output


def pollOut(delay):

    IO.QX0.value = True
    time.sleep(delay)
    IO.QX0.value = False

    IO.QX1.value = True
    time.sleep(delay)
    IO.QX1.value = False

    IO.QX2.value = True
    time.sleep(delay)
    IO.QX2.value = False

    IO.QX3.value = True
    time.sleep(delay)
    IO.QX3.value = False

    IO.QX4.value = True
    time.sleep(delay)
    IO.QX4.value = False

    IO.QX5.value = True
    time.sleep(delay)
    IO.QX5.value = False

    IO.QX6.value = True
    time.sleep(delay)
    IO.QX6.value = False

    IO.QX7.value = True
    time.sleep(delay)
    IO.QX7.value = False

# scan inputs and toggle the respective output twice


def pollIn():
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
            time.sleep(0.2)
            fnc.value = False
            fnc.value = True
            time.sleep(0.2)
            fnc.value = False
            toggle = True
            time.sleep(0.2)

    return toggle


# ========== main ==========
flag = True
while True:

    # keep scanning whilst there is an input
    flag = pollIn()

    if not flag:
        # pollOut(0.2)
        pollOut1(0.1)

# these lines used to confirm code is running in the loop
    IO.LED.value = not IO.LED.value
    time.sleep(1.0)
