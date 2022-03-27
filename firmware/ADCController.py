import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import Config

class ADCController():

    def __init__(self):
        self.offset = 0
        # △load / △V (N/V)
        self.scaler = abs(Config.CAL_LOAD_2 - Config.CAL_LOAD_1) / abs(Config.CAL_VOLTAGE_2 - Config.CAL_VOLTAGE_1)

        # Initialize the I2C bus and ADC at max sampling rate
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c, data_rate=860)
        ads.mode = ADS.Mode.CONTINUOUS
        # We use channel 0 for input from the load cell
        self.loadInput = AnalogIn(ads, ADS.P0, ADS.P1)
        return


    def tare(self):
        self.offset = self.loadInput.voltage
        return


    def getLoad(self):
        load = self.scaler * (self.loadInput.voltage - self.offset)
        return load
