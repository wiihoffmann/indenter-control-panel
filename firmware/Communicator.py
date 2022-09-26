import time
import serial
import serial.tools.list_ports
import dataTools.UnitConverter as uc
import dataTools.MeasurementParams
from struct import *

ERROR_CODE = 'E'
EMERGENCY_STOP_CODE = 'H'
MOVE_X_AXIS_CODE = 'X'
MOVE_Y_AXIS_CODE = 'Y'
MOVE_Z_AXIS_CODE = 'Z'
BEGIN_MEASUREMENT_CODE = 'B'
REGULAR_DATA_POINT_CODE = 'D'
MAX_LOAD_CODE = 'b'
DATA_POINT_WITH_VAS_CODE = 'V'
SINGLE_VAS_SCORE_CODE = 'v'
MEASUREMENT_COMPLETE_CODE = 'C'
NEW_TEST_BEGIN_CODE = 'N'
RAW_MEASUREMENT_CODE = 'M'
RAW_MEASUREMENT_VOLTS_CODE = 'm'
CONTROLLER_READY_CODE = 'R'
NO_COMMAND_CODE = 'K'


REGULAR_TEST_CODE = bytes("R", 'utf-8')
PPT_TEST_CODE = bytes("T", 'utf-8')
PPI_TEST_CODE = bytes("I", 'utf-8')
TEMPORAL_SUMMATION_TEST_CODE = bytes("S", 'utf-8')

arduino = None

class Communicator:

    def __init__(self):
        global arduino

        if arduino == None: 
            ports = list(serial.tools.list_ports.comports())
            if len(ports) != 0:
                for p in ports:
                    if (p.description is not None and "USB2.0-Ser!" in p.description) or (p.manufacturer is not None and "Arduino" in p.manufacturer):
                        arduino = serial.Serial(port=p.device, baudrate=1000000, timeout=None)
                        arduino.flush()

                        # wait for arduino to be ready
                        while(self.readCommand() != CONTROLLER_READY_CODE):
                            time.sleep(0)
                        return
            raise RuntimeError("Could not detect and connect to the Arduino. Is it connected?")


    def __sendCommand(self, preamble, num=0000):
        preamble = bytes(preamble, 'utf-8')
        dataToSend = pack("<%dsh" % (len(preamble)), preamble, int(num))
        arduino.write(dataToSend)


    def commandAvailable(self):
        return arduino.in_waiting >= 4


    def readCommand(self):
        while not self.commandAvailable():
            time.sleep(0)
        
        numBytesWaiting = arduino.in_waiting
        readBytes = arduino.read_until(b'*', numBytesWaiting)
        if len(readBytes) < numBytesWaiting:
            return arduino.read().decode('utf-8')
        
        print("ERROR: trying to read command again!")
        print("Discarded bytes: " + str(readBytes))
        return(self.readCommand())


    def readInt(self):
        data = arduino.read(2)
        value = int.from_bytes(data, byteorder='little', signed=True)
        return value


    def getRawADCReading(self):      
        # request raw ADC value and wait for reply
        self.__sendCommand("*M", 1234)
        
        # make sure we get a raw adc reading
        command = self.readCommand()
        if command != 'M': return
        reading = self.readInt()

        return reading


    def getADCVoltageReading(self):      
        # request a voltage reading from the ADC and wait for reply
        self.__sendCommand("*m", 1234)
        
        # make sure we get a raw adc reading
        command = self.readCommand()
        if command != 'm': return
        reading = self.readInt()

        return reading


    def sendMeasurementBegin(self, params: dataTools.MeasurementParams):
        # convert from steps/second to micros/step
        dataToSend = pack("<%dshHhHHHHHHH?c" % (len(params.preamble)), params.preamble, params.preload, params.preloadTime, params.maxLoad, params.maxLoadTime, params.stepDelay, params.holdDownDelay, params.holdUpDelay, params.eStopStepDelay, params.tolerance, params.iterations, params.flipDirection, params.testType)
        arduino.write(dataToSend)


    def readDataPoint(self):
        # wait for the data point to arrive
        while arduino.in_waiting < 7:
            time.sleep(0)

        data = unpack("<ihB", arduino.read(7))
        return data


    def readDataPointWithVAS(self):
        # wait for the data point with VAS score to arrive
        while arduino.in_waiting < 9:
            time.sleep(0)

        data = unpack("<ihBh", arduino.read(9))
        return data


    def emergencyStop(self, stepRate):
        self.__sendCommand('*S', uc.stepRateToMicros(stepRate))


    def moveXAxisUp(self, stepRate):
        self.__sendCommand('*X', -1*uc.stepRateToMicros(stepRate))


    def moveXAxisDown(self, stepRate):
        self.__sendCommand('*X', uc.stepRateToMicros(stepRate))


    def stopXAxis(self):
        self.__sendCommand('*X', 0)


    def moveYAxisUp(self, stepRate):
        self.__sendCommand('*Y', -1*uc.stepRateToMicros(stepRate))


    def moveYAxisDown(self, stepRate):
        self.__sendCommand('*Y', uc.stepRateToMicros(stepRate))


    def stopYAxis(self):
        self.__sendCommand('*Y', 0)


    def moveZAxisUp(self, stepRate):
        self.__sendCommand('*Z', -1*uc.stepRateToMicros(stepRate))


    def moveZAxisDown(self, stepRate):
        self.__sendCommand('*Z', uc.stepRateToMicros(stepRate))


    def stopZAxis(self):
        self.__sendCommand('*Z', 0)

