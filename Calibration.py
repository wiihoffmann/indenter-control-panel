#!/usr/bin/python3
# line above lets us launch the program with ./Calibration.py instead of "python3 Calibration.py"

import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

averaging = 50
sample_delay = .2

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create differential input between channel 0 and 1
chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("Printing out voltages:")

while True:
    total = 0
    for i in range(averaging):
        total += chan.voltage
        time.sleep(sample_delay)

    print("{:>5.3f}V".format(total/averaging))
    