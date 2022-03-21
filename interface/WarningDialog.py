
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

class WarningDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        loadUi("interface/loadError.ui", self)