
import math
from graphTools.Grapher import *


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

        # default to time series when setting up the graph axes
        self.setupTimeSeries()
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
            pointSkip = math.ceil(len(data.sample) / Config.GRAPH_MAX_POINTS)
            if pointSkip == 0:
                pointSkip = 1

            self.openFiles.append(data.filename)
            self.loadLines.append(self.graph.plot(data.sample[::pointSkip], data.load[::pointSkip], pen=self.getPen()))
            self.loadStepLines.append(self.graph.plot(data.step[::pointSkip], data.load[::pointSkip], pen=self.getPen()))
            self.stepLines.append(self.graph.plot(data.sample[::pointSkip], data.step[::pointSkip], pen=self.getPen()))
            # if len(self.data.sample) == len(self.data.VASScores):
            #     self.VASLines.setData(self.data.sample[::pointSkip], self.data[0].VASScores[::pointSkip])
            #     self.VASStepLines.setData(self.data.step[::pointSkip], self.data[0].VASScores[::pointSkip])
            self.setupTimeSeries()
        return


    def clear(self):
        """ Clears the collected data and the graph area. """
        self.openFiles = []
        self.setupTimeSeries()
        super().clear()
        return
