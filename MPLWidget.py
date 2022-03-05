from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import numpy
    
class MPLWidget(QWidget):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.stepPlot = self.canvas.axes.plot([],[])[0]
        self.loadPlot = self.canvas.axes.plot([],[])[0]
        self.setLayout(layout)


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