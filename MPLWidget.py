from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import numpy
    

import matplotlib
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvas
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class CustomFigCanvas(FigureCanvas, TimedAnimation):
    
    def __init__(self):
        self.addedData = []
        print(matplotlib.__version__)
        # The data
        self.xlim = 300
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        a = []
        b = []
        a.append(2.0)
        a.append(4.0)
        a.append(2.0)
        b.append(4.0)
        b.append(3.0)
        b.append(4.0)
        self.y = (self.n * 0.0) + 50
        # The window
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)
        # self.ax1 settings
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('raw data')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='red', linewidth=2)
        self.line1_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(0, 100)
        self.fig.tight_layout()
        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        return

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        lines = [self.line1, self.line1_tail, self.line1_head]
        for l in lines:
            l.set_data([], [])
        return

    def addData(self, value):
        self.addedData.append(value)
        return

    def zoomIn(self, value):
        bottom = self.ax1.get_ylim()[0]
        top = self.ax1.get_ylim()[1]
        bottom += value
        top -= value
        self.ax1.set_ylim(bottom,top)
        self.draw()
        return

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)
            pass
        return

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedData) > 0):
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedData[0]
            del(self.addedData[0])

        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]
        for l in self._drawn_artists:
            l.set_animated(True)
        return


    def clear(self):
        self.canvas.axes.clear()
        self.canvas.axes.legend(
            ('cosine', 'sine'), loc='upper right')
        self.canvas.axes.set_title('Cosine - Sine Signal')
        self.stepPlot = self.canvas.axes.plot([],[])[0]
        self.loadPlot = self.canvas.axes.plot([],[])[0]
        self.canvas.draw()


    def plotData(self, x, step, load):
        self.canvas.axes.clear()
        self.stepPlot = self.canvas.axes.plot(x, step)[0]
        self.loadPlot = self.canvas.axes.plot(x, load)[0]
        self.canvas.axes.legend(('Step', 'Load'), loc='upper right')
        self.canvas.axes.set_title('Results')
        self.canvas.axes.set_ylabel("y axis")
        self.canvas.axes.set_xlabel("x axis")

        self.canvas.figure.tight_layout()
        self.canvas.draw()

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
        data_signal = pyqtSignal(float)

    ''' End Class '''