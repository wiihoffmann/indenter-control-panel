
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QThread
from multiprocessing import Event
import sys
import os

#custom class imports
from firmware.Indenter import *
from interface.WarningDialog import *

DEFAULT_MAX_LOAD = "60"
DEFAULT_MAX_LOAD_TIME = "2"
DEFAULT_PRELOAD = "5"
DEFAULT_PRELOAD_TIME = "1"
DEFAULT_STEP_RATE = "1500"

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

        # set up the signal handler for the "done" signal from the measurement loop
        self.sigHandler = DoneSigHandler()
        self.sigHandler.doneSig.connect(self.enableButtons)
        self.sigHandler.start()

        # the buttons to disable during a measurement
        self.toBlank = [self.clearButton, self.exitButton, self.loadButton, self.saveButton, self.moveUpButton, self.moveDownButton,
                    self.preloadIncButton, self.preloadDecButton, self.preloadTimeIncButton, self.preloadTimeDecButton,
                    self.maxLoadIncButton, self.maxLoadDecButton, self.maxLoadTimeIncButton, self.maxLoadTimeDecButton,
                    self.stepRateIncButton, self.stepRateDecButton]

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
        self.maxLoadIncButton.pressed.connect( lambda: self.updateReadout(5, 110, 5, self.maxLoadDisplay))
        self.maxLoadDecButton.pressed.connect( lambda: self.updateReadout(5, 110, -5, self.maxLoadDisplay))
        
        # set up the max load time buttons / readout
        self.maxLoadTimeDisplay.setText(DEFAULT_MAX_LOAD_TIME + " s")
        self.maxLoadTimeIncButton.pressed.connect( lambda: self.updateReadout(0, 15, 1, self.maxLoadTimeDisplay))
        self.maxLoadTimeDecButton.pressed.connect( lambda: self.updateReadout(0, 15, -1, self.maxLoadTimeDisplay))

        # set up the step rate buttons / readout
        self.stepRateDisplay.setText(DEFAULT_STEP_RATE)
        self.stepRateIncButton.pressed.connect( lambda: self.updateReadout(1000, 2500, 100, self.stepRateDisplay))
        self.stepRateDecButton.pressed.connect( lambda: self.updateReadout(1000, 2500, -100, self.stepRateDisplay))
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
            self, "Load measurement from file", os.path.join(self.dir, "Collected Data/"), "CSV Files (*.csv);;All Files (*)")
       
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

        # disable some buttons during the measurement
        for i in self.toBlank:
            i.setEnabled(False)
        
        # if the preload is larger than the max load, issue a warning
        if preload >= maxLoad:
            dlg = WarningDialog(self)
            dlg.exec()
        # else start the measurement
        else:
            self.indenter.takeStiffnessMeasurement(preload, preloadTime, maxLoad, maxLoadTime, stepRate, self.sigHandler.asyncDoneEvent)


    def enableButtons(self):
        """ Enables the buttons when the measurement completes. """

        for i in self.toBlank:
            i.setEnabled(True)
        return


    def exitProgram(self):
        """ Quits the program. """

        self.indenter.emergencyStop()
        sys.exit()
        return



class DoneSigHandler(QThread):
    """ This class allows us to synchronize signals from the measurement loop (asynchronous)
    with the QT GUI loop (synchronous). """

    doneSig = pyqtSignal()
    asyncDoneEvent = Event()

    def __init__(self):
        """ Initialize a new done signal handler"""
        super().__init__()
        self.asyncDoneEvent.clear()

    def run(self):
        """ The main loop of the signal handler. """
        while True:
            try:
                # wait for an asynchronous done signal, then send a synchronous done signal
                self.asyncDoneEvent.wait()
                self.doneSig.emit()
                self.asyncDoneEvent.clear()
            except Exception as e:
                print(e)
        return

