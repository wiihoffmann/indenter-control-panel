
#custom  class imports
from StepperController import *
from ADCController import *
from Logger import *

import random

class Indenter():

    def __init__(self, mplWidget):
        self.MPLWidget = mplWidget
        
        # set up the motor controller and ADC controller
        self.Stepper = StepperController(12,16)
        self.ADC = ADCController()
        self.Logger = Logger()

        self.x = []
        self.step = []
        self.load = []


    def loadAndShowResults(self, filename):
        self.x, self.step, self.load = self.Logger.loadFile(filename)
        self.MPLWidget.plotData(self.x, self.step, self.load)


    def saveResults(self, filename):
        self.Logger.saveFile(filename, self.x, self.step, self.load)


    def compareResults(self, filename):
        # to be implemented - load data from another CSV and overlay it on the current graph
        pass


    def startJogUp(self):
        self.Stepper.startMovingUp(1000)


    def stopJogUp(self):
        self.Stepper.stopMovingUp()


    def startJogDown(self):
        self.Stepper.startMovingDown(1000)


    def stopJogDown(self):
        self.Stepper.stopMovingDown()

    def takeStiffnessMeasurement(self, load):
        print("started")
        for i in range(100):
            self.MPLWidget.addDataPoint(i-1, random.randint(1, 50), random.randint(1, 50))
        print("done updating")

    def emergencyStop(self):
        print("stopped")