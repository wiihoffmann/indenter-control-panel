
import pyqtgraph as pg



class Grapher():
    """ A class for plotting collected data into the graph are of the UI.
        This class allows for graphing data as its collected, graphing old data,
        and clearing the graph. """

    def __init__(self, graphHandle):
        """ Creates a new grapher object for visualizing collected data.
        Parameters:
            graphHandle: The pyqtplot widget used in the UI """

        self.graph = graphHandle

        # set up line colors
        self.redPen = pg.mkPen('r', width=3)
        self.bluePen = pg.mkPen('b', width=3)
        return
    

    def setupTimeSeries(self):
        
        self.view = 0

        # set up the graph area
        self.graph.setBackground('w')
        self.graph.setLabel('left', 'Displacement (x100)', units ='steps')
        self.graph.setLabel('right', 'Force', units ='N')
        self.graph.setLabel('bottom', 'Sample number')
        return


    def setupLoadDisplacementGraph(self):
        
        self.view = 1

        # set up the graph area
        self.graph.setBackground('w')
        self.graph.setLabel('left', 'Force', units ='N')
        self.graph.setLabel('right', '', units ='')
        self.graph.setLabel('bottom', 'Displacement (x100)', units ='steps')
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

        self.xData = []
        self.stepData = []
        self.loadData = []
        self.loadLine.clear()
        self.stepLine.clear()
        return

