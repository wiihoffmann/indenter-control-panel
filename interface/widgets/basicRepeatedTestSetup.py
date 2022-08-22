
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
import os

import Config
from interface.dialogs.DirectionPanel import *
from interface.dialogs.WarningDialog import *
from interface.widgets.basicTestSetupWidget import *
from interface.SignalConnector import *


class BasicRepeatedTestSetupWidget(BasicTestSetupWidget):


    def __init__(self, indenter, backButtonCallback):
        # self.indenter = indenter
        
        super().__init__(indenter, backButtonCallback, "interface/widgets/basicRepeatedTestControls.ui")

        # # the buttons to disable during a measurement
        # self.toBlank = [self.backButton, self.positionButton, self.stepRateIncButton, self.stepRateDecButton, 
        #             self.preloadIncButton, self.preloadDecButton, self.preloadTimeIncButton, self.preloadTimeDecButton,
        #             self.maxLoadIncButton, self.maxLoadDecButton, self.maxLoadTimeIncButton, self.maxLoadTimeDecButton]

        # set up interface buttons
        self.repeatCountDisplay.setText(str(Config.DEFAULT_REPEAT_COUNT))
        self.repeatCountIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_REPEAT_COUNT, Config.MAX_REPEAT_COUNT, Config.REPEAT_COUNT_INCREMENT_SIZE, self.repeatCountDisplay))
        self.repeatCountDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_REPEAT_COUNT, Config.MAX_REPEAT_COUNT, -1 * Config.REPEAT_COUNT_INCREMENT_SIZE, self.repeatCountDisplay))
        
        
        print("init basic repeated test setup complete")
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
            # disable some buttons during the measurement
            for i in self.toBlank:
                i.setEnabled(False)

            self.indenter.takeStiffnessMeasurement(preload, preloadTime, maxLoad, maxLoadTime, stepRate, self.sigHandler.getAsyncSignal())


