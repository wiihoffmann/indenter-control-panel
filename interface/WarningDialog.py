
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import os

class WarningDialog(QDialog):
    """ The class responsible for loading the error window. """

    def __init__(self, parent):
        """ Make a new instance of the error window. """
        self.dir = parent.dir
        
        super().__init__(parent)
        loadUi("interface/loadError.ui", self)
        loadUi(os.path.join(self.dir, "interface/loadError.ui"), self)
        self.setWindowTitle("ERROR!")
        return

