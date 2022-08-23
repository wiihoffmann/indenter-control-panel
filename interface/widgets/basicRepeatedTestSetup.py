
import Config
from interface.widgets.basicTestSetupWidget import *
from interface.dialogs.DirectionPanel import *
from interface.dialogs.WarningDialog import *


class BasicRepeatedTestSetupWidget(BasicTestSetupWidget):


    def __init__(self, indenter, backButtonCallback):
        self.indenter = indenter

        super().__init__(indenter, backButtonCallback, "interface/widgets/basicRepeatedTestControls.ui")

        # add buttons to disable during a measurement
        self.toBlank.extend([self.repeatCountIncButton, self.repeatCountDecButton])

        # set up repeat count buttons
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
        repeatCount = int(self.repeatCountDisplay.text())

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

            self.indenter.takeStiffnessMeasurement(preload, preloadTime, maxLoad, maxLoadTime, stepRate, self.sigHandler.getAsyncSignal(), iterations = repeatCount)

