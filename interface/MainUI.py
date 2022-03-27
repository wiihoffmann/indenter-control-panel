
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import sys
import os

#custom class imports
from firmware.Indenter import *
from interface.WarningDialog import *
import Config


class MainWindow(QMainWindow):
    """ The class responsible for managing the main interface window.
    This class also defines what happend when buttons are pressed. """

    def __init__(self, dir):
        """ Create a new instance of the main window of the indenter controller.
        Parameters:
            dir (str): the directory the program was launched from """

        # the directory we launched from
        self.dir = dir

        # initialize Qt for the GUI
        QMainWindow.__init__(self)
        loadUi(os.path.join(self.dir, "interface/mainWindow.ui"), self)
        self.setWindowTitle("Indenter Control Panel")
        self.showFullScreen()

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
        self.preloadDisplay.setText(str(Config.DEFAULT_PRELOAD) + " N")
        self.preloadIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_PRELOAD, Config.MAX_PRELOAD, Config.PRELOAD_INCREMENT_SIZE, self.preloadDisplay))
        self.preloadDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_PRELOAD, Config.MAX_PRELOAD, -1 * Config.PRELOAD_INCREMENT_SIZE, self.preloadDisplay))
        
        # set up the preload time buttons / readout
        self.preloadTimeDisplay.setText(str(Config.DEFAULT_PRELOAD_TIME) + " s")
        self.preloadTimeIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_HOLD_TIME, Config.MAX_HOLD_TIME, Config.HOLD_TIME_INCREMENT_SIZE, self.preloadTimeDisplay))
        self.preloadTimeDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_HOLD_TIME, Config.MAX_HOLD_TIME, -1 * Config.HOLD_TIME_INCREMENT_SIZE, self.preloadTimeDisplay))

        # set up the max load buttons / readout
        self.maxLoadDisplay.setText(str(Config.DEFAULT_MAX_LOAD) + " N")
        self.maxLoadIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_LOAD, Config.MAX_LOAD, Config.MAX_LOAD_INCREMENT_SIZE, self.maxLoadDisplay))
        self.maxLoadDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_LOAD, Config.MAX_LOAD, -1 * Config.MAX_LOAD_INCREMENT_SIZE, self.maxLoadDisplay))
        
        # set up the max load time buttons / readout
        self.maxLoadTimeDisplay.setText(str(Config.DEFAULT_MAX_LOAD_TIME) + " s")
        self.maxLoadTimeIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_HOLD_TIME, Config.MAX_HOLD_TIME, Config.HOLD_TIME_INCREMENT_SIZE, self.maxLoadTimeDisplay))
        self.maxLoadTimeDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_HOLD_TIME, Config.MAX_HOLD_TIME, -1 * Config.HOLD_TIME_INCREMENT_SIZE, self.maxLoadTimeDisplay))

        # set up the step rate buttons / readout
        self.stepRateDisplay.setText(str(Config.DEFAULT_STEP_RATE))
        self.stepRateIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_STEP_RATE, Config.MAX_STEP_RATE, Config.STEP_RATE_INCREMENT_SIZE, self.stepRateDisplay))
        self.stepRateDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_STEP_RATE, Config.MAX_STEP_RATE, -1 * Config.STEP_RATE_INCREMENT_SIZE, self.stepRateDisplay))
        return


    def updateReadout(self, min, max, step, readout):
        """ Updates a parameter readout in the user interface when a button is pressed. 
        Parameters:
            min (int): the minimum value the readout can take
            max (int): the maximum value the readout can take
            step (int): the value to increment/decrement the readout by
            readout (QLineEdit): the readout to update"""

        # increment the readout by the step value
        if readout.text()[-1:].isalpha():   # if we have units
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
        return


    def saveFile(self):
        """ Start a dialog to save the current graph data into a CSV file. """

        # start the dialog for picking a directory and file name
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save measurement to file", os.path.join(self.dir, "Collected Data/"), "CSV File (*.csv)", options=options)
        
        # save data if the file name is valid
        if filename:
            self.indenter.saveResults(filename)
        return


    def loadFile(self):
        """ Start a dialog to load data from a CSV file. """

        # start the dialog for picking a directory and file name
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load measurement from file", "", "CSV Files (*.csv);;All Files (*)")
        
        # load data if the file name is valid
        if filename:
            self.indenter.loadAndShowResults(filename)
        #self.indenter.loadAndShowResults("/home/pi/spinal-stiffness-indenter/sample data/2021-12-5-15-19-34.csv")
        return


    def startMeasurement(self):
        """ Initiates a stiffness measurement. """

        # get the measurement parameters from the readouts
        preload = int(self.preloadDisplay.text()[:-2])
        maxLoad = int(self.maxLoadDisplay.text()[:-2])
        preloadTime = int(self.preloadTimeDisplay.text()[:-2])
        maxLoadTime = int(self.maxLoadTimeDisplay.text()[:-2])
        stepRate = int(self.stepRateDisplay.text())

        # if the preload is larger than the max load, issue a warning
        if preload >= maxLoad:
            dlg = WarningDialog(self)
            dlg.exec()
        # else start the measurement
        else:
            self.indenter.takeStiffnessMeasurement(preload, preloadTime, maxLoad, maxLoadTime, stepRate)
        return


    def exitProgram(self):
        """ Quits the program. """

        self.indenter.emergencyStop()
        sys.exit()
        return

