# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from MainUI import *

app = QApplication([])
window = MainWindow("dialog.ui")
window.show()
window.updateGraph()
app.exec_()


