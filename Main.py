#!/usr/bin/python3
# line above lets us launch the program with ./Main.py instead of "python3 Main.py"

from interface.mainWindows.MainUI import *
from interface.mainWindows.CompareWindow import *
import os


# get the path the program was launched from
dir = os.path.dirname(__file__)
os.chdir(dir)
window = None


def openCompareWindow(self):
    global window
    window.close()
    window = CompareWindow(openMainWindow)
    window.show()
    return


def openMainWindow(self):
    global window
    window.close()
    window = MainUI(openCompareWindow)
    window.show()
    return


if __name__ == "__main__":
    print("Starting control panel ... ", end = "")
    # launch the main program
    app = QApplication([])
    window = MainUI(openCompareWindow)
    window.show()
    print("done!")
    app.exec_()

