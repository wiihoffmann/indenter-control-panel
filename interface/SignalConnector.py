from PyQt5.QtCore import pyqtSignal, QThread
from multiprocessing import Event

class SignalConnector(QThread):
    """ This class allows us to synchronize signals from traditional python processes (asynchronous)
    with the QT GUI loop and QThreads (synchronous). """

    QTsignal = pyqtSignal()
    asyncEvent = Event()

    def __init__(self):
        """ Initialize a new signal handler"""
        super().__init__()
        self.asyncEvent.clear()


    def connect(self, function):
        self.QTsignal.connect(function)

    def setAsyncSignal(self):
        self.asyncEvent.set()

    def getAsyncSignal(self):
        return self.asyncEvent

    def run(self):
        """ The main loop of the signal handler. """
        while True:
            try:
                # wait for an asynchronous done signal, then send a synchronous done signal
                self.asyncEvent.wait()
                self.QTsignal.emit()
                self.asyncEvent.clear()
            except Exception as e:
                print(e)
        return

