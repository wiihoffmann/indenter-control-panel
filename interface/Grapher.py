
from PyQt5 import QtCore
import pyqtgraph as pg
import threading

import Config


class Grapher():
    """ A class for plotting collected data into the graph are of the UI.
        This class allows for graphing data as its collected, graphing old data,
        and clearing the graph. """

    def __init__(self, graphHandle):
        """ Creates a new grapher object for visualizing collected data.
        Parameters:
            graphHandle: The pyqtplot widget used in the UI """

        self.graph = graphHandle
        self.xData = []
        self.stepData = []
        self.loadData = []
        self.lock = threading.Lock() # lock for controlling access to graph data
        
        # set up line colors
        self.redPen = pg.mkPen('r', width=3)
        self.bluePen = pg.mkPen('b', width=3)

        # add the two data series for load and displacement data
        self.loadLine = self.graph.plot(self.xData, self.loadData, pen=self.redPen)
        self.stepLine = self.graph.plot(self.xData, self.stepData, pen=self.bluePen)

        # set up a process for refreshing the graph with newly collected data
        self.timer = QtCore.QTimer()
        self.timer.setInterval(Config.GRAPH_REFRESH_DELAY)
        self.timer.timeout.connect(self.refreshPlot)
        self.timer.start()

        # default to time series when setting up the graph axes
        self.setupTimeSeries()
        return
    

    def setupTimeSeries(self):
        print("making time series graph")

        # update current view type
        self.view = 0

        # set up the graph area
        self.graph.setBackground('w')
        self.graph.setLabel('left', 'Displacement (x100)', units ='steps')
        self.graph.setLabel('right', 'Force', units ='N')
        self.graph.setLabel('bottom', 'Sample number')

        # add the two data series for load and displacement data
        self.loadLine.setData(self.xData, self.loadData, pen=self.redPen)
        self.stepLine.setData(self.xData, self.stepData, pen=self.bluePen)
        
        # make sure the update timer is running
        self.timer.start()
        return


    def setupLoadDisplacementGraph(self):
        print("making load displacement graph")
        
        # don't auto update the graph data
        self.timer.stop()

        # update current view type
        self.view = 1

        # set up the graph area
        self.graph.setBackground('w')
        self.graph.setLabel('left', 'Force', units ='N')
        self.graph.setLabel('right', '', units ='')
        self.graph.setLabel('bottom', 'Displacement (x100)', units ='steps')
        
        # add the two data series for load and displacement data
        self.loadLine.setData(self.stepData, self.loadData, pen=self.redPen)
        self.stepLine.setData([], [], pen=self.bluePen)
        return


    def cycleViews(self):
        # toggle to time series
        if self.view == 0:
            self.setupLoadDisplacementGraph()
        # toggle to load as function of displacement
        elif self.view == 1:
            self.setupTimeSeries()

        # make sure the data is in range
        self.graph.getPlotItem().enableAutoRange()
        return


    def refreshPlot(self):
        """ Refreshes the graph display with any newly collected data. """

        self.lock.acquire()
        self.loadLine.setData(self.xData, self.loadData)
        self.stepLine.setData(self.xData, self.stepData)
        self.lock.release()
        return


    def addDataPoint(self, step, load):
        """ Adds a single data point to the end of the graph.
        Parameters:
            step (int): the displacemet for this data point
            load (float): the load value for this data point """

        self.lock.acquire()
        # if this is the first data point in the series
        if self.xData == []:
            self.xData.append(1)
        # else increment the sample number by 1 and append
        else:
            self.xData.append(self.xData[-1]+1)

        self.stepData.append(step)
        self.loadData.append(load)
        self.lock.release()
        return


    def addDataFromPipe(self, pipe):
        """ Starts a process to add data points to the end of the graph from a pipe.
        Parameters:
            pipe (Pipe): the pipe to read data from """

        self.pipeManagerhandle= threading.Thread(name = 'pipeManager', target = pipeManager, args=(self, pipe))
        self.pipeManagerhandle.start()
        return


    def setData(self, x, step = [], load = []):
        """ Sets all of the data for the series in the graph.
        Parameters:
            x (int): array of sample numbers to be graphed
            step (int): array of displacement data to be graphed
            load (fload): array of load data to be graphed """
        # default back to a time series
        self.setupTimeSeries()

        self.lock.acquire()
        self.xData = x
        self.stepData = step
        self.loadData = load
        self.loadLine.setData(self.xData, self.loadData, pen=self.redPen)
        self.stepLine.setData(self.xData, self.stepData, pen=self.bluePen)
        self.lock.release()
        return


    def getData(self):
        """ Gets all of the data currently shown in the graph.
        Returns:
            xData (int): array of sample numbers
            stepData (int): array of displacement data
            loadData (fload): array of load data """

        return self.xData, self.stepData, self.loadData


    def clear(self):
        """ Clears the collected data and the graph area. """
        self.setupTimeSeries()
        self.graph.getPlotItem().enableAutoRange()

        self.lock.acquire()
        self.xData = []
        self.stepData = []
        self.loadData = []
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