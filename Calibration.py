#!/usr/bin/python3
# line above lets us launch the program with ./Calibration.py instead of "python3 Calibration.py"

import time
from firmware.Communicator import *

averaging = 50
sample_delay = .1

comm = Communicator()

print("Printing out readings:")

while True:
    total = 0
    for i in range(averaging):
        total += comm.getRawADCReading()
        time.sleep(sample_delay)

    print("{:>5.3f}".format(total/averaging))
    