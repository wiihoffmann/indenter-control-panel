
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
import sys
import os

class BasicTestSetupWidget(QWidget):


    def __init__(self, parent):
        """ Make a new instance of the error window. """
        self.dir = parent.dir
        
        super().__init__()
        loadUi(os.path.join(self.dir, "interface/widgets/basicTestControls.ui"), self)


        # # the buttons to disable during a measurement
        # self.toBlank = [self.clearButton, self.exitButton, self.loadButton, self.saveButton, self.positionButton,
        #             self.preloadIncButton, self.preloadDecButton, self.preloadTimeIncButton, self.preloadTimeDecButton,
        #             self.maxLoadIncButton, self.maxLoadDecButton, self.maxLoadTimeIncButton, self.maxLoadTimeDecButton,
        #             self.stepRateIncButton, self.stepRateDecButton, self.viewButton, self.compareButton]


        #self.backButton.clicked.connect(parent.returnToMain)               # exit button

        print("here")
        return


    def back(self):
        """ Quits the program. """
        print("quitting for now")
        sys.exit()
        return


