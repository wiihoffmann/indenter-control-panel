
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
import sys
import os

class MainControl(QWidget):


    def __init__(self, parent):
        """ Make a new instance of the error window. """
        self.dir = parent.dir
        self.parent = parent
        
        super().__init__()
        loadUi(os.path.join(self.dir, "interface/widgets/mainControlWidget.ui"), self)

        self.exitButton.clicked.connect(self.exitProgram)               # exit button
        self.normalTestButton.clicked.connect(self.normal)

        print("here")
        return

    def normal(self):
        print(self.parent.buttonStack.indexOf(self.parent.temp))
        self.parent.buttonStack.setCurrentIndex(self.parent.buttonStack.indexOf(self.parent.temp2))
        print("swapping to default")

    def exitProgram(self):
        """ Quits the program. """
        sys.exit()
        return


