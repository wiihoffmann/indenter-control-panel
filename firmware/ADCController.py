
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import Config

class ADCController():
    """ An interface class for the ADC.
    This class allows for easily interfacing with the ADC to perform operations
    that we need for the indenter (taring, getting load, etc.)
    """

    def __init__(self):
        """Make a new instance of the ADC controller."""
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
        """ Zeroes the load reading."""
        self.offset = self.loadInput.voltage
        return


    def getLoad(self):
        """ Gets the load currently applied to the indenter.
        Returns:
            load (int): the load applied to the indenter in newtons
        """
        load = self.scaler * (self.loadInput.voltage - self.offset)
        return load

