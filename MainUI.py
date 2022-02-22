from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random


from Controller import *

class MainWindow(QMainWindow):
    
    def __init__(self, UIFileName):
        # initialize Qt for the GUI
        QMainWindow.__init__(self)
        loadUi(UIFileName,self)
        self.setWindowTitle("Indenter Control Panel")
        # set up bindings for the buttons and widgets
        self.pushButton_generate_random_signal.clicked.connect(self.updateGraph)
        self.pushButton_clear_graph.clicked.connect(self.clearGraph)
        self.LoadButton.clicked.connect(self.loadFile)
        self.SaveButton.clicked.connect(self.saveFile)
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        self.spinBox.valueChanged.connect(self.show_result)
        self.setButton.clicked.connect(self.display_force)
        
        self.upButton.pressed.connect(self.startMovingUp)
        self.upButton.released.connect(self.stopMovingUp)
        
        self.downButton.pressed.connect(self.startMovingDown)
        self.downButton.released.connect(self.stopMovingDown)

        # set up the motor and ADC controller
        self.controller = Controller(12,16)


    def updateGraph(self):
        f = random.randint(1, 50)
        length_of_signal = 10000
        t = np.linspace(0,1,length_of_signal)
        
        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosine', 'sine'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosine - Sine Signal')
        self.MplWidget.canvas.figure.tight_layout()
        self.MplWidget.canvas.draw()
        

    def clearGraph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.legend(('cosine', 'sine'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosine - Sine Signal')
        self.MplWidget.canvas.draw()
        self.forceTextEdit.setText('Cleared graph')


    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","CSV File (*.csv)", options=options)
        if fileName:
            print(fileName)


    def loadFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            print(fileName)

    def show_result(self):
        value = self.spinBox.value()
        
    def display_force(self):
        self.forceTextEdit.setText('Applying force of: ' + str(self.spinBox.value()) + ' N')
    
    def startMovingUp(self):
        self.controller.startMovingUp(1000)

    def stopMovingUp(self):
        self.controller.stopMovingUp() 

    def startMovingDown(self):
        self.controller.startMovingDown(1000)

    def stopMovingDown(self):
        self.controller.stopMovingDown()
