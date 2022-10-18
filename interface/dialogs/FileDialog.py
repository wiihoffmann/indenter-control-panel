
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from threading import Timer
from datetime import datetime
import subprocess
import os

# custom class imports
import Config
from firmware.Indenter import *


class FileDialog():
    
    def __init__(self, parent):
        self.parent = parent
        return


    def launchKeyboard(self):
        # if Config.FULLSCREEN_MODE: self.showMaximized()
        subprocess.run(["xvkbd", "-no-keypad", "-window", "Save measurement to file"])
        # if Config.FULLSCREEN_MODE: self.showFullScreen()
        return


    def getDirectory(self):
        """Returns a string to the directory in which files should be stored.
        Attempts to store to a USB stick before storing locally."""

        # check if a USB stick is inserted and set default path to it
        if os.path.isdir("/media/pi"):
            dirs = os.listdir("/media/pi")
            if len(dirs) != 0:
                return os.path.join("/media/pi", dirs[0]) + "/"
        # else save locally
        return os.path.join(os.getcwd(), "Collected Data/")


    def buildFileName(self, indenter):
        # set default file name to the current date/time
        now = datetime.now()
        # dd-mm-YY H-M-S
        dt_string = now.strftime("%Y-%m-%d %H-%M-%S")
        print(indenter.getLastTestType())
        if(indenter.getLastTestType() == REGULAR_TEST_CODE):
            return dt_string + " regular"
        elif(indenter.getLastTestType() == PPI_TEST_CODE):
            return dt_string + " PPI"
        elif(indenter.getLastTestType() == PPT_TEST_CODE):
            return dt_string + " PPT"
        elif(indenter.getLastTestType() == TEMPORAL_SUMMATION_TEST_CODE):
            return dt_string + " Temporal Summation"
        return dt_string


    def showSaveDialog(self, indenter):
        # open the on screen keyboard once the next window has had a chance to open
        if Config.SHOW_KEYBOARD:
            Timer(.25, self.launchKeyboard).start()

        # start the dialog for picking a directory and file name
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save measurement to file", self.getDirectory() + self.buildFileName(indenter), "CSV File (*.csv)", options=options)
        
        return filename


    def showLoadDialog(self):
        """ Start a dialog to load data from a CSV file. """

        # start the dialog for picking a directory and file name
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self.parent, "Load measurement from file", self.getDirectory(), "CSV Files (*.csv);;All Files (*)", options=options)

        return filename


    def showSavePromptDialog(self, indenter):
        reply = QMessageBox.question(self.parent, 'Save test data?', 'Do you want to save the test data?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            filename = self.showSaveDialog(indenter)
            indenter.saveResults(filename)
        return