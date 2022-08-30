
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from threading import Timer
from datetime import datetime
import subprocess
import sys
import os

#custom class imports
from firmware.Indenter import *
from interface.dialogs.DirectionPanel import *
from interface.widgets.RegularTestSetupWidget import *
from interface.widgets.PPTTestSetupWidget import *
from interface.widgets.PPITestSetupWidget import *
from interface.widgets.TemporalSummationTestSetupWidget import *
import Config


class MainUI(QMainWindow):
    """ The class responsible for managing the main interface window.
    This class also defines what happend when buttons are pressed. """

    def __init__(self, compareCallback):
        """ Create a new instance of the main window of the indenter controller.
        Parameters:
            dir (str): the directory the program was launched from """

        # initialize Qt for the GUI
        QMainWindow.__init__(self)
        loadUi(os.path.join(os.getcwd(), "interface/mainWindows/mainWindow.ui"), self)
        self.setWindowTitle("Indenter Control Panel")
        # self.showFullScreen()

        # initialize the firmware/back end functionality
        self.indenter = Indenter(self.plotWidget)

        # build the control widgets
        self.regularTestSetupWidget = RegularTestSetupWidget(self.indenter, lambda: self.buttonStack.setCurrentIndex(0))
        self.PPTTestSetupWidget = PPTTestSetupWidget(self.indenter, lambda: self.buttonStack.setCurrentIndex(0))
        self.PPITestSetupWidget = PPITestSetupWidget(self.indenter, lambda: self.buttonStack.setCurrentIndex(0))
        self.TemporalSummationTestSetupWidget = TemporalSummationTestSetupWidget(self.indenter, lambda: self.buttonStack.setCurrentIndex(0))

        # add widgets to the stack and show the main widget
        self.buttonStack.addWidget(self.regularTestSetupWidget)
        self.buttonStack.addWidget(self.PPTTestSetupWidget)
        self.buttonStack.addWidget(self.PPITestSetupWidget)
        self.buttonStack.addWidget(self.TemporalSummationTestSetupWidget)

        # set up bindings for the buttons
        self.clearButton.clicked.connect(self.indenter.clearResults)    # clear button
        self.viewButton.clicked.connect(self.indenter.changeView)       # view button
        self.loadButton.clicked.connect(self.loadFile)                  # load button
        self.saveButton.clicked.connect(self.saveFile)                  # save button
        self.compareButton.clicked.connect(compareCallback)             # compare button
        self.exitButton.clicked.connect(self.exitProgram)               # exit button
        self.positionButton.clicked.connect(self.__openPositionWindow)  # positioning button
        self.setupButton.clicked.connect(self.goToSetup)
        return


    def __openPositionWindow(self):
        window = DirectionPanel()
        window.exec_()
        return


    def goToSetup(self):
        if self.regularTestRadioButton.isChecked():
            print("regular")
            self.buttonStack.setCurrentIndex(self.buttonStack.indexOf(self.regularTestSetupWidget))

        elif self.PPITestRadioButton.isChecked():
            self.buttonStack.setCurrentIndex(self.buttonStack.indexOf(self.PPITestSetupWidget))
            print("PPI test")

        elif self.PPTTestRadioButton.isChecked():
            print("PPT test")
            self.buttonStack.setCurrentIndex(self.buttonStack.indexOf(self.PPTTestSetupWidget))

        elif self.temporalSummationTestRadioButton.isChecked():
            self.buttonStack.setCurrentIndex(self.buttonStack.indexOf(self.TemporalSummationTestSetupWidget))
            print("temporal summation test")

        return


    def launchKeyboard(self):
        self.showMaximized()
        subprocess.run(["xvkbd", "-no-keypad", "-window", "Save measurement to file"])
        self.showFullScreen()
        return


    def getDirectory(self):
        """Returns a string to the directory in which files should be stored.
        Attempts to store to a USB stick before storing locally."""

        # check if a USB stick is inserted and set default path to it
        if os.path.isdir("/media/pi"):
            dirs = os.listdir("/media/pi")
            if len(dirs) != 0:
                directory = os.path.join("/media/pi", dirs[0]) + "/"
        # else save locally
        else:
            directory = os.path.join(os.getcwd(), "Collected Data/")
        return directory


    def buildFileName(self):
        # set default file name to the current date/time
        now = datetime.now()
        # dd-mm-YY H-M-S
        dt_string = now.strftime("%Y-%m-%d %H-%M-%S")
        print(self.indenter.getLastTestType())
        if(self.indenter.getLastTestType() == REGULAR_TEST_CODE):
            return dt_string + " regular"
        elif(self.indenter.getLastTestType() == PPI_TEST_CODE):
            return dt_string + " PPI"
        elif(self.indenter.getLastTestType() == PPT_TEST_CODE):
            return dt_string + " PPT"
        elif(self.indenter.getLastTestType() == TEMPORAL_SUMMATION_TEST_CODE):
            return dt_string + " Temporal Summation"
        return dt_string


    def saveFile(self):
        """ Start a dialog to save the current graph data into a CSV file. """
        
        # open the on screen keyboard once the next window has had a chance to open
        if Config.SHOW_KEYBOARD:
            Timer(.25, self.launchKeyboard).start()

        # start the dialog for picking a directory and file name
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save measurement to file", self.getDirectory() + self.buildFileName(), "CSV File (*.csv)", options=options)
        
        # save data if the file name is valid
        if filename:
            self.indenter.saveResults(filename)
        return


    def loadFile(self):
        """ Start a dialog to load data from a CSV file. """

        # start the dialog for picking a directory and file name
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load measurement from file", self.getDirectory(), "CSV Files (*.csv);;All Files (*)", options=options)
       
        # load data if the file name is valid
        if filename:
            self.indenter.loadAndShowResults(filename)
        return


    def exitProgram(self):
        """ Quits the program. """

        self.indenter.emergencyStop()
        sys.exit()
        return

