
from multiprocessing import Process, Pipe, Event
import time

#custom class imports
from firmware.StepperController import *
from firmware.ADCController import *
from datalogger.Logger import *
from interface.Grapher import *


JOG_SPEED = 2000
TOLERANCE = 1
SAMPLE_RATE = 1000
DIR_PIN = 23  #physical pin 16, GPIO23


class Indenter():

    def __init__(self, graph):
        # the graph object in the UI
        self.graph = Grapher(graph)
        
        # set up the stepper controller and data logger
        self.Stepper = StepperController(DIR_PIN) #physical pin 16, GPIO23
        self.Logger = Logger()

        # used to kill a measurement in an emergency
        self.emergencySignal = Event()
        # process handle for the measurement loop
        self.measurementHandle = None
        return


    def loadAndShowResults(self, filename):
        x, step, load = self.Logger.loadFile(filename)
        self.graph.setData(x, step, load)
        return


    def saveResults(self, filename):
        x, step, load = self.graph.getData()
        self.Logger.saveFile(filename, x, step, load)
        return


    def clearResults(self):
        self.graph.clear()
        return


    def compareResults(self, filename):
        # TODO: load data from another CSV and overlay it on the current graph
        pass


    def startJogUp(self):
        self.Stepper.startMovingUp(JOG_SPEED)
        return


    def stopJogging(self):
        self.Stepper.stopMoving()
        return


    def startJogDown(self):
        self.Stepper.startMovingDown(JOG_SPEED)
        return


    def takeStiffnessMeasurement(self, preload, preloadTime, maxLoad, maxLoadTime, stepRate, doneSignal):        
        # only start a measurement if one is not currently running
        if self.measurementHandle == None or not self.measurementHandle.is_alive():
            self.graph.clear()
            
            # clear emergency stop state and establish a pipe to send data to the graph
            self.emergencySignal.clear()
            parentGraphPipe, childGraphPipe = Pipe()
            self.graph.addDataFromPipe(parentGraphPipe)

            # launch a process to handle taking the stiffness measurement
            self.measurementHandle = Process(name = 'measurementLoop', target = measurementLoop, args=(preload, preloadTime, maxLoad, maxLoadTime, stepRate, childGraphPipe, self.emergencySignal, doneSignal))
            self.measurementHandle.start()
        return


    def emergencyStop(self):
        # terminate the process doing the stiffness measurement
        self.emergencySignal.set()
        return



def applyLoad(displacement, target, stepRate, ADC, stepper, graphPipe, emergencySignal):
    # move down to apply the main load
    load = ADC.getLoad()
    stepper.startMovingDown(stepRate)
    # move down until the target load is achieved
    while(load < target and not emergencySignal.is_set()):
        # log a data point
        displacement += stepper.getDisplacement()
        graphPipe.send([displacement, load*100])
        time.sleep(1 / SAMPLE_RATE)
        load = ADC.getLoad()
    displacement += stepper.stopMoving()
    return displacement


def dwell(displacement, target, stepRate, dwellTime, ADC, stepper, graphPipe, emergencySignal):   
    # once the target load is achieved, dwell at the target load for some time
    startTime = time.time()
    # while the dwell time has not elapsed
    while time.time() < (startTime + dwellTime) and not emergencySignal.is_set():
        time.sleep(1 / SAMPLE_RATE)
        load = ADC.getLoad()
        graphPipe.send([displacement, load*100])
        
        # move up if too much load is applied
        if load > (target + TOLERANCE):
            displacement += stepper.stopMoving()
            stepper.startMovingUp(100)

        # move down is too little load is applied
        elif load < (target - TOLERANCE):
            displacement += stepper.stopMoving()
            stepper.startMovingDown(100)

        # do nothing if the load is just right
        else:
            displacement += stepper.stopMoving()
    return displacement


def retract(displacement, stepRate, ADC, stepper, graphPipe, emergencySignal):
    # return the indenter head to its starting position, logging data on the way
    stepper.startMovingUp(stepRate)
    # move the indenter up by the number of steps we moved it down
    while(displacement > 0 and not emergencySignal.is_set()):
        # log a data point
        displacement += stepper.getDisplacement()
        time.sleep(1 / SAMPLE_RATE)
        load = ADC.getLoad()
        graphPipe.send([displacement, load*100])
    stepper.stopMoving()
    return displacement


def measurementLoop(preload, preloadTime, maxLoad, maxLoadTime, stepRate, graphPipe, emergencySignal, doneSignal):
    try:
        displacement = 0
        stepper = StepperController(DIR_PIN)
        ADC = ADCController()
        ADC.tare()

        # apply preload
        displacement = applyLoad(displacement, preload, stepRate, ADC, stepper, graphPipe, emergencySignal)
        # preload dwell
        displacement = dwell(displacement, preload, stepRate, preloadTime, ADC, stepper, graphPipe, emergencySignal)
        # apply main load
        displacement = applyLoad(displacement, maxLoad, stepRate, ADC, stepper, graphPipe, emergencySignal)
        # main load dwell
        displacement = dwell(displacement, maxLoad, stepRate, maxLoadTime, ADC, stepper, graphPipe, emergencySignal)
        # retract
        displacement = retract(displacement, stepRate, ADC, stepper, graphPipe, emergencySignal)

        # if we had an emergency, we still need to retract the indenter head
        if emergencySignal.is_set():
            stepper.emergencyStop(displacement, stepRate)

    # stop the indenter if any exceptions occur
    except Exception as e:
        stepper.emergencyStop(displacement, stepRate)
        print(e)
    
    # close the pipe to the graph before quitting the process
    finally:
        graphPipe.close()
        doneSignal.set() 
    return

