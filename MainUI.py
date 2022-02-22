from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
import sys
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random


from Controller import *


class MainWindow(QMainWindow):

    def __init__(self, UIFileName):
        # initialize Qt for the GUI
        QMainWindow.__init__(self)
        loadUi(UIFileName, self)
        self.setWindowTitle("Indenter Control Panel")
        # set up bindings for the buttons and widgets
        self.pushButton_generate_random_signal.clicked.connect(
            self.updateGraph)
        self.pushButton_clear_graph.clicked.connect(self.clearGraph)
        self.LoadButton.clicked.connect(self.loadFile)
        self.SaveButton.clicked.connect(self.saveFile)
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        self.forceText.insertPlainText("10")

        self.incrementButton.setAutoRepeat(True)
        self.decrementButton.setAutoRepeat(True)

        self.incrementButton.pressed.connect(
            lambda: self.update_force('increment'))
        self.decrementButton.pressed.connect(
            lambda: self.update_force('decrement'))

        self.exitButton.clicked.connect(self.exitProgram)

        self.startButton.clicked.connect(self.startProgram)
        self.stopButton.clicked.connect(self.stopProgram)

        self.upButton.pressed.connect(self.startMovingUp)
        self.upButton.released.connect(self.stopMovingUp)

        self.downButton.pressed.connect(self.startMovingDown)
        self.downButton.released.connect(self.stopMovingDown)

        # set up the motor and ADC controller
        self.controller = Controller(12, 16)

    def updateGraph(self):
        f = random.randint(1, 50)
        length_of_signal = 10000
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(
            ('cosine', 'sine'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosine - Sine Signal')
        self.MplWidget.canvas.figure.tight_layout()
        self.MplWidget.canvas.draw()

    def clearGraph(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.legend(
            ('cosine', 'sine'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosine - Sine Signal')
        self.MplWidget.canvas.draw()

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "CSV File (*.csv)", options=options)
        if fileName:
            print(fileName)

    def loadFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            print(fileName)

    def update_force(self, _str):
        init_force = int(self.forceText.toPlainText())
        new_force = (init_force+5) if _str == 'increment' else (init_force-5)

        if(0 <= new_force <= 100):
            self.forceText.setText(str(new_force))
        else:
            self.forceText.setText('0')

    def startMovingUp(self):
        self.controller.startMovingUp(1000)

    def stopMovingUp(self):
        self.controller.stopMovingUp()

    def startMovingDown(self):
        self.controller.startMovingDown(1000)

    def stopMovingDown(self):
        self.controller.stopMovingDown()

    def startProgram(self):
        print("started")

    def stopProgram(self):
        print("stopped")

    def exitProgram(self):
        print("stopped")
        sys.exit()
