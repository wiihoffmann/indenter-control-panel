
import threading
import time

#custom class imports
from StepperController import *
from ADCController import *
from Logger import *
from Grapher import *
from hx711 import HX711

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
        self.Stepper.startMovingUp(2000)


    def stopJogging(self):
        self.Stepper.stopMoving()


    def startJogDown(self):
        self.Stepper.startMovingDown(2000)


    def takeStiffnessMeasurement(self, load):
        self.graph.clear()

        # launch a thread to handle taking the stiffness measurement
        #TODO: make sure that only one instance of this thread runs at a time!!!
        self.measurementLoopHandle = threading.Thread(name = 'measurementLoop', target = measurementLoop, args=(load, 1500, self.graph))
        self.measurementLoopHandle.start()


    def emergencyStop(self):
        global killMeasurement
        # terminate the thread doing the stiffness measurement
        killMeasurement = True

        # TODO: start backing off the indenter to the home position here
        self.Stepper.stopMoving()

        print("stopped")


    def shutdown(self):
        self.Stepper.stopMoving()



killMeasurement = False
displacement = 0
TOLERANCE = 50
def measurementLoop(targetLoad, stepRate, graph):
    global killMeasurement, displacement
    
    # set up the HX711
    hx = HX711(29, 31)
    hx.set_offset(8214368.3125)
    hx.set_scale(243.8564841498559)
    stepper = StepperController(16)
    displacement = 0
    killMeasurement = False
    
    try:
        # move down until the target load is achieved
        load = hx.get_grams()
        stepper.startMovingDown(stepRate)
        while(load < targetLoad and not killMeasurement):
            hx.power_down()
            time.sleep(.002)
            hx.power_up()
            load = hx.get_grams()
            graph.addDataPoint(stepper.getDisplacement(), load)

        displacement = stepper.stopMoving()
        
        # TODO: delete me once next section works properly
        time.sleep(2)
        
        # once the target load is achieved, dwell at the target load for some time
        # TODO: make sure load is maintained for the dwell time by moving the indenter up and down
        # startTime = time.time()
        # while time.time() < startTime + 2:
        #     hx.power_down()
        #     hx.power_up()
        #     load = hx.get_grams()
            
        #     if load > (targetLoad + TOLERANCE):
        #         # move up
        #         displacement += stepper.stopMoving()
        #         stepper.startMovingUp(stepRate)

        #     elif load < (targetLoad - TOLERANCE):
        #         # move down
        #         displacement += stepper.stopMoving()
        #         stepper.startMovingDown(stepRate)

        #     else:
        #         # stop moving
        #         displacement += stepper.stopMoving()
            
        #     # TODO: log new data point here
        #     #print(stepper.getDisplacement())

        # move the indenter up by the number of steps we moved it down
        # TODO: implement the above comment
        stepper.startMovingUp(stepRate)
        while(abs(displacement) > abs(stepper.getDisplacement()) and not killMeasurement):
            hx.power_down()
            time.sleep(.001)
            hx.power_up()
            load = hx.get_grams()
            
            graph.addDataPoint(displacement + stepper.getDisplacement(), load)
            
        stepper.stopMoving()
        
    except (KeyboardInterrupt, SystemExit):
        stepper.stopMoving()
        cleanAndExit()

    return