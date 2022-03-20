
# UI imports
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *

# data management imports
import sys

#custom class imports
from firmware.Indenter import *

DEFAULT_MAX_LOAD = "60"
DEFAULT_MAX_LOAD_TIME = "2"
DEFAULT_PRELOAD = "5"
DEFAULT_PRELOAD_TIME = "1"
DEFAULT_STEP_RATE = "1500"

class MainWindow(QMainWindow):

    def __init__(self, UIFileName):
        # initialize Qt for the GUI
        QMainWindow.__init__(self)
        loadUi(UIFileName, self)
        self.setWindowTitle("Indenter Control Panel")

        # initialize the firmware/back end functionality
        self.indenter = Indenter(self.plotWidget)

        # set up bindings for the buttons
        self.clearButton.clicked.connect(self.indenter.clearResults)    # clear button
        self.loadButton.clicked.connect(self.loadFile)                  # load button
        self.saveButton.clicked.connect(self.saveFile)                  # save button
        self.exitButton.clicked.connect(self.exitProgram)               # exit button
        
        self.startButton.clicked.connect(self.startMeasurement)         # start button
        self.stopButton.clicked.connect(self.indenter.emergencyStop)    # stop button

        self.moveUpButton.pressed.connect(self.indenter.startJogUp)     # jog up button pressed
        self.moveUpButton.released.connect(self.indenter.stopJogging)   # jog up button released

        self.moveDownButton.pressed.connect(self.indenter.startJogDown) # jog down button pressed
        self.moveDownButton.released.connect(self.indenter.stopJogging) # jog down button released
        
        # set up the preload buttons / readout
        self.preloadDisplay.setText(DEFAULT_PRELOAD + " N")
        self.preloadIncButton.pressed.connect( lambda: self.updateReadout(5, 30, 1, self.preloadDisplay))
        self.preloadDecButton.pressed.connect( lambda: self.updateReadout(5, 30, -1, self.preloadDisplay))
        
        # set up the preload time buttons / readout
        self.preloadTimeDisplay.setText(DEFAULT_PRELOAD_TIME + " s")
        self.preloadTimeIncButton.pressed.connect( lambda: self.updateReadout(0, 15, 1, self.preloadTimeDisplay))
        self.preloadTimeDecButton.pressed.connect( lambda: self.updateReadout(0, 15, -1, self.preloadTimeDisplay))

        # set up the max load buttons / readout
        self.maxLoadDisplay.setText(DEFAULT_MAX_LOAD + " N")
        self.maxLoadIncButton.pressed.connect( lambda: self.updateReadout(5, 100, 5, self.maxLoadDisplay))
        self.maxLoadDecButton.pressed.connect( lambda: self.updateReadout(5, 100, -5, self.maxLoadDisplay))
        
        # set up the max load time buttons / readout
        self.maxLoadTimeDisplay.setText(DEFAULT_MAX_LOAD_TIME + " s")
        self.maxLoadTimeIncButton.pressed.connect( lambda: self.updateReadout(0, 15, 1, self.maxLoadTimeDisplay))
        self.maxLoadTimeDecButton.pressed.connect( lambda: self.updateReadout(0, 15, -1, self.maxLoadTimeDisplay))

        # set up the step rate buttons / readout
        self.stepRateDisplay.setText(DEFAULT_STEP_RATE)
        self.stepRateIncButton.pressed.connect( lambda: self.updateReadout(1000, 2500, 100, self.stepRateDisplay))
        self.stepRateDecButton.pressed.connect( lambda: self.updateReadout(1000, 2500, -100, self.stepRateDisplay))


    def updateReadout(self, min, max, step, readout):     
        # increment the readout by the step value
        if readout.text()[:-1].isalpha(): # if we have units
            newValue = int(readout.text()[:-2]) + step
            units = readout.text()[-2:]
        else: # if there are no units
            newValue = int(readout.text()) + step
            units = ""

        # wrap between the min and the max
        if newValue > max:
            newValue = min
        elif newValue < min:
            newValue = max
        
        # set the readout to the new value
        readout.setText(str(newValue) + units)


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


    def startMeasurement(self):
        # TODO: make sure that the preload is less than the full load!
        maxLoad = int(self.maxLoadDisplay.text()[:-2])
        self.indenter.takeStiffnessMeasurement(maxLoad)


    def exitProgram(self):
        self.indenter.emergencyStop()
        sys.exit()
