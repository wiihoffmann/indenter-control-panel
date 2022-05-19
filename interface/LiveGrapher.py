
from PyQt5 import QtCore
import threading

from interface.Grapher import *
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

        self.data = MeasurementData([],[],[])
        self.lock = threading.Lock() # lock for controlling access to graph data
        
        # add the two data series for load and displacement data
        self.loadLine = self.graph.plot(self.data.sample, self.data.load, pen=self.redPen)
        self.stepLine = self.graph.plot(self.data.sample, self.data.step, pen=self.bluePen)

        # set up a process for refreshing the graph with newly collected data
        self.timer = QtCore.QTimer()
        self.timer.setInterval(Config.GRAPH_REFRESH_DELAY)
        self.timer.timeout.connect(self.refreshPlot)
        self.timer.start()

        # default to time series when setting up the graph axes
        self.setupTimeSeries()
        return
    

    def setupTimeSeries(self):

        super().setupTimeSeries()

        # add the two data series for load and displacement data
        self.loadLine.setData(self.data.sample, self.data.load, pen=self.redPen)
        self.stepLine.setData(self.data.sample, self.data.step, pen=self.bluePen)       

        # make sure the update timer is running
        self.timer.start()
        return


    def setupLoadDisplacementGraph(self):
        
        # don't auto update the graph data
        self.timer.stop()

        super().setupLoadDisplacementGraph()

        # add the two data series for load and displacement data
        self.loadLine.setData(self.data.step, self.data.load, pen=self.redPen)
        self.stepLine.clear()
        return


    def startLiveUpdate(self):
        self.timer.start()


    def stopLiveUpdate(self):
        self.timer.stop()


    def refreshPlot(self):
        """ Refreshes the graph display with any newly collected data. """

        self.lock.acquire()
        self.loadLine.setData(self.data.sample, self.data.load)
        self.stepLine.setData(self.data.sample, self.data.step)
        self.lock.release()
        return


    def addDataPoint(self, step, load):
        """ Adds a single data point to the end of the graph.
        Parameters:
            step (int): the displacemet for this data point
            load (float): the load value for this data point """

        self.lock.acquire()
        # if this is the first data point in the series
        if self.data.sample == []:
            self.data.sample.append(1)
        # else increment the sample number by 1 and append
        else:
            self.data.sample.append(self.data.sample[-1]+1)

        self.data.step.append(step)
        self.data.load.append(load)
        self.lock.release()
        return


    def addDataFromPipe(self, pipe):
        """ Starts a process to add data points to the end of the graph from a pipe.
        Parameters:
            pipe (Pipe): the pipe to read data from """

        self.pipeManagerhandle= threading.Thread(name = 'pipeManager', target = pipeManager, args=(self, pipe))
        self.pipeManagerhandle.start()
        return


    def setData(self, graphData):
        """ Sets all of the data for the series in the graph.
        Parameters:
            x (int): array of sample numbers to be graphed
            step (float): array of displacement data to be graphed
            load (float): array of load data to be graphed """
        # default back to a time series
        self.setupTimeSeries()

        self.lock.acquire()
        self.data = graphData
        self.loadLine.setData(self.data.sample, self.data.load)
        self.stepLine.setData(self.data.sample, self.data.step)
        self.lock.release()
        return


    def clear(self):
        """ Clears the collected data and the graph area. """

        self.lock.acquire()
        super().clear()
        self.data = MeasurementData([],[],[])
        self.loadLine.clear()
        self.stepLine.clear()
        self.lock.release()
        return



def pipeManager(self, pipe):
    """ The thread function responsible for loading data from the pipe and 
    plotting it to the graph area. """

    done = False # pipe EOF
    while not done:          
        # graph the data waiting in the pipe
        try:
            step, data = pipe.recv()
            self.addDataPoint(step, data)
        except EOFError:
            done = True
    return