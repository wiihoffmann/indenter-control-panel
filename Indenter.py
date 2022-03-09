
import threading
import time

#custom class imports
from StepperController import *
from ADCController import *
from Logger import *
from Grapher import *

#TODO: remove
import numpy as np

class Indenter():

    def __init__(self, graph):
        self.graph = Grapher(graph)
        
        # set up the motor controller and ADC controller
        self.Stepper = StepperController(16)
        self.ADC = ADCController()
        self.Logger = Logger()


    def loadAndShowResults(self, filename):
        x, step, load = self.Logger.loadFile(filename)
        self.graph.setData(x, step, load)


    def saveResults(self, filename):
        x, step, load = self.graph.getData()
        self.Logger.saveFile(filename, x, step, load)


    def clearResults(self):
        self.graph.clear()

    def compareResults(self, filename):
        # TODO: load data from another CSV and overlay it on the current graph
        pass


    def startJogUp(self):
        self.Stepper.startMovingUp(1000)


    def stopJogging(self):
        self.Stepper.stopMoving()


    def startJogDown(self):
        self.Stepper.startMovingDown(1000)


    def takeStiffnessMeasurement(self, load):
        global terminate
        self.graph.clear()
        time.sleep(1)
        # launch a thread to handle taking the stiffness measurement
        self.measurementLoop = threading.Thread(name = 'myDataLoop', target = measurementLoop, daemon = True, args = (self.graph,))
        self.measurementLoop.start()


    def emergencyStop(self):
        global killMeasurement
        # terminate the thread doing the stiffness measurement
        killMeasurement = True

        # TODO: start backing off the indenter to the home position here

        print("stopped")


killMeasurement = False
def measurementLoop(graph):
    global killMeasurement

    logger = Logger()
    x, step, load = logger.loadFile("./samples/2021-12-5-15-19-34.csv")

    killMeasurement = False
    i=0
    while(not killMeasurement):
        if(i >= x[-1]):
            killMeasurement = True
        graph.addDataPoint(step[i], load[i])
        time.sleep(0.001)
        i += 1
    return