
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
import os

import Config
from interface.dialogs.DirectionPanel import *
from interface.dialogs.WarningDialog import *
from interface.SignalConnector import *


class BasicTestSetupWidget(QWidget):


    def __init__(self, indenter, backButtonCallback):
        self.indenter = indenter
        
        super().__init__()
        loadUi(os.path.join(os.getcwd(), "interface/widgets/basicTestControls.ui"), self)

        # the buttons to disable during a measurement
        self.toBlank = [self.backButton, self.positionButton, self.stepRateIncButton, self.stepRateDecButton, 
                    self.preloadIncButton, self.preloadDecButton, self.preloadTimeIncButton, self.preloadTimeDecButton,
                    self.maxLoadIncButton, self.maxLoadDecButton, self.maxLoadTimeIncButton, self.maxLoadTimeDecButton]

        # set up interface buttons
        self.backButton.clicked.connect(backButtonCallback)             # back button
        self.startButton.clicked.connect(self.startMeasurement)         # start button
        self.stopButton.clicked.connect(self.indenter.emergencyStop)    # stop button
        self.positionButton.clicked.connect(self.__openPositionWindow)  # positioning button

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

        # set up the signal handler for the "done" signal from the measurement loop
        self.sigHandler = SignalConnector()
        
        print("init basic test setup complete")
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
        preload = int(self.preloadDisplay.text()[:-2])
        maxLoad = int(self.maxLoadDisplay.text()[:-2])
        preloadTime = int(self.preloadTimeDisplay.text()[:-2])
        maxLoadTime = int(self.maxLoadTimeDisplay.text()[:-2])
        stepRate = int(self.stepRateDisplay.text())
        
        # if the preload is larger than the max load, issue a warning
        if preload >= maxLoad:
            dlg = WarningDialog(self)
            dlg.exec()
            dlg.raise_()

        # else start the measurement
        else:
            # set up the signal handler for the done signal
            self.sigHandler.connect(self.enableButtons)
            self.sigHandler.start()

            # disable some buttons during the measurement
            for i in self.toBlank:
                i.setEnabled(False)

            self.indenter.takeStiffnessMeasurement(preload, preloadTime, maxLoad, maxLoadTime, stepRate, self.sigHandler.getAsyncSignal())


    def enableButtons(self):
        """ Enables the buttons when the measurement completes. """

        for i in self.toBlank:
            i.setEnabled(True)
        return

