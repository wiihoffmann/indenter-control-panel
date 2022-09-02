
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
import os

class WarningDialog(QDialog):
    """ The class responsible for loading the error window. """

    def __init__(self, parent):
        """ Make a new instance of the error window. """
        
        super().__init__(parent)
        loadUi(os.path.join(os.getcwd(), "interface/dialogs/loadError.ui"), self)
        self.setWindowTitle("ERROR!")
        return

