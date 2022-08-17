
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import sys
import os

#custom class imports
from graphTools.ComparisonGrapher import *
from dataTools.Logger import *


class CompareWindow(QMainWindow):
    """ The class responsible for managing the main interface window.
    This class also defines what happend when buttons are pressed. """

    def __init__(self, dir, mainUIcallback):
        """ Create a new instance of the main window of the indenter controller.
        Parameters:
            dir (str): the directory the program was launched from """

        # the directory we launched from
        self.dir = dir

        # initialize Qt for the GUI
        QMainWindow.__init__(self)
        loadUi(os.path.join(self.dir, "interface/mainWindows/compareWindow.ui"), self)
        self.setWindowTitle("Indenter Control Panel")
        self.showFullScreen()

        # initialize the grapher functionality
        self.grapher = ComparisonGrapher(self.plotWidget)
        # initialize the logger for loading files
        self.logger = Logger()

        # set up bindings for the buttons
        self.clearButton.clicked.connect(self.grapher.clear)        # clear button
        self.viewButton.clicked.connect(self.grapher.cycleViews)    # view button
        self.loadButton.clicked.connect(self.loadFile)              # load button
        self.exitButton.clicked.connect(mainUIcallback)             # exit button
        return


    def getDirectory(self):
        """Returns a string to the directory in which files should be stored.
        Attempts to store to a USB stick before storing locally."""

        # check if a USB stick is inserted and set default path to it
        dirs = os.listdir("/media/pi")
        if len(dirs) != 0:
            directory = os.path.join("/media/pi", dirs[0]) + "/"
        # else save locally
        else:
            directory = os.path.join(self.dir, "Collected Data/")
        return directory


    def loadFile(self):
        """ Start a dialog to load data from a CSV file. """

        # start the dialog for picking a directory and file name
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load measurement from file", self.getDirectory(), "CSV Files (*.csv);;All Files (*)", options=options)
       
        # load data if the file name is valid
        if filename:
            measurementData = self.logger.loadFile(filename)
            self.grapher.addDataSet(measurementData)            

        return


    def exitProgram(self):
        """ Quits the program. """

        sys.exit()
        return

