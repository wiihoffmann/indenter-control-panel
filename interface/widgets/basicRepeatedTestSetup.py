
import Config
from interface.widgets.basicTestSetupWidget import *
from interface.dialogs.DirectionPanel import *
from interface.dialogs.WarningDialog import *


class BasicRepeatedTestSetupWidget(BasicTestSetupWidget):


    def __init__(self, indenter, backButtonCallback):
        self.indenter = indenter

        super().__init__(indenter, backButtonCallback, "interface/widgets/basicRepeatedTestControls.ui")

        # add buttons to disable during a measurement
        self.toBlank.append([self.repeatCountIncButton, self.repeatCountDecButton])

        # set up repeat count buttons
        self.repeatCountDisplay.setText(str(Config.DEFAULT_REPEAT_COUNT))
        self.repeatCountIncButton.pressed.connect( lambda: self.updateReadout(Config.MIN_REPEAT_COUNT, Config.MAX_REPEAT_COUNT, Config.REPEAT_COUNT_INCREMENT_SIZE, self.repeatCountDisplay))
        self.repeatCountDecButton.pressed.connect( lambda: self.updateReadout(Config.MIN_REPEAT_COUNT, Config.MAX_REPEAT_COUNT, -1 * Config.REPEAT_COUNT_INCREMENT_SIZE, self.repeatCountDisplay))
 
        print("init basic repeated test setup complete")
        return


    def startMeasurement(self):
        """ Initiates a stiffness measurement. """

        print(self.testCount)

        # get the measurement parameters from the readouts
        preload = int(self.preloadDisplay.text()[:-2])
        maxLoad = int(self.maxLoadDisplay.text()[:-2])
        preloadTime = int(self.preloadTimeDisplay.text()[:-2])
        maxLoadTime = int(self.maxLoadTimeDisplay.text()[:-2])
        stepRate = int(self.stepRateDisplay.text())
        testIterations = int(self.repeatCountDisplay.text())
        
        # reset variables after performing the required number of tests
        if self.testCount >= testIterations:
            print("here 1")
            self.testCount = 0
            self.enableButtons()
        # if the preload is larger than the max load, issue a warning
        elif preload >= maxLoad:
            print("here 2")
            dlg = WarningDialog(self)
            dlg.exec()
            dlg.raise_()
        # else start the measurement
        else:
            print("here 3")
            self.testCount += 1

            # set up the signal handler for the done signal
            self.sigHandler.connect(self.startMeasurement)
            self.sigHandler.start()

            # disable some buttons during the measurement
            for i in self.toBlank:
                i.setEnabled(False)

            # wait for previous measurement thread to close
            while(self.indenter.measurementInProgress()):
                time.sleep(0)
            self.indenter.takeStiffnessMeasurement(preload, preloadTime, maxLoad, maxLoadTime, stepRate, self.sigHandler.getAsyncSignal())
        return

