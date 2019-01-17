from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import numpy as np
from scipy.integrate import odeint
import random

import gui
import file_utils
import calculate
from calc_thread import Worker

from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import animation
from matplotlib import pyplot as plt


class MyApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.make_connections()
        col_headers = ['X', 'Y', 'Z']
        self.initialPointsTbl.setHorizontalHeaderLabels(col_headers)

        self.initPoints = []
        self.x_t = []
        # Inits for animation
        self.init_figure()
        self.fig = self.widget.fig
        self.stopped = True
        self.rotval = 2
        self.anispeed = 2
        self.playBtn.setEnabled(False)

    def make_connections(self):
        self.calculateBtn.clicked.connect(self.calculate)
        self.addPointBtn.clicked.connect(self.addPoint)
        self.playBtn.clicked.connect(self.stop_animation)
        self.initBtn.clicked.connect(self.init_figure)
        self.aniSpeedBtn.sliderReleased.connect(self.speed_changed)
        self.rotSpeedBtn.sliderReleased.connect(self.rotation_changed)
        self.aniInitAction.triggered.connect(self.init_figure)
        self.aniPlay_Action.triggered.connect(self.stop_animation)
        self.saveBtn.clicked.connect(self.save_fig)
        self.aniSave_Action.triggered.connect(self.save_fig)
        self.about_Action.triggered.connect(self.about)
        self.close_Action.triggered.connect(lambda r: QtWidgets.QApplication.instance().quit())
        self.initialPointsTbl.doubleClicked.connect(self.delete_point)

    def about(self):
        QtWidgets.QMessageBox.information(self, 'About', 'An interactive plotter for the Lorenz System. \n'
                                                         'Coded by: Nick Andreakos, 2018')
    def delete_point(self):
        rows = sorted(set(index.row() for index in self.initialPointsTbl.selectedIndexes()))
        for row in rows:
            x = float(self.initialPointsTbl.item(row, 0).text())
            y = float(self.initialPointsTbl.item(row, 1).text())
            z = float(self.initialPointsTbl.item(row, 2).text())
            rmitem = [x, y, z]
            self.initPoints = [point for point in self.initPoints if rmitem != point]
            self.initialPointsTbl.removeRow(row)

 
    def calculate(self):
        if not self.initPoints == []:
            self.playBtn.setEnabled(True)
            self.aniPlay_Action.setEnabled(True)

            step = self.stepSpin.value()
            ts = self.tsSpin.value()
            tf = self.tfSpin.value()
            self.x_t = calculate.get_lorenz(step, ts, tf, self.initPoints)
            self.animate_plot()
            self.calculateBtn.setText('Restart')

        else:
            QtWidgets.QMessageBox.critical(self, 'Error', 'No initial points selected.')

    def addPoint(self):
        x = self.x1Spin.value()
        y = self.y1Spin.value()
        z = self.z1Spin.value()
        newPoint = [x, y, z]
        if not newPoint in self.initPoints:
            self.initPoints.append(newPoint)
            print('New point added.')
            rowPosition = len(self.initPoints) - 1
            self.initialPointsTbl.insertRow(rowPosition)
            self.initialPointsTbl.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(x)))
            self.initialPointsTbl.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(y)))
            self.initialPointsTbl.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(z)))
        else:
            QtWidgets.QMessageBox.critical(self, 'Error', 'The point you try to add already \n'
                                                          'exists.')

    # ---------------------ANIMATION STUFF------------------------------ #
    def save_fig(self):
        try:
            file_utils.save_fig(self.fig)
            QtWidgets.QMessageBox.information(self, 'Success', 'The figure saved.')
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, 'Error saving figure', err.args[0])
            print(err)


    def rotation_changed(self):
        self.rotval = self.rotSpeedBtn.value()
        print('New rotation speed: %i' % self.rotval)
        if self.calculateBtn.text() == 'Restart':
            QtWidgets.QMessageBox.information(self, 'Restart required', 'Press the Stop and then the Restart button \n'
                                                                        'to apply changes.')

    def speed_changed(self):
        self.anispeed = self.aniSpeedBtn.value()
        print('New animation speed: %i' % self.anispeed)
        if self.calculateBtn.text() == 'Restart':
            QtWidgets.QMessageBox.information(self, 'Restart required', 'Press the Stop and then the Restart button \n'
                                                                        'to apply changes.')

    def init_figure(self):
        self.widget.canvas.ax.clear()
        self.widget.canvas.ax.grid()
        self.widget.canvas.ax.set_xlim(-50, 50)
        self.widget.canvas.ax.set_ylim(-50, 50)
        self.widget.canvas.ax.set_zlim(-50, 50)
        colors = plt.cm.jet(np.linspace(0, 1, len(self.initPoints)))
        self.lines = sum([self.widget.canvas.ax.plot([], [], [], '-',c=color, lw=1) for color in colors], [])
        self.pts = sum([self.widget.canvas.ax.plot([], [], [], '.', c=color) for color in colors],[])
        self.widget.canvas.draw()

    def setup_animation(self):
        self.init_figure()
        for line in self.lines:
            self.line = self.widget.canvas.ax.plot([], [], [])
        self.stopped = False

    def update_figure(self, i, rot, sp):
        i_ = i
        i = (sp * i) % self.x_t.shape[1]
        for xi, line, pt in zip(self.x_t, self.lines, self.pts):
            x, y, z = xi[:i].T
            line.set_data(x, y)
            line.set_3d_properties(z)
            pt.set_data(x[-1:], y[-1:])
            pt.set_3d_properties(z[-1:])

        if rot > 0:
            i_ = (rot * i_) % self.x_t.shape[1]
            self.widget.canvas.ax.view_init(30, 0.3 * i_)

        return self.lines + self.pts

    def stop_animation(self):
        if self.stopped:
            self.aniPlay_Action.setText('Stop')
            self.playBtn.setText('Stop')
            self.anim.event_source.start()
            self.stopped = not self.stopped
        else:
            self.aniPlay_Action.setText('Play')
            self.playBtn.setText('Play')
            self.anim.event_source.stop()
            self.stopped = not self.stopped

    def animate_plot(self):
        self.init_figure()
        self.frames = int(len(self.x_t[0])/self.anispeed)
        if self.stopped:
            self.widget.canvas.ax.view_init(30,50)
            self.widget.canvas.draw()
            self.stopped = False
            self.playBtn.setText('Stop')
            self.aniPlay_Action.setText('Stop')
            try:
                if len(self.x_t )> 0:
                    self.anim = animation.FuncAnimation(self.widget.canvas.ax.get_figure(),
                                                        self.update_figure,
                                                        init_func=self.setup_animation,
                                                        frames=self.frames,
                                                        fargs=[self.rotval, self.anispeed],
                                                        interval=50, repeat=False)

            except Exception as err:
                print(err)

            self.widget.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
if hasattr(QtWidgets.QStyleFactory, 'AA_UseHighDpiPixmaps'):
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
form = MyApp()
form.show()
sys.exit(app.exec_())
