
from multiprocessing import Process, Pipe, Event
import time

#custom class imports
from firmware.StepperController import *
from firmware.ADCController import *
from datalogger.Logger import *
from interface.Grapher import *
from firmware.hx711 import HX711


JOG_SPEED = 2000
TOLERANCE = 1
DIR_PIN = 23


class Indenter():

    def __init__(self, graph):
        # the graph object in the UI
        self.graph = Grapher(graph)
        
        # set up the stepper controller and ADC controller
        self.Stepper = StepperController(DIR_PIN)
        self.ADC = ADCController()
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
    
    # set up the HX711
    average = 1
    hx = HX711(5,6)
    hx.set_offset(8214368.3125)
    hx.set_scale(243.8564841498559)
    hx.tare()
    
    try:
        start = time.time()
        # TODO: implement preloading and preload hold

        # move down to apply the main load
        load = hx.get_grams(average) /1000*9.81
        stepper.startMovingDown(stepRate)
        # move down until the target load is achieved
        while(load < maxLoad and not emergencySignal.is_set()):
            hx.power_down()
            time.sleep(.005)
            hx.power_up()
            load = hx.get_grams(average) /1000*9.81
            # log a data point
            graphPipe.send([stepper.getDisplacement(), load*100])
        displacement = stepper.stopMoving()
        
        print("time to apply load: " + str(time.time() - start))
        start = time.time()

        #TODO: update the displacement values here
        # once the target load is achieved, dwell at the target load for some time
        startTime = time.time()
        # while the dwell time has not elapsed
        while time.time() < (startTime + maxLoadTime) and not emergencySignal.is_set():
            hx.power_down()
            time.sleep(.005)
            hx.power_up()
            load = hx.get_grams(average) /1000*9.81
            
            # move up if too much load is applied
            if load > (maxLoad + TOLERANCE):
                stepper.stopMoving()
                stepper.startMovingUp(stepRate/8)

            # move down is too little load is applied
            elif load < (maxLoad - TOLERANCE):
                stepper.stopMoving()
                stepper.startMovingDown(stepRate/8)

            # do nothing if the load is just right
            else:
                stepper.stopMoving()
            
            # log a data point
            graphPipe.send([displacement, load*100])

        print("time spent dwelling: " + str(time.time() - start))
        start = time.time()

        # return the indenter head to its starting position, logging daa on the way
        stepper.startMovingUp(stepRate)
        # move the indenter up by the number of steps we moved it down
        while(abs(displacement) > abs(stepper.getDisplacement()) and not emergencySignal.is_set()):
            hx.power_down()
            time.sleep(.005)
            hx.power_up()
            load = hx.get_grams(average) /1000*9.81

            # log a data point
            graphPipe.send([displacement + stepper.getDisplacement(), load*100])
        stepper.stopMoving()
        
        print("time spent retracting (non-emerg): " + str(time.time() - start))
        start = time.time()

        # if we had an emergency, we still need to retract the indenter head
        if emergencySignal.is_set():
            stepper.emergencyStop(displacement, stepRate)
            
            print("time spent retracting (emerg): " + str(time.time() - start))
            start = time.time()

    # stop the indenter if any exceptions occur
    except Exception as e:
        stepper.emergencyStop(displacement, stepRate)
    
    # close the pipe to the graph before quitting the process
    finally:
        graphPipe.close()
        
    return