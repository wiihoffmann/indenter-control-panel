
from interface.Grapher import *


class ComparisonGrapher(Grapher):
    """ A class for plotting collected data into the graph are of the UI.
        This class allows for graphing data as its collected, graphing old data,
        and clearing the graph. """

    def __init__(self, graphHandle):
        """ Creates a new grapher object for visualizing collected data.
        Parameters:
            graphHandle: The pyqtplot widget used in the UI """
        super().__init__(graphHandle)

        self.openFiles = []
        self.loadLines = []
        self.stepLines = []
        self.loadStepLines = []

        # default to time series when setting up the graph axes
        self.setupTimeSeries()
        return
    

    def setupTimeSeries(self):

        super().setupTimeSeries()

        print("building time series graph")

        for i in self.loadLines:
            i.show()

        for i in self.stepLines:
            i.show()

        for i in self.loadStepLines:
            i.hide()

        return


    def setupLoadDisplacementGraph(self):
        
        super().setupLoadDisplacementGraph()
        
        print("building load displacement graph")

        for i in self.loadLines:
            i.hide()

        for i in self.stepLines:
            i.hide()

        for i in self.loadStepLines:
            i.show()

        return


    def addDataSet(self, data):
        """ Adds a set of data to the graph screen.
        Parameters:
            x (int): array of sample numbers to be graphed
            step (int): array of displacement data to be graphed
            load (fload): array of load data to be graphed """

        # check if the file has already been opened -> don't open it again
        exists = False
        for filename in self.openFiles:
            if filename == data.filename:
                exists = True

        # open the file if it is not already open
        if exists == False:
            self.openFiles.append(data.filename)
            self.loadLines.append(self.graph.plot(data.sample, data.load, pen=self.getPen()))
            self.stepLines.append(self.graph.plot(data.sample, data.step, pen=self.getPen()))
            self.loadStepLines.append(self.graph.plot(data.step, data.load, pen=self.getPen()))
            self.setupTimeSeries()
        return


    def clear(self):
        """ Clears the collected data and the graph area. """
        for i in self.loadLines:
            i.clear()

        for i in self.stepLines:
            i.clear()

        for i in self.loadStepLines:
            i.clear()  

        self.openFiles = []
        self.loadLines = []
        self.stepLines = []
        self.loadStepLines = []

        super().clear()
        return
