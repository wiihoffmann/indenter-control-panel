#!/usr/bin/python3
# line above lets us launch the program with ./Main.py instead of "python3 Main.py"

import RPi.GPIO as GPIO
from interface.MainUI import *
from interface.CompareWindow import *
import os

window = None

# get the path the program was launched from
dir = os.path.dirname(__file__)


def openCompareWindow(self):
    global window

#    window.indenter.graph.stopLiveUpdate()  #TODO: remove this line once other stuff is fixed

    window.close()    
    GPIO.cleanup()
    window = CompareWindow(dir, openMainWindow)
    window.show()
    return


def openMainWindow(self):
    global window
    window.close()
    window = MainUI(dir, openCompareWindow)
    window.show()
    return


if __name__ == "__main__":
    # launch the main program
    app = QApplication([])
    window = MainUI(dir, openCompareWindow)
    window.show()
    app.exec_()

