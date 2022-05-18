
from multiprocessing import Process, Pipe, Event
import RPi.GPIO as GPIO
import time

#custom class imports
from firmware.StepperController import *
from firmware.ADCController import *
from datalogger.Logger import *
from interface.LiveGrapher import *
import Config

DIR_PIN = 23  # physical pin 16, GPIO23
EMERG_STOP_PIN = 24 # GPIO24 for emergency stop button

class Indenter():
    """ The main controller class for the indenter.
    This class imlements the controller for the indenter. It allows for performing 
    measurements, loading/saving data, homing the indenter head, emergency stop, etc.
    """

    def __init__(self, graph):
        """ Creates a new instance of the indenter controller.
        Parameters:
            graph: A reference to the graph widget in the interface """
        
        # the graph object in the UI
        self.graph = LiveGrapher(graph)

        # set up the stepper controller and data logger
        self.Stepper = StepperController(DIR_PIN) #physical pin 16, GPIO23
        self.Logger = Logger()

        # used to kill a measurement in an emergency
        self.emergencySignal = Event()
        # process handle for the measurement loop
        self.measurementHandle = None

        # set up emergency stop button
        GPIO.setmode(GPIO.BCM)  # Use GPIO pin numbering (as opposed to header pin number)
        GPIO.setup(EMERG_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(EMERG_STOP_PIN, GPIO.FALLING, callback=self.emergencyStop, bouncetime=100)
        return


    def loadAndShowResults(self, filename):
        """ Given a file name, load the data in the file and show it in
        the graph area of the UI. 
        Parameters:
            filename (str): the name of the file to load data from"""
        
        self.graph.clear()
        data = self.Logger.loadFile(filename)
        self.graph.setData(data)
        return


    def saveResults(self, filename):
        """ Saves the measurement data to a file.
        Parameters:
            filename (str): the name of the file to save data to """

        data = self.graph.getData()
        self.Logger.saveFile(filename, data)
        return


    def clearResults(self):
        """ Clears the graph area of the UI. """
        self.graph.clear()
        return


    def startJogUp(self):
        """ Starts manually jogging the indenter head upwards. """
        
        self.Stepper.startMovingUp(Config.JOG_SPEED)
        return


    def stopJogging(self):
        """ Starts manually jogging the indenter head downwards. """

        self.Stepper.stopMoving()
        return


    def startJogDown(self):
        """ Stops the manual jogging of the indenter head. """

        self.Stepper.startMovingDown(Config.JOG_SPEED)
        return


    def changeView(self):
        self.graph.cycleViews()


    def takeStiffnessMeasurement(self, preload, preloadTime, maxLoad, maxLoadTime, stepRate, doneSignal):
        """ Initiates the process of taking a new stffness measurement.
        Parameters:
            preload (int): how much preload to apply (newtons)
            preloadTime (int): how long to keep the preload applied (seconds)
            maxLoad (int): the full load to apply (newtons)
            maxLoadTime (int): how long to keep the max load applied (seconds)
            stepRate (int): how fast to move the indenter head (steps/second)"""

        # only start a measurement if one is not currently running
        if self.measurementHandle == None or not self.measurementHandle.is_alive():
            self.graph.setupTimeSeries()
            self.graph.clear()
            
            # clear emergency stop state and establish a pipe to send data to the graph
            self.emergencySignal.clear()
            parentGraphPipe, childGraphPipe = Pipe()
            self.graph.addDataFromPipe(parentGraphPipe)

            # launch a process to handle taking the stiffness measurement
            self.measurementHandle = Process(name = 'measurementLoop', target = measurementLoop, args=(preload, preloadTime, maxLoad, maxLoadTime, stepRate, childGraphPipe, self.emergencySignal, doneSignal))
            self.measurementHandle.start()
        return


    def emergencyStop(self, *args):
        """ Defines the emergency stop procedure. """

        # terminate the process doing the stiffness measurement
        self.emergencySignal.set()
        return



def applyLoad(displacement, target, stepRate, ADC, stepper, graphPipe, emergencySignal):
    """ Moves the indenter head down to apply a target load
    Parameters:
        displacement (int): the current displacement of the indenter head
        target (int): the load we wish to maintain (newtons)
        stepRate (int): how fast to move the indenter head (steps/second)
        ADC (ADCController): the ADC to get load data from
        stepper (StepperController): the stepper we want to control
        graphPipe (Pipe): the pipe used to send data into the graph process
        emergencySignal (Event): a signal used to start an emergency stop.
    Returns:
        displacement (int): the displacement of the indenter head"""

    load = ADC.getLoad()
    stepper.startMovingDown(stepRate)
    # move down until the target load is achieved
    while(load < target and not emergencySignal.is_set()):
        # log a data point
        displacement += stepper.getDisplacement()
        graphPipe.send([displacement/100, load])
        time.sleep(1 / Config.SAMPLE_RATE)
        load = ADC.getLoad()
        
    displacement += stepper.stopMoving()
    return displacement


def dwell(displacement, target, dwellTime, ADC, stepper, graphPipe, emergencySignal):
    """ Once the target load is achieved, dwell at the target load for some time and collect data.
    Parameters:
        displacement (int): the current displacement of the indenter head
        target (int): the load we wish to maintain (newtons)
        dwellTime (int): how long to keep the target load applied for (seconds)
        ADC (ADCController): the ADC to get load data from
        stepper (StepperController): the stepper we want to control
        graphPipe (Pipe): the pipe used to send data into the graph process
        emergencySignal (Event): a signal used to start an emergency stop.
    Returns:
        displacement (int): the displacement of the indenter head"""

    startTime = time.time()
    # while the dwell time has not elapsed
    while time.time() < (startTime + dwellTime) and not emergencySignal.is_set():
        # log a data point
        time.sleep(1 / Config.SAMPLE_RATE)
        load = ADC.getLoad()
        graphPipe.send([displacement/100, load])
        
        # move up if too much load is applied and we're not already moving up
        if load > (target + Config.TOLERANCE) and stepper.getDirection() != -1:
            displacement += stepper.stopMoving()
            stepper.startMovingUp(Config.HOLD_STEP_UP_RATE)

        # move down is too little load is applied and we're not already moving down
        elif load < (target - Config.TOLERANCE) and stepper.getDirection() != 1:
            displacement += stepper.stopMoving()
            stepper.startMovingDown(Config.HOLD_STEP_DOWN_RATE)

        # do nothing if the load is just right
        elif load >= (target - Config.TOLERANCE) and load <= (target + Config.TOLERANCE):
            displacement += stepper.stopMoving()

        # else just keep recording data
        else:
            displacement += stepper.getDisplacement()
    return displacement


def retract(displacement, stepRate, ADC, stepper, graphPipe, emergencySignal):
    """ Retracts the indenter head back to the starting position, logging data on the way.
    Parameters:
        displacement (int): the current displacement of the indenter head
        stepRate (int): how fast to move the indenter head (steps/second)
        ADC (ADCController): the ADC to get load data from
        stepper (StepperController): the stepper we want to control
        graphPipe (Pipe): the pipe used to send data into the graph process
        emergencySignal (Event): a signal used to start an emergency stop.
    Returns:
        displacement (int): the displacement of the indenter head (should be 0)"""

    stepper.startMovingUp(stepRate)
    # move the indenter up by the number of steps we moved it down
    while(displacement > 0 and not emergencySignal.is_set()):
        # log a data point
        time.sleep(1 / Config.SAMPLE_RATE)
        displacement += stepper.getDisplacement()
        load = ADC.getLoad()
        graphPipe.send([displacement/100, load])
    
    stepper.stopMoving()
    return displacement


def measurementLoop(preload, preloadTime, maxLoad, maxLoadTime, stepRate, graphPipe, emergencySignal, doneSignal):
    """ The process which performs the stiffness measurement.
    Parameters:
        preload (int): how much preload to apply (newtons)
        preloadTime (int): how long to keep the preload applied (seconds)
        maxLoad (int): the full load to apply (newtons)
        maxLoadTime (int): how long to keep the max load applied (seconds)
        stepRate (int): how fast to move the indenter head (steps/second)
        graphPipe (Pipe): the pipe used to send data into the graph process
        emergencySignal (Event): a signal used to start an emergency stop."""
    
    try:
        displacement = 0
        stepper = StepperController(DIR_PIN)
        ADC = ADCController()
        ADC.tare()

        # apply preload
        displacement = applyLoad(displacement, preload, stepRate, ADC, stepper, graphPipe, emergencySignal)
        # preload dwell
        displacement = dwell(displacement, preload, preloadTime, ADC, stepper, graphPipe, emergencySignal)
        # apply main load
        displacement = applyLoad(displacement, maxLoad, stepRate, ADC, stepper, graphPipe, emergencySignal)
        # main load dwell
        displacement = dwell(displacement, maxLoad, maxLoadTime, ADC, stepper, graphPipe, emergencySignal)
        # retract
        displacement = retract(displacement, stepRate, ADC, stepper, graphPipe, emergencySignal)

        # if we had an emergency, we still need to retract the indenter head
        if emergencySignal.is_set():
            #displacement += stepper.stopMoving()
            stepper.emergencyStop(displacement, Config.EMERGENCY_STOP_STEP_RATE)

    # stop the indenter if any exceptions occur
    except Exception as e:
        displacement += stepper.stopMoving()
        stepper.emergencyStop(displacement, Config.EMERGENCY_STOP_STEP_RATE)
        print(e)
    
    # close the pipe to the graph before quitting the process
    finally:
        graphPipe.close()
        doneSignal.set() 
    return

