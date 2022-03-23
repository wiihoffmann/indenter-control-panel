import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class ADCController():

    def __init__(self):
        self.offset = 0
        # first load/voltage calibration pair
        self.calLoad1 = 0
        self.calVoltage1 = 0
        # second load/voltage calibration pair
        self.calLoad2 = 100
        self.calVoltage2 = 2.00
        # △load / △V (N/V)
        self.scaler = abs(self.calLoad2 - self.calLoad1) / abs(self.calVoltage2 - self.calVoltage1)

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


# import time
# import board
# import busio
# import adafruit_ads1x15.ads1015 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn

# # Create the I2C bus
# i2c = busio.I2C(board.SCL, board.SDA)

# # Create the ADC object using the I2C bus
# ads = ADS.ADS1015(i2c)

# # Create single-ended input on channel 0
# chan = AnalogIn(ads, ADS.P0)

# # Create differential input between channel 0 and 1
# #chan = AnalogIn(ads, ADS.P0, ADS.P1)

# print("{:>5}\t{:>5}".format('raw', 'v'))

# while True:
#     print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
#     time.sleep(0.5)