from PyQt5 import QtCore
import pyqtgraph as pg
import threading

REFRESH_DELAY = 250 # ms

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
        self.orangePen = pg.mkPen('r', width=3)
        self.bluePen = pg.mkPen('b', width=3)

        # set up the graph area
        self.graph.setBackground('w')
        self.graph.setLabel('left', 'Displacement', units ='steps')
        self.graph.setLabel('right', 'Force', units ='N')
        self.graph.setLabel('bottom', 'Sample number')

        # add the two data series for load and displacement data
        self.loadLine =  self.graph.plot([], [], pen=self.orangePen)
        self.stepLine =  self.graph.plot([], [], pen=self.bluePen)

        # set up a process for refreahing the graph with newly collected data
        self.timer = QtCore.QTimer()
        self.timer.setInterval(REFRESH_DELAY)
        self.timer.timeout.connect(self.refreshPlot)
        self.timer.start()
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


    def setData(self, x, step, load):
        """ Sets all of the data for the series in the graph.
        Parameters:
            x (int): array of sample numbers to be graphed
            step (int): array of displacement data to be graphed
            load (fload): array of load data to be graphed """

        self.lock.acquire()
        self.xData = x
        self.stepData = step
        self.loadData = load
        self.loadLine.setData(self.xData, self.loadData, pen=self.orangePen)
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