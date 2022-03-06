from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import numpy
    
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MPLGrapher(FigureCanvas, TimedAnimation):
    
    def __init__(self):
        self.loadData = []
        self.stepData = []

        # TODO: probably dont need this stuff... but I'm scared to remove it right now
        self.xlim = 300
        self.n = numpy.linspace(0, self.xlim - 1, self.xlim)
        self.y = (self.n * 0.0) + 50
        
        # Setup the graph area
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()

        # set up the line styles
        self.line1 = Line2D([], [], color='blue')
        self.line2 = Line2D([], [], color='orange')

        # add the lines to the graph
        self.ax1.add_line(self.line1)
        # TODO: get second line working properly
        self.ax1.add_line(self.line2)
        
        # set up the axis
        self.ax1.set_xlabel('sample number')
        self.ax1.set_ylabel('load')
        self.ax2.set_ylabel('steps')
        self.ax1.legend(('load', 'steps'), loc='upper right')
        self.ax1.set_title('load - displacement graph')
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(0, 100)

        # finish configuring the graph area
        self.fig.tight_layout()
        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        return


    def new_frame_seq(self):
        return iter(range(self.n.size))


    def _init_draw(self):
        lines = [self.line1, self.line2]
        for l in lines:
            l.set_data([], [])
        return


    def addData(self, step, load):
        self.stepData.append(step)
        self.loadData.append(load)
        return


    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.loadData) > 0):
            self.y = numpy.roll(self.y, -1)
            self.y[-1] = self.loadData[0]
            del(self.loadData[0])

        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line2.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])

        self._drawn_artists = [self.line1, self.line2]
        for l in self._drawn_artists:
            l.set_animated(True)
        return


    # def _step(self, *args):
    #     # Extends the _step() method for the TimedAnimation class.
    #     try:
    #         TimedAnimation._step(self, *args)
    #     except Exception as e:
    #         TimedAnimation._stop(self)
    #         pass
    #     return


    # TODO: fix me
    def clear(self):
        self.ax1.clear()
        self.ax1.legend(
            ('cosine', 'sine'), loc='upper right')
        self.ax1.set_title('Cosine - Sine Signal')
        self.stepPlot = self.ax1.plot([],[])[0]
        self.loadPlot = self.ax1.plot([],[])[0]
        #self.fig.draw()


    # TODO: fix me
    def plotData(self, x, step, load):
        self.ax1.clear()
        self.stepPlot = self.ax1.plot(x, step)[0]
        self.loadPlot = self.ax1.plot(x, load)[0]
        self.ax1.legend(('Step', 'Load'), loc='upper right')
        self.ax1.set_title('Results')
        self.ax1.set_ylabel("y axis")
        self.ax1.set_xlabel("x axis")

        self.fig.tight_layout()
        self.canvas.draw()


    # TODO: fix me
    def addDataPoint(self, x, step, load):
        self.loadPlot.set_xdata(numpy.append(self.loadPlot.get_xdata(), x))
        self.loadPlot.set_ydata(numpy.append(self.loadPlot.get_ydata(), load))
        self.canvas.figure.tight_layout()
        self.canvas.draw()
        self.canvas.flush_events()


    # You need to setup a signal slot mechanism, to
    # send data to your GUI in a thread-safe way.
    # Believe me, if you don't do this right, things
    # go very very wrong..
    class Communicate(QObject):
        data_signal = pyqtSignal(float, float)

 