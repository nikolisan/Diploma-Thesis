from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
import calculate

class Worker(QObject):

    # sig_done = pyqtSignal(float)

    def __init__(self, ts, tf, step, initial):
        super().__init__()
        self.step = step
        self.ts = ts
        self.tf = tf
        self.initial = initial

    @pyqtSlot()
    def work(self):
        print("Hello from thread")
        # x_t = calculate.get_lorenz(self.step, self.ts, self.tf, self.initial)
        # print(type(x_t))
        # self.sig_done.emit(1.0)
