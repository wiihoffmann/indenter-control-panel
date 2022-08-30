
from PyQt5 import QtCore
import threading
import copy

import dataTools.UnitConverter as uc
from graphTools.Grapher import *
from interface.SignalConnector import *
import Config



class LiveGrapher(Grapher):
    """ A class for plotting collected data into the graph are of the UI.
        This class allows for graphing data as its collected, graphing old data,
        and clearing the graph. """

    def __init__(self, graphHandle):
        """ Creates a new grapher object for visualizing collected data.
        Parameters:
            graphHandle: The pyqtplot widget used in the UI """
        super().__init__(graphHandle)

        # set up line colors
        self.redPen = pg.mkPen('r', width=Config.GRAPH_LINE_WIDTH)
        self.bluePen = pg.mkPen('b', width=Config.GRAPH_LINE_WIDTH)

        self.data = [MeasurementData([],[],[],[])]
        self.testIndex = 0
        # add the two data series for load and displacement data
        self.loadLines.append(self.graph.plot(self.data[self.testIndex].sample, self.data[self.testIndex].load, pen=self.redPen))
        self.stepLines.append(self.graph.plot(self.data[self.testIndex].sample, self.data[self.testIndex].step, pen=self.bluePen))
        self.loadStepLines.append(self.graph.plot(self.data[self.testIndex].step, self.data[self.testIndex].load, pen=self.redPen))
        self.lock = threading.Lock() # lock for controlling access to graph data

        # default to time series when setting up the graph axes
        self.setupTimeSeries()
        return


    def setupTimeSeries(self):
        super().setupTimeSeries()
        self.refreshPlot()
        return


    def setupLoadDisplacementGraph(self):
        super().setupLoadDisplacementGraph()
        self.refreshPlot()
        return


    def startLiveUpdate(self):
        # set up a process for refreshing the graph with newly collected data
        self.timer = QtCore.QTimer()
        self.timer.setInterval(Config.GRAPH_REFRESH_DELAY)
        self.timer.timeout.connect(self.refreshPlot)
        self.timer.start()
        print("timer started")


    def stopLiveUpdate(self):
        self.timer.stop()
        self.refreshPlot()


    def refreshPlot(self):
        """ Refreshes the graph display with any newly collected data. """
        self.lock.acquire()
        # if we are showing a time series
        if(self.view == 0):
            self.loadLines[0].setData(self.data[0].sample[::Config.GRAPH_POINT_SKIP], self.data[0].load[::Config.GRAPH_POINT_SKIP])
            self.stepLines[0].setData(self.data[0].sample[::Config.GRAPH_POINT_SKIP], self.data[0].step[::Config.GRAPH_POINT_SKIP])
        # if we are showing the force as a function of displacement
        elif(self.view == 1):
            self.loadStepLines[0].setData(self.data[0].step[::Config.GRAPH_POINT_SKIP], self.data[0].load[::Config.GRAPH_POINT_SKIP])
        self.lock.release()
        return


    def addDataPoint(self, dataPoint):
        """ Adds a single data point to the end of the graph.
        Parameters:
            step (int): the displacemet for this data point
            load (float): the load value for this data point """

        self.lock.acquire()

        # if this is the first data point in the series
        if self.data[0].sample == []:
            self.data[0].sample.append(1)
        # else increment the sample number by 1 and append
        else:
            self.data[0].sample.append(self.data[0].sample[-1] +1)
        
        self.data[0].step.append(dataPoint[0])
        self.data[0].load.append(dataPoint[1])
        self.data[0].phase.append(dataPoint[2])


        # if we are doing multiple tests, add the data into its own trial too
        if self.testIndex > 0:
            # if this is the first data point in the series
            if self.data[self.testIndex].sample == []:
                self.data[self.testIndex].sample.append(1)
            # else increment the sample number by 1 and append
            else:
                self.data[self.testIndex].sample.append(self.data[self.testIndex].sample[-1] +1)
            
            self.data[self.testIndex].step.append(dataPoint[0])
            self.data[self.testIndex].load.append(dataPoint[1])
            self.data[self.testIndex].phase.append(dataPoint[2])

        self.lock.release()
        return


    def addDataFromPipe(self, dataQueue):
        """ Starts a process to add data points to the end of the graph from a pipe.
        Parameters:
            pipe (Pipe): the pipe to read data from """

        # start performing live updates to the graph screen
        self.startLiveUpdate()

        # set up a signal handler to stop live updates when the pipe closes
        self.signalManager = SignalConnector()
        self.signalManager.connect(self.stopLiveUpdate)
        self.signalManager.start()

        # start the thread to accept data over the pipe
        self.pipeManagerhandle= threading.Thread(name = 'pipeManager', target = pipeManager, args=(self, dataQueue, self.signalManager))
        self.pipeManagerhandle.start()
        return


    def setData(self, graphData):
        """ Sets all of the data for the series in the graph.
        Parameters:
            x (int): array of sample numbers to be graphed
            step (float): array of displacement data to be graphed
            load (float): array of load data to be graphed """

        self.lock.acquire()
        self.data = [graphData]
        self.loadLines[0].setData(self.data[0].sample, self.data[0].load)
        self.stepLines[0].setData(self.data[0].sample, self.data[0].step)
        self.loadStepLines[0].setData(self.data[0].step, self.data[0].load)
        self.lock.release()
        
        # default back to a time series
        self.setupTimeSeries()
        return


    def getData(self):
        """ Gets all of the data currently shown in the graph.
        Returns:
            xData (int): array of sample numbers
            stepData (int): array of displacement data
            loadData (fload): array of load data """

        return self.data


    def splitTestData(self):
        print("live grapher got the N")
        # if this is the first split, copy the first trial before splitting
        if self.testIndex == 0:
            self.data.append(copy.deepcopy(self.data[0]))
            self.testIndex += 1

        self.data.append(MeasurementData([],[],[],[]))
        self.testIndex += 1
        return


    def clear(self):
        """ Clears the collected data and the graph area. """

        self.lock.acquire()
        super().clear()
        self.data = [MeasurementData([],[],[],[])]
        self.testIndex = 0
        self.loadLines.append(self.graph.plot(self.data[self.testIndex].sample, self.data[self.testIndex].load, pen=self.redPen))
        self.stepLines.append(self.graph.plot(self.data[self.testIndex].sample, self.data[self.testIndex].step, pen=self.bluePen))
        self.loadStepLines.append(self.graph.plot(self.data[self.testIndex].step, self.data[self.testIndex].load, pen=self.redPen))
        self.lock.release()
        self.refreshPlot()
        return



def pipeManager(self, dataQueue, pipeEndSignal):
    """ The thread function responsible for loading data from the pipe and 
    plotting it to the graph area. """
    rawData = None
    done = False # pipe EOF
    while not done:          
        # graph the data waiting in the pipe
        try:
            data = dataQueue.get()
            if data == None: 
                done = True
            elif data == 'D':
                rawData = list(dataQueue.get())
                rawData[0] = rawData[0] / 100 # scale the displacement
                rawData[1] = uc.rawADCToNewton(rawData[1]) # convert load from adc reading to newtons
                self.addDataPoint(rawData)
            elif data == 'N':
                self.splitTestData()

        except Exception as e:
            print(e)
    pipeEndSignal.setAsyncSignal()
    return