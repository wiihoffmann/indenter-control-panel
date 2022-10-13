
import pyqtgraph as pg
from dataTools.MeasurementData import *
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
        self.colorindex = 0

        self.loadLines = []
        self.stepLines = []
        self.loadStepLines = []
        self.VASLines = []
        self.VASStepLines = []
        
        return
    

    def getPen(self):
        color = pg.intColor(self.colorindex, hues=Config.GRAPH_COLORS, values=1, maxValue=255, minValue=150, maxHue=360, minHue=0, sat=255, alpha=255)
        self.colorindex += 1
        return pg.mkPen(color, width = Config.GRAPH_LINE_WIDTH)


    def setupTimeSeries(self):
        
        self.view = 0

        # set up the graph area
        self.graph.setBackground('w')
        self.graph.setLabel('left', 'Displacement (x100)', units ='steps')
        self.graph.setLabel('right', 'Force', units ='N')
        self.graph.setLabel('bottom', 'Sample number')
        
        if self.loadLines != [] and self.stepLines != [] and self.loadStepLines != []:
            for i in self.loadLines:
                i.show()

            for i in self.stepLines:
                i.show()

            for i in self.VASLines:
                i.show()

            for i in self.VASStepLines:
                i.hide()

            for i in self.loadStepLines:
                i.hide()

        return


    def setupLoadDisplacementGraph(self):
        
        self.view = 1

        # set up the graph area
        self.graph.setBackground('w')
        self.graph.setLabel('left', 'Force', units ='N')
        self.graph.setLabel('right', 'VAS score', units ='')
        self.graph.setLabel('bottom', 'Displacement (x100)', units ='steps')

        if self.loadLines != [] and self.stepLines != [] and self.loadStepLines != []:
            for i in self.loadLines:
                i.hide()

            for i in self.stepLines:
                i.hide()

            for i in self.VASLines:
                i.hide()

            for i in self.VASStepLines:
                i.show()

            for i in self.loadStepLines:
                i.show()

        return


    def cycleViews(self):
        # toggle to time series
        if self.view == 0:
            # update current view type
            self.setupLoadDisplacementGraph()

        # toggle to load as function of displacement
        elif self.view == 1:
            # update current view type
            self.setupTimeSeries()

        # make sure the data is in range
        self.graph.getPlotItem().enableAutoRange()
        return


    def clear(self):
        """ Clears the collected data and the graph area. """
        for i in self.loadLines:
            i.clear()

        for i in self.stepLines:
            i.clear()

        for i in self.loadStepLines:
            i.clear()  

        for i in self.VASLines:
            i.clear() 

        for i in self.VASStepLines:
            i.clear() 

        self.loadLines = []
        self.stepLines = []
        self.loadStepLines = []
        self.VASLines = []
        self.VASStepLines = []

        self.graph.getPlotItem().enableAutoRange()
        self.colorindex = 0
        return

