
# UI imports
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *

# data management imports
import sys

#custom  class imports
from Indenter import *

class MainWindow(QMainWindow):

    def __init__(self, UIFileName):
        # initialize Qt for the GUI
        QMainWindow.__init__(self)
        loadUi(UIFileName, self)
        self.setWindowTitle("Indenter Control Panel")

        # initialize the firmware/back end functionality
        self.indenter = Indenter(self.plotWidget)

        # set up bindings for the buttons
        self.pushButton_clear_graph.clicked.connect(self.indenter.clearResults)  # clear button
        self.LoadButton.clicked.connect(self.loadFile)                           # load button
        self.SaveButton.clicked.connect(self.saveFile)                           # save button
        self.exitButton.clicked.connect(self.exitProgram)                        # exit button
        
        self.startButton.clicked.connect(self.startMeasurement)                  # start button
        self.stopButton.clicked.connect(self.indenter.emergencyStop)             # stop button

        self.upButton.pressed.connect(self.indenter.startJogUp)                  # jog up button pressed
        self.upButton.released.connect(self.indenter.stopJogging)                # jog up button released

        self.downButton.pressed.connect(self.indenter.startJogDown)              # jog down button pressed
        self.downButton.released.connect(self.indenter.stopJogging)              # jog down button released
        
        # set up the force application buttons / readout
        self.incrementButton.setAutoRepeat(True)
        self.decrementButton.setAutoRepeat(True)
        self.forceText.insertPlainText("20")
        self.incrementButton.pressed.connect(
            lambda: self.update_force('increment'))
        self.decrementButton.pressed.connect(
            lambda: self.update_force('decrement'))
        

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(
            self, "QFileDialog.getSaveFileName()", "", "CSV File (*.csv)", options=options)
        if filename:
            self.indenter.saveResults(filename)


    def loadFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if filename:
            self.indenter.loadAndShowResults(filename)


    def update_force(self, _str):
        # get current force and increment/decrement base on button pressed
        init_force = int(self.forceText.toPlainText())
        new_force = (init_force+5) if _str == 'increment' else (init_force-5)
        
        # wrap force values over 100 back to 0
        if(0 <= new_force <= 100):
            self.forceText.setText(str(new_force))
        else:
            self.forceText.setText('0')


    def startMeasurement(self):
        loadGrams = int(self.forceText.toPlainText())/9.81*1000 # convert force to mass
        self.indenter.takeStiffnessMeasurement(loadGrams)


    def exitProgram(self):
        print("stopped")
        self.indenter.shutdown()
        sys.exit()
