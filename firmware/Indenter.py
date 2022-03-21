
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


    def takeStiffnessMeasurement(self, preload, preloadTime, maxLoad, maxLoadTime, stepRate):
        # only start a measurement if one is not currently running
        if self.measurementHandle == None or not self.measurementHandle.is_alive():
            self.graph.clear()
            
            # clear emergency stop state and establish a pipe to send data to the graph
            self.emergencySignal.clear()
            parentGraphPipe, childGraphPipe = Pipe()
            self.graph.addDataFromPipe(parentGraphPipe)

            # launch a process to handle taking the stiffness measurement
            self.measurementHandle = Process(name = 'measurementLoop', target = measurementLoop, args=(preload, preloadTime, maxLoad, maxLoadTime, stepRate, childGraphPipe, self.emergencySignal))
            self.measurementHandle.start()
        return


    def emergencyStop(self):
        # terminate the process doing the stiffness measurement
        self.emergencySignal.set()
        return



def measurementLoop(preload, preloadTime, maxLoad, maxLoadTime, stepRate, graphPipe, emergencySignal):
    displacement = 0
    stepper = StepperController(DIR_PIN)
    ADC = ADCController()
    ADC.tare()
    try:
        
        # TODO: implement preloading and preload hold
        
        # move down to apply the main load
        load = ADC.getLoad()
        start = time.time()
        stepper.startMovingDown(stepRate)
        # move down until the target load is achieved
        while(load < maxLoad and not emergencySignal.is_set()):
            # log a data point
            displacement += stepper.getDisplacement()
            graphPipe.send([displacement, load*100])
            time.sleep(1 / SAMPLE_RATE)
            load = ADC.getLoad()
        displacement += stepper.stopMoving()

        print("time to apply load: " + str(time.time() - start))
        start = time.time()

        #TODO: update the displacement values here
        # once the target load is achieved, dwell at the target load for some time
        startTime = time.time()
        # while the dwell time has not elapsed
        while time.time() < (startTime + maxLoadTime) and not emergencySignal.is_set():
            graphPipe.send([displacement, load*100])
            time.sleep(1 / SAMPLE_RATE)
            load = ADC.getLoad()
            
            # move up if too much load is applied
            if load > (maxLoad + TOLERANCE):
                displacement += stepper.stopMoving()
                stepper.startMovingUp(stepRate/8)

            # move down is too little load is applied
            elif load < (maxLoad - TOLERANCE):
                displacement += stepper.stopMoving()
                stepper.startMovingDown(stepRate/8)

            # do nothing if the load is just right
            else:
                displacement += stepper.stopMoving()
            

        print("time spent dwelling: " + str(time.time() - start))
        start = time.time()

        # return the indenter head to its starting position, logging daa on the way
        stepper.startMovingUp(stepRate)
        # move the indenter up by the number of steps we moved it down
        while(displacement > 0 and not emergencySignal.is_set()):
            # log a data point
            displacement += stepper.getDisplacement()
            graphPipe.send([displacement, load*100])
            time.sleep(1 / SAMPLE_RATE)
            load = ADC.getLoad()
        stepper.stopMoving()
        
        print("time spent retracting (non-emerg): " + str(time.time() - start))
        start = time.time()

        # if we had an emergency, we still need to retract the indenter head
        if emergencySignal.is_set():
            stepper.emergencyStop(displacement, stepRate)
            
            print("time spent retracting (emerg): " + str(time.time() - start))

    # stop the indenter if any exceptions occur
    except Exception as e:
        stepper.emergencyStop(displacement, stepRate)
    
    # close the pipe to the graph before quitting the process
    finally:
        graphPipe.close()
    return
