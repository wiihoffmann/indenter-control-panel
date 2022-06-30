import time
import serial
import serial.tools.list_ports
import dataTools.UnitConverter as uc
import dataTools.MeasurementParams
from struct import *

_connected = False

class Communicator:

    def __init__(self):
        global _connected

        if not _connected: 
            _connected = True
            ports = list(serial.tools.list_ports.comports())
            
            if len(ports) != 0:
                self.arduino = serial.Serial(port=ports.pop().device, baudrate=2000000, timeout=None)
                self.arduino.flush()

                # wait for arduino to be ready
                while(self.readCommand() != 'R'):
                    time.sleep(0)

            else:
                raise RuntimeError("Could not detect and connect to the Arduino. Is it connected?")


    def __sendCommand(self, preamble, int=0000):
        preamble = bytes(preamble, 'utf-8')
        dataToSend = pack("<%dsh" % (len(preamble)), preamble, int)
        self.arduino.write(dataToSend)


    def commandAvailable(self):
        return self.arduino.in_waiting >= 4


    def readCommand(self):
        while not self.commandAvailable():
            time.sleep(0)
        
        numBytesWaiting = self.arduino.in_waiting
        readBytes = self.arduino.read_until(b'*', numBytesWaiting)
        if len(readBytes) < numBytesWaiting:
            return self.arduino.read().decode('utf-8')
        
        print("ERROR: trying to read command again!")
        print("Discarded bytes: " + str(readBytes))
        return(self.readCommand())


    def readInt(self):
        data = self.arduino.read(2)
        value = int.from_bytes(data, byteorder='little', signed=True)
        return value


    def getRawADCReading(self):      
        # request raw ADC value and wait for reply
        self.sendCode("*M", 1234)
        
        # make sure we get a raw adc reading
        command = self.readCommand()
        if command != 'M': return
        reading = self.readInt()

        return reading


    def sendMeasurementBegin(self, params: dataTools.MeasurementParams):
        # convert from steps/second to micros/step
        dataToSend = pack("<%dshHhHHHHHH?" % (len(params.preamble)), params.preamble, params.preload, params.preloadTime, params.maxLoad, params.maxLoadTime, params.stepDelay, params.holdDownDelay, params.holdUpDelay, params.eStopStepDelay, params.tolerance, params.flipDirection)
        self.arduino.write(dataToSend)


    def readDataPoint(self):
        # wait for the data point to arrive
        while self.arduino.in_waiting < 9:
            time.sleep(0)

        data = unpack("<ihB", self.arduino.read(7))
        return data


    def moveXAxisUp(self, stepRate):
        self.__sendCommand('X', -1*uc.stepRateToMicros(stepRate))


    def moveXAxisDown(self, stepRate):
        self.__sendCommand('X', uc.stepRateToMicros(stepRate))


    def stopXAxis(self):
        self.__sendCommand('X', 0)


    def moveYAxisUp(self, stepRate):
        self.__sendCommand('Y', -1*uc.stepRateToMicros(stepRate))


    def moveYAxisDown(self, stepRate):
        self.__sendCommand('Y', uc.stepRateToMicros(stepRate))


    def stopYAxis(self):
        self.__sendCommand('Y', 0)


    def moveZAxisUp(self, stepRate):
        self.__sendCommand('Z', -1*uc.stepRateToMicros(stepRate))


    def moveZAxisDown(self, stepRate):
        self.__sendCommand('Z', uc.stepRateToMicros(stepRate))


    def stopZAxis(self):
        self.__sendCommand('Z', 0)

