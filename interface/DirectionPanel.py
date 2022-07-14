from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import os

from firmware.Communicator import *
import Config

class DirectionPanel(QDialog):

    def __init__(self, parent, dir):
        self.dir = dir
        self.comm = Communicator()

        # initialize Qt for the GUI
        super().__init__(parent)
        loadUi(os.path.join(self.dir, "interface/directionPad.ui"), self)
        self.setWindowTitle("Position control panel")

        # set up button actions
        self.forwardButton.clicked.connect(self.__moveForward)
        self.backwardButton.clicked.connect(self.__moveBackward)
        self.leftButton.clicked.connect(self.__moveLeft)
        self.rightButton.clicked.connect(self.__moveRight)
        self.upButton.clicked.connect(self.__moveUp)
        self.downButton.clicked.connect(self.__moveDown)
        self.doneButton.clicked.connect(self.__done)
        return


    def __moveLeft(self):
        if self.flipLeftRightCheck.isChecked():
            self.comm.moveYAxisUp(Config.JOG_SPEED)
        else:
            self.comm.moveYAxisDown(Config.JOG_SPEED)
        return


    def __moveRight(self):
        if self.flipLeftRightCheck.isChecked():
            self.comm.moveYAxisDown(Config.JOG_SPEED)
        else:
            self.comm.moveYAxisUp(Config.JOG_SPEED)
        return


    def __moveForward(self):
        if self.flipFrontBackCheck.isChecked():
            self.comm.moveXAxisUp(Config.JOG_SPEED)
        else:
            self.comm.moveXAxisDown(Config.JOG_SPEED)
        return


    def __moveBackward(self):
        if self.flipFrontBackCheck.isChecked():
            self.comm.moveXAxisDown(Config.JOG_SPEED)
        else:
            self.comm.moveXAxisUp(Config.JOG_SPEED)
        return


    def __moveDown(self):
        if Config.INVERT_DIR:
            self.comm.moveZAxisDown(Config.JOG_SPEED)
        else:
            self.comm.moveZAxisUp(Config.JOG_SPEED)
        return
    

    def __moveUp(self):
        if Config.INVERT_DIR:
            self.comm.moveZAxisUp(Config.JOG_SPEED)
        else:
            self.comm.moveZAxisDown(Config.JOG_SPEED)
        return


    def __done(self):
        self.close()
        return

