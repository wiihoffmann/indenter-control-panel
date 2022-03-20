from PyQt5 import QtCore
import pyqtgraph as pg
import threading

class Grapher():
    
    def __init__(self, graphHandle):
        self.graph = graphHandle
        self.xData = []
        self.stepData = []
        self.loadData = []
        
        self.orangePen = pg.mkPen('r', width=3)
        self.bluePen = pg.mkPen('b', width=3)

        self.graph.setBackground('w')
        self.graph.setLabel('left', 'Displacement', units ='steps')
        self.graph.setLabel('right', 'Force', units ='N')
        self.graph.setLabel('bottom', 'Sample number')

        self.loadLine =  self.graph.plot([], [], pen=self.orangePen)
        self.stepLine =  self.graph.plot([], [], pen=self.bluePen)

        self.lock = threading.Lock()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.refreshPlot)
        self.timer.start()
        return
    

    def refreshPlot(self):
        self.lock.acquire()
        self.loadLine.setData(self.xData, self.loadData)
        self.stepLine.setData(self.xData, self.stepData)
        self.lock.release()
        return


    def addDataPoint(self, step, load):
        self.lock.acquire()
        if self.xData == []:
            self.xData.append(1)
        else:
            self.xData.append(self.xData[-1]+1)
        self.stepData.append(step)
        self.loadData.append(load)
        self.lock.release()
        return


    def addDataFromPipe(self, pipe):
        self.pipeManagerhandle= threading.Thread(name = 'pipeManager', target = pipeManager, args=(self, pipe))
        self.pipeManagerhandle.start()


    def setData(self, x, step, load):
        self.lock.acquire()
        self.xData = x
        self.stepData = step
        self.loadData = load
        self.loadLine.setData(self.xData, self.loadData, pen=self.orangePen)
        self.stepLine.setData(self.xData, self.stepData, pen=self.bluePen)
        self.lock.release()
        return


    def getData(self):
        return self.xData, self.stepData, self.loadData


    def clear(self):
        self.lock.acquire()
        self.xData = []
        self.stepData = []
        self.loadData = []
        self.loadLine.clear()
        self.stepLine.clear()
        self.lock.release()

 
def pipeManager(self, pipe):
    done = False
    while not done:
        try:
            step, data = pipe.recv()
            self.addDataPoint(step, data)
        except EOFError:
            done = True
    return