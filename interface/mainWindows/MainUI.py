
from PyQt5.uic import loadUi
import sys
import os

#custom class imports
from firmware.Indenter import *
from interface.dialogs.DirectionPanel import *
from interface.dialogs.FileDialog import *
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
        if Config.FULLSCREEN_MODE: self.showFullScreen()

        # initialize the firmware/back end functionality
        self.indenter = Indenter(self.plotWidget)

        # initialize widget for saving and loading files
        self.fileDialog = FileDialog(self)

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
        self.clearButton.clicked.connect(self.clear)                    # clear button
        self.viewButton.clicked.connect(self.indenter.changeView)       # view button
        self.loadButton.clicked.connect(self.loadFile)                  # load button
        self.saveButton.clicked.connect(self.saveFile)                  # save button
        self.compareButton.clicked.connect(compareCallback)             # compare button
        self.exitButton.clicked.connect(self.exitProgram)               # exit button
        self.positionButton.clicked.connect(self.__openPositionWindow)  # positioning button
        self.setupButton.clicked.connect(self.goToSetup)
        return


    def __openPositionWindow(self):
        if Config.FULLSCREEN_MODE: self.showMaximized()
        window = DirectionPanel()
        window.exec_()
        if Config.FULLSCREEN_MODE: self.showFullScreen()
        return


    def clearLCDreadouts(self, keepLast = False):
        if(not keepLast or self.indenter.getLastTestType() != PPI_TEST_CODE):
            self.PPITestSetupWidget.waitMSG.show()
            self.PPITestSetupWidget.VAS_LCD.hide()
        
        if(not keepLast or self.indenter.getLastTestType() != PPT_TEST_CODE):
            self.PPTTestSetupWidget.waitMSG.show()
            self.PPTTestSetupWidget.loadLCD.hide()
        return


    def clear(self):
        self.indenter.clearResults()
        self.clearLCDreadouts(False)
        return


    def goToSetup(self):
        self.clearLCDreadouts(True)
        if self.regularTestRadioButton.isChecked():
            self.buttonStack.setCurrentIndex(self.buttonStack.indexOf(self.regularTestSetupWidget))

        elif self.PPITestRadioButton.isChecked():
            self.buttonStack.setCurrentIndex(self.buttonStack.indexOf(self.PPITestSetupWidget))

        elif self.PPTTestRadioButton.isChecked():
            self.buttonStack.setCurrentIndex(self.buttonStack.indexOf(self.PPTTestSetupWidget))

        elif self.temporalSummationTestRadioButton.isChecked():
            self.buttonStack.setCurrentIndex(self.buttonStack.indexOf(self.TemporalSummationTestSetupWidget))

        return


    def saveFile(self):
        """ Start a dialog to save the current graph data into a CSV file. """
        filename = self.fileDialog.showSaveDialog(self.indenter)
        
        # save data if the file name is valid
        if filename:
            if Config.FULLSCREEN_MODE: self.showMaximized()
            self.indenter.saveResults(filename)
            if Config.FULLSCREEN_MODE: self.showFullScreen()
        return


    def loadFile(self):
        """ Start a dialog to load data from a CSV file. """
        if Config.FULLSCREEN_MODE: self.showMaximized()
        filename = self.fileDialog.showLoadDialog()
        if Config.FULLSCREEN_MODE: self.showFullScreen()

        # load data if the file name is valid
        if filename:
            self.indenter.loadAndShowResults(filename)
        return


    def exitProgram(self):
        """ Quits the program. """

        self.indenter.emergencyStop()
        sys.exit()
        return

