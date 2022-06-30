
from multiprocessing import Process, Pipe, Event

#custom class imports
from firmware.Communicator import *
from dataTools.Logger import *
from dataTools.MeasurementParams import *
from graphTools.LiveGrapher import *
import dataTools.UnitConverter as uc
import Config

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

        # set up the communicator and data logger
        self.comm = Communicator()
        self.Logger = Logger()

        # used to kill a measurement in an emergency
        self.emergencySignal = Event()
        # process handle for the measurement loop
        self.measurementHandle = None
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

        self.comm.moveZAxisUp(Config.JOG_SPEED)
        return


    def stopJogging(self):
        """ Starts manually jogging the indenter head downwards. """

        self.comm.stopZAxis()
        return


    def startJogDown(self):
        """ Stops the manual jogging of the indenter head. """

        self.comm.moveZAxisDown(Config.JOG_SPEED)
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
            
            # pack all of the measurement parameters
            params = MeasurementParams(0,0,0,0,0)
            params.preload = int(uc.NewtonToRawADC(preload))
            params.preloadTime = int(preloadTime * 1000) # convert seconds to millis
            params.maxLoad = int(uc.NewtonToRawADC(maxLoad))
            params.maxLoadTime = int(maxLoadTime * 1000) # convert seconds to millis
            params.stepDelay = int(uc.stepRateToMicros(stepRate))

            # launch a process to handle taking the stiffness measurement
            self.measurementHandle = Process(name = 'measurementLoop', target = measurementLoop, args=(params, self.comm, childGraphPipe, self.emergencySignal, doneSignal))
            self.measurementHandle.start()
        return


    def emergencyStop(self, *args):
        """ Defines the emergency stop procedure. """

        # terminate the process doing the stiffness measurement
        self.emergencySignal.set()
        return


def measurementLoop(params, comm:Communicator, graphPipe, emergencySignal, doneSignal):
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
        comm.sendMeasurementBegin(params)

        command = comm.readCommand()
        while(command != 'C'):
            if(command == 'D'):
                graphPipe.send(comm.readDataPoint())
            else:
                print("Got unexpected command while performing measurement! Got command: " + command)
            command = comm.readCommand()

    # stop the indenter if any exceptions occur
    except Exception as e:
        # displacement += stepper.stopMoving()
        # stepper.emergencyStop(displacement, Config.EMERGENCY_STOP_STEP_RATE)
        print(e)
    
    # close the pipe to the graph before quitting the process
    finally:
        graphPipe.close()
        doneSignal.set() 
    return

