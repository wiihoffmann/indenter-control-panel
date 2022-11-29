
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
import os

import Config
from dataTools.MeasurementParams import *
from interface.dialogs.DirectionPanel import *
from interface.dialogs.WarningDialog import *
from interface.dialogs.ErrorDialog import *
from interface.dialogs.FileDialog import*
from interface.SignalConnector import *


class TemporalSummationTestSetupWidget(QWidget):


    def __init__(self, indenter, backButtonCallback):
        self.indenter = indenter

        super().__init__()
        loadUi(os.path.join(os.getcwd(), "interface/widgets/temporalSummationTestControls.ui"), self)

        # the buttons to disable during a measurement
        self.toBlank = [self.backButton, self.startButton, self.positionButton, self.stepRateIncButton, self.stepRateDecButton, 
                    self.maxLoadIncButton, self.maxLoadDecButton, self.repeatCountIncButton, self.repeatCountDecButton]

        # set up interface buttons
        self.backButton.clicked.connect(backButtonCallback)             # back button
        self.startButton.clicked.connect(self.startMeasurement)         # start button
        self.stopButton.clicked.connect(self.indenter.emergencyStop)    # stop button
        self.positionButton.clicked.connect(self.__openPositionWindow)  # positioning button

        # set up the max load buttons / readout
        self.maxLoadDisplay.setText(str(Config.TEMP_SUMM_DEFAULT_MAX_LOAD) + " N")
        self.maxLoadIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_LOAD, Config.MAX_LOAD, Config.MAX_LOAD_INCREMENT_SIZE, self.maxLoadDisplay))
        self.maxLoadDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_LOAD, Config.MAX_LOAD, -1 * Config.MAX_LOAD_INCREMENT_SIZE, self.maxLoadDisplay))

        # set up the step rate buttons / readout
        self.stepRateDisplay.setText(str(Config.TEMP_SUMM_DEFAULT_STEP_RATE))
        self.stepRateIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_STEP_RATE, Config.MAX_STEP_RATE, Config.STEP_RATE_INCREMENT_SIZE, self.stepRateDisplay))
        self.stepRateDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_STEP_RATE, Config.MAX_STEP_RATE, -1 * Config.STEP_RATE_INCREMENT_SIZE, self.stepRateDisplay))

        # set up repeat count buttons
        self.repeatCountDisplay.setText(str(Config.TEMP_SUMM_DEFAULT_REPEAT_COUNT))
        self.repeatCountIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_REPEAT_COUNT, Config.MAX_REPEAT_COUNT, Config.REPEAT_COUNT_INCREMENT_SIZE, self.repeatCountDisplay))
        self.repeatCountDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_REPEAT_COUNT, Config.MAX_REPEAT_COUNT, -1 * Config.REPEAT_COUNT_INCREMENT_SIZE, self.repeatCountDisplay))
 

        # set up the signal handler for the "done" signal from the measurement loop
        self.sigHandler = SignalConnector()
        # set up file dialog for save prompt
        self.fileDialog = FileDialog(self)
        return


    def __openPositionWindow(self):
        window = DirectionPanel()
        window.exec_()
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


    def startMeasurement(self):
        """ Initiates a stiffness measurement. """

        # get the measurement parameters from the readouts
        preload = 0
        maxLoad = int(self.maxLoadDisplay.text()[:-2])
        preloadTime = 0
        maxLoadTime = 0
        stepRate = int(self.stepRateDisplay.text())
        repeatCount = int(self.repeatCountDisplay.text())

        # if the preload is larger than the max load, issue a warning
        if preload >= maxLoad:
            dlg = WarningDialog(self)
            dlg.exec()
            dlg.raise_()

        # else start the measurement
        else:
            # set up the signal handler for the done signal
            self.sigHandler.connect(self.postTest)
            self.sigHandler.start()

            # disable some buttons during the measurement
            for i in self.toBlank:
                i.setEnabled(False)

            self.indenter.takeStiffnessMeasurement(preload, preloadTime, maxLoad, maxLoadTime, stepRate, self.sigHandler.getAsyncSignal(), repeatCount, TEMPORAL_SUMMATION_TEST_CODE)


    def postTest(self):
        """ Enables the buttons when the measurement completes. Prompts to save file."""
        self.sigHandler.disconnect()

        for i in self.toBlank:
            i.setEnabled(True)

        if(not self.indenter.wasMeasurementEStopped() and self.indenter.wasMeasurementSuccessful()):
            self.fileDialog.showSavePromptDialog(self.indenter)
        if(not self.indenter.wasMeasurementEStopped() and not self.indenter.wasMeasurementSuccessful()):
            dlg = ErrorDialog(self)
            dlg.exec()
            dlg.raise_()

        return

