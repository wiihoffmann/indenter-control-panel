
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

class WarningDialog(QDialog):
    """ The class responsible for loading the error window. """

    def __init__(self, parent=None):
        """ Make a new instance of the error window. """
        
        super().__init__(parent)
        loadUi("interface/loadError.ui", self)
        return

