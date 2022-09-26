#!/usr/bin/python3
# line above lets us launch the program with ./Calibration.py instead of "python3 Calibration.py"

import time
from firmware.Communicator import *

averaging = 50
sample_delay = .1

voltage_averaging = 20
voltage_sample_delay = .001

comm = Communicator()

print("Printing out readings:")


def calibrationMode():
    while True:
        total = 0
        for i in range(averaging):
            total += comm.getRawADCReading()
            time.sleep(sample_delay)

        print("{:>5.3f}".format(total/averaging))


def voltageMode():
    while True:
        total = 0
        for i in range(voltage_averaging):
            total += comm.getADCVoltageReading()
            time.sleep(voltage_sample_delay)

        print("{:>5.3f}".format(total/voltage_averaging/1000))


def selectMode():
    option = input("press 'C' for calibration mode, or 'V' for voltage mode: ").upper()
    if option == 'C':
        calibrationMode()
    elif option == 'V':
        voltageMode()
    else:
        selectMode()


if __name__ == "__main__":
    selectMode()