
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import os

#custom class imports
from graphTools.ComparisonGrapher import *
from interface.dialogs.FileDialog import *
from dataTools.Logger import *


class CompareWindow(QMainWindow):
    """ The class responsible for managing the main interface window.
    This class also defines what happend when buttons are pressed. """

    def __init__(self, mainUIcallback):
        """ Create a new instance of the main window of the indenter controller.
        Parameters:
            dir (str): the directory the program was launched from """

        # initialize Qt for the GUI
        QMainWindow.__init__(self)
        loadUi(os.path.join(os.getcwd(), "interface/mainWindows/compareWindow.ui"), self)
        self.setWindowTitle("Indenter Control Panel")
        if Config.FULLSCREEN_MODE: self.showFullScreen()

        # initialize the grapher functionality
        self.grapher = ComparisonGrapher(self.plotWidget)
        # initialize the logger for loading files
        self.logger = Logger()
        # initialize widget for saving and loading files
        self.fileDialog = FileDialog(self)

        # set up bindings for the buttons
        self.clearButton.clicked.connect(self.grapher.clear)        # clear button
        self.viewButton.clicked.connect(self.grapher.cycleViews)    # view button
        self.loadButton.clicked.connect(self.loadFile)              # load button
        self.exitButton.clicked.connect(mainUIcallback)             # exit button
        return


    def loadFile(self):
        """ Start a dialog to load data from a CSV file. """
        filename = self.fileDialog.showLoadDialog()
    
        # load data if the file name is valid
        if filename:
            measurementData = self.logger.loadFile(filename)
            self.grapher.addDataSet(measurementData)            
        return

