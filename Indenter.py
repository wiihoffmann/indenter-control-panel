
#custom  class imports
from StepperController import *
from ADCController import *
from Logger import *
from MPLGrapher import *

#TODO: remove
import numpy as np

class Indenter():

    def __init__(self, MPLgraph):
        self.graph = MPLgraph
        
        # set up the motor controller and ADC controller
        self.Stepper = StepperController(12,16)
        self.ADC = ADCController()
        self.Logger = Logger()

        self.x = []
        self.step = []
        self.load = []


    def loadAndShowResults(self, filename):
        self.x, self.step, self.load = self.Logger.loadFile(filename)
        self.graph.plotData(self.x, self.step, self.load)


    def saveResults(self, filename):
        self.Logger.saveFile(filename, self.x, self.step, self.load)


    def compareResults(self, filename):
        # TODO: load data from another CSV and overlay it on the current graph
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
        global terminate
        # launch a thread to handle taking the stiffness measurement
        self.measurementLoop = threading.Thread(name = 'myDataLoop', target = measurementLoop, daemon = True, args = (self.addData_callbackFunc,))
        self.measurementLoop.start()


    def emergencyStop(self):
        global killMeasurement
        # terminate the thread doing the stiffness measurement
        killMeasurement = True

        # TODO: start backing off the indenter to the home position here

        print("stopped")


    def addData_callbackFunc(self, step, load):
        self.graph.addData(step, load)
        return


killMeasurement = False
def measurementLoop(addData_callbackFunc):
    global killMeasurement
    # Setup the signal-slot mechanism.
    mySrc = MPLGrapher.Communicate()
    mySrc.data_signal.connect(addData_callbackFunc)

    # Simulate some data
    n = np.linspace(0, 499, 500)
    y = 50 + 25*(np.sin(n / 8.3)) + 10*(np.sin(n / 7.5)) - 5*(np.sin(n / 1.5))
    i = 0
    killMeasurement = False
    while(not killMeasurement):
        if(i > 499):
            i = 0
        time.sleep(0.001)
        mySrc.data_signal.emit(12, y[i]) # <- Here you emit a signal!
        i += 1
    return