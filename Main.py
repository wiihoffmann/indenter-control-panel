#!/usr/bin/python3
# line above lets us launch the program with ./Main.py instead of "python3 Main.py"

from interface.mainWindows.MainUI import *
from interface.mainWindows.CompareWindow import *
import os


# get the path the program was launched from
dir = os.path.dirname(__file__)
window = None


def openCompareWindow(self):
    global window
    window.close()
    window = CompareWindow(dir, openMainWindow)
    window.show()
    return


def openMainWindow(self):
    global window
    window.close()
    window = MainUI(openCompareWindow)
    window.show()
    return


if __name__ == "__main__":
    # launch the main program
    app = QApplication([])
    window = MainUI(openCompareWindow)
    window.show()
    app.exec_()

