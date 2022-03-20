# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from interface.MainUI import *

app = QApplication([])
window = MainWindow("interface/dialog.ui")
window.show()
app.exec_()


