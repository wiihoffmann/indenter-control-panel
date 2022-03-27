#!/usr/bin/python3
# line above lets us launch the program with ./Main.py instead of "python3 Main.py"

from interface.MainUI import *
import os

# get the path the program was launched from
dir = os.path.dirname(__file__)

# launch the main program
app = QApplication([])
window = MainWindow(dir)
window.show()
app.exec_()

