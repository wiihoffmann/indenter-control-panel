
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
import sys
import os

class basicTestSetupWidget(QWidget):


    def __init__(self, parent):
        """ Make a new instance of the error window. """
        self.dir = parent.dir
        
        super().__init__()
        loadUi(os.path.join(self.dir, "interface/widgets/basicTestControls.ui"), self)

        self.backButton.clicked.connect(parent.returnToMain)               # exit button

        print("here")
        return


    def back(self):
        """ Quits the program. """
        print("quitting for now")
        sys.exit()
        return


