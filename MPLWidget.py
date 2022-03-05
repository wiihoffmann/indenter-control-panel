from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
    
class MPLWidget(QWidget):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(layout)


    def clear(self):
        self.canvas.axes.clear()
        self.canvas.axes.legend(
            ('cosine', 'sine'), loc='upper right')
        self.canvas.axes.set_title('Cosine - Sine Signal')
        self.canvas.draw()


    def plotData(self, x, step, load):
        self.canvas.axes.clear()
        self.canvas.axes.plot(x, step)
        self.canvas.axes.plot(x, load)
        self.canvas.axes.legend(('Step', 'Load'), loc='upper right')
        self.canvas.axes.set_title('Results')
        self.canvas.axes.set_ylabel("y axis")
        self.canvas.axes.set_xlabel("x axis")

        self.canvas.figure.tight_layout()
        self.canvas.draw()