
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from threading import Timer
from datetime import datetime
import subprocess
import sys
import os

#custom class imports
from firmware.Indenter import *
from interface.dialogs.DirectionPanel import *
from interface.widgets.basicTestSetup import *
import Config


class MainUI(QMainWindow):
    """ The class responsible for managing the main interface window.
    This class also defines what happend when buttons are pressed. """

    def __init__(self, dir, compareCallback):
        """ Create a new instance of the main window of the indenter controller.
        Parameters:
            dir (str): the directory the program was launched from """

        # the directory we launched from
        self.dir = dir

        # initialize Qt for the GUI
        QMainWindow.__init__(self)
        loadUi(os.path.join(self.dir, "interface/mainWindows/mainWindow.ui"), self)
        self.setWindowTitle("Indenter Control Panel")
        self.showFullScreen()

        # initialize the firmware/back end functionality
        self.indenter = Indenter(self.plotWidget)

        # build the control widgets
        self.basicTestSetupWidget = BasicTestSetupWidget(self)
        
        # add widgets to the stack and show the main widget
        self.buttonStack.addWidget(self.basicTestSetupWidget)

        # set up bindings for the buttons
        self.clearButton.clicked.connect(self.indenter.clearResults)    # clear button
        self.viewButton.clicked.connect(self.indenter.changeView)       # view button
        self.loadButton.clicked.connect(self.loadFile)                  # load button
        self.saveButton.clicked.connect(self.saveFile)                  # save button
        self.compareButton.clicked.connect(compareCallback)             # compare button
        self.exitButton.clicked.connect(self.exitProgram)               # exit button
        self.positionButton.clicked.connect(self.__openPositionWindow)  # positioning button
        self.setupButton.clicked.connect(self.goToSetup)

        # # the buttons to disable during a measurement
        # self.toBlank = [self.clearButton, self.exitButton, self.loadButton, self.saveButton, self.positionButton,
        #             self.preloadIncButton, self.preloadDecButton, self.preloadTimeIncButton, self.preloadTimeDecButton,
        #             self.maxLoadIncButton, self.maxLoadDecButton, self.maxLoadTimeIncButton, self.maxLoadTimeDecButton,
        #             self.stepRateIncButton, self.stepRateDecButton, self.viewButton, self.compareButton]

        
        # self.startButton.clicked.connect(self.startMeasurement)         # start button
        # self.stopButton.clicked.connect(self.indenter.emergencyStop)    # stop button

        # # set up the preload buttons / readout
        # self.preloadDisplay.setText(str(Config.DEFAULT_PRELOAD) + " N")
        # self.preloadIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_PRELOAD, Config.MAX_PRELOAD, Config.PRELOAD_INCREMENT_SIZE, self.preloadDisplay))
        # self.preloadDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_PRELOAD, Config.MAX_PRELOAD, -1 * Config.PRELOAD_INCREMENT_SIZE, self.preloadDisplay))
        
        # # set up the preload time buttons / readout
        # self.preloadTimeDisplay.setText(str(Config.DEFAULT_PRELOAD_TIME) + " s")
        # self.preloadTimeIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_HOLD_TIME, Config.MAX_HOLD_TIME, Config.HOLD_TIME_INCREMENT_SIZE, self.preloadTimeDisplay))
        # self.preloadTimeDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_HOLD_TIME, Config.MAX_HOLD_TIME, -1 * Config.HOLD_TIME_INCREMENT_SIZE, self.preloadTimeDisplay))

        # # set up the max load buttons / readout
        # self.maxLoadDisplay.setText(str(Config.DEFAULT_MAX_LOAD) + " N")
        # self.maxLoadIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_LOAD, Config.MAX_LOAD, Config.MAX_LOAD_INCREMENT_SIZE, self.maxLoadDisplay))
        # self.maxLoadDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_LOAD, Config.MAX_LOAD, -1 * Config.MAX_LOAD_INCREMENT_SIZE, self.maxLoadDisplay))
        
        # # set up the max load time buttons / readout
        # self.maxLoadTimeDisplay.setText(str(Config.DEFAULT_MAX_LOAD_TIME) + " s")
        # self.maxLoadTimeIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_HOLD_TIME, Config.MAX_HOLD_TIME, Config.HOLD_TIME_INCREMENT_SIZE, self.maxLoadTimeDisplay))
        # self.maxLoadTimeDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_HOLD_TIME, Config.MAX_HOLD_TIME, -1 * Config.HOLD_TIME_INCREMENT_SIZE, self.maxLoadTimeDisplay))

        # # set up the step rate buttons / readout
        # self.stepRateDisplay.setText(str(Config.DEFAULT_STEP_RATE))
        # self.stepRateIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_STEP_RATE, Config.MAX_STEP_RATE, Config.STEP_RATE_INCREMENT_SIZE, self.stepRateDisplay))
        # self.stepRateDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_STEP_RATE, Config.MAX_STEP_RATE, -1 * Config.STEP_RATE_INCREMENT_SIZE, self.stepRateDisplay))


        # set up the signal handler for the "done" signal from the measurement loop
        # self.sigHandler = SignalConnector()
        # self.sigHandler.connect(self.enableButtons)
        # self.sigHandler.start()
        return


    def __openPositionWindow(self):
        window = DirectionPanel(self, self.dir)
        window.exec_()
        return


    def goToSetup(self):
        if self.regularTestRadioButton.isChecked():
            print("regular")
            self.buttonStack.setCurrentIndex(self.buttonStack.indexOf(self.basicTestSetupWidget))
        elif self.regularRepeatedTestRadioButton.isChecked():
            print("repeated regular")   
        return


    def launchKeyboard(self):
        self.showMaximized()
        subprocess.run(["xvkbd", "-no-keypad", "-window", "Save measurement to file"])
        self.showFullScreen()
        return


    def getDirectory(self):
        """Returns a string to the directory in which files should be stored.
        Attempts to store to a USB stick before storing locally."""

        # check if a USB stick is inserted and set default path to it
        dirs = os.listdir("/media/pi")
        if len(dirs) != 0:
            directory = os.path.join("/media/pi", dirs[0]) + "/"
        # else save locally
        else:
            directory = os.path.join(self.dir, "Collected Data/")
        return directory


    def saveFile(self):
        """ Start a dialog to save the current graph data into a CSV file. """
        
        # open the on screen keyboard once the next window has had a chance to open
        if Config.SHOW_KEYBOARD:
            Timer(.25, self.launchKeyboard).start()
        
        # set default file name to the current date/time
        now = datetime.now()
        # dd-mm-YY H-M-S
        dt_string = now.strftime("%Y-%m-%d %H-%M-%S")

        # start the dialog for picking a directory and file name
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save measurement to file", self.getDirectory() + dt_string + ".csv", "CSV File (*.csv)", options=options)
        
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
            self, "Load measurement from file", self.getDirectory(), "CSV Files (*.csv);;All Files (*)", options=options)
       
        # load data if the file name is valid
        if filename:
            self.indenter.loadAndShowResults(filename)
        return


    # def startMeasurement(self):
    #     """ Initiates a stiffness measurement. """

    #     # get the measurement parameters from the readouts
    #     preload = int(self.preloadDisplay.text()[:-2])
    #     maxLoad = int(self.maxLoadDisplay.text()[:-2])
    #     preloadTime = int(self.preloadTimeDisplay.text()[:-2])
    #     maxLoadTime = int(self.maxLoadTimeDisplay.text()[:-2])
    #     stepRate = int(self.stepRateDisplay.text())
        
    #     # if the preload is larger than the max load, issue a warning
    #     if preload >= maxLoad:
    #         dlg = WarningDialog(self)
    #         dlg.exec()
    #         dlg.raise_()

    #     # else start the measurement
    #     else:
    #         # disable some buttons during the measurement
    #         for i in self.toBlank:
    #             i.setEnabled(False)

    #         self.indenter.takeStiffnessMeasurement(preload, preloadTime, maxLoad, maxLoadTime, stepRate, self.sigHandler.getAsyncSignal())


    # def enableButtons(self):
    #     """ Enables the buttons when the measurement completes. """

    #     for i in self.toBlank:
    #         i.setEnabled(True)
    #     return


    def exitProgram(self):
        """ Quits the program. """

        self.indenter.emergencyStop()
        sys.exit()
        return

