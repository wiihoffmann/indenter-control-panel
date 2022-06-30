
import Config


def calculateCalFactor():
    # △ADC (N/V) / △load
    return abs(Config.CAL_VOLTAGE_2 - Config.CAL_VOLTAGE_1) / abs(Config.CAL_READING_2 - Config.CAL_READING_1)


def stepRateToMicros(stepRate):
    return (1/stepRate) * 10**6 / 2


def NewtonToRawADC(load):
    return calculateCalFactor() * load


def rawADCToNewton(reading):
    return reading / calculateCalFactor()