
from multiprocessing import Process, Queue

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

        # process handle for the measurement loop
        self.measurementHandle = None
        
        self.lastTestType = bytes("", 'utf-8')
        return


    def getLastTestType(self):
        return self.lastTestType


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
        dataset = self.graph.getData()
        self.Logger.saveFile(dataset, filename)
        return
    

    def clearResults(self):
        """ Clears the graph area of the UI. """
        self.graph.clear()
        return


    def changeView(self):
        self.graph.cycleViews()


    def emergencyStop(self, *args):
        """ Defines the emergency stop procedure. """
        self.comm.emergencyStop(Config.EMERGENCY_STOP_STEP_RATE)
        return


    def measurementInProgress(self):
        return self.measurementHandle != None and self.measurementHandle.is_alive()


    def takeStiffnessMeasurement(self, preload, preloadTime, maxLoad, maxLoadTime, stepRate, doneSignal, iterations, measurementType):
        """ Initiates the process of taking a new stffness measurement.
        Parameters:
            preload (int): how much preload to apply (newtons)
            preloadTime (int): how long to keep the preload applied (seconds)
            maxLoad (int): the full load to apply (newtons)
            maxLoadTime (int): how long to keep the max load applied (seconds)
            stepRate (int): how fast to move the indenter head (steps/second)"""

        # only start a measurement if one is not currently running
        if self.measurementHandle == None or not self.measurementHandle.is_alive():
            self.lastTestType = measurementType
            
            self.graph.setupTimeSeries()
            self.graph.clear()

            dataQueue = Queue()
            self.graph.addDataFromPipe(dataQueue)
            
            # pack all of the measurement parameters
            params = MeasurementParams(0,0,0,0,0, firmware.Communicator.REGULAR_TEST_CODE)
            params.preload = int(uc.NewtonToRawADC(preload))
            params.preloadTime = int(preloadTime * 1000) # convert seconds to millis
            params.maxLoad = int(uc.NewtonToRawADC(maxLoad))
            params.maxLoadTime = int(maxLoadTime * 1000) # convert seconds to millis
            params.stepDelay = int(uc.stepRateToMicros(stepRate))
            params.iterations = iterations
            params.testType = measurementType

            # launch a process to handle taking the stiffness measurement
            self.measurementHandle = Process(name = 'measurementLoop', target = measurementLoop, args=(params, self.comm, dataQueue, doneSignal))
            self.measurementHandle.start()
        return



def measurementLoop(params, comm, dataQueue, doneSignal):
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
        while command != MEASUREMENT_COMPLETE_CODE:
            # data point
            if command == REGULAR_DATA_POINT_CODE:
                dataQueue.put(REGULAR_DATA_POINT_CODE)
                dataQueue.put(comm.readDataPoint())
            elif command == DATA_POINT_WITH_BUTTON_STATE_CODE:
                dataQueue.put(DATA_POINT_WITH_BUTTON_STATE_CODE)
                
                pass
            elif command == DATA_POINT_WITH_VAS_CODE:
                dataQueue.put(DATA_POINT_WITH_VAS_CODE)
                
                # TODO: implement me
                
                pass
            # split collected data
            elif command == NEW_TEST_BEGIN_CODE:
                dataQueue.put(NEW_TEST_BEGIN_CODE)
                
                # TODO: implement me
                
            else:
                print("Got unexpected command while performing measurement! Got command: " + command)
            command = comm.readCommand()

    # stop the indenter if any exceptions occur
    except Exception as e:
        print(e)
    
    # close the pipe to the graph before quitting the process
    finally:
        dataQueue.put(None)
        doneSignal.set()
    return

