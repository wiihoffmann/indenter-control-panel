
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

        self.xData = []
        self.stepData = []
        self.loadData = []

        # default to time series when setting up the graph axes
        self.setupTimeSeries()
        return
    

    def setupTimeSeries(self):

        super().setupTimeSeries()

        return


    def setupLoadDisplacementGraph(self):
        
        super().setupLoadDisplacementGraph()

        return


    def addDataSet(self, x, step = [], load = []):
        """ Adds a set of data to the graph screen.
        Parameters:
            x (int): array of sample numbers to be graphed
            step (int): array of displacement data to be graphed
            load (fload): array of load data to be graphed """


        return


    # def clear(self):
    #     """ Clears the collected data and the graph area. """
    #     super().clear()


    #     return
