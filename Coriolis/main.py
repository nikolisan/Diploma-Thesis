# -*- coding: utf-8 -*- 
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import gui
import calculate_traj

class MainUiClass(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super(MainUiClass, self).__init__(None)

        QtWidgets.QMessageBox.information(self, 'Coriolis Trajectory', 'If the window is too small, \n'
                                                                       'adjust the size manually.')

        self.setupUi(self)

        self.calculateBtn.clicked.connect(self.calculate_action)
        self.showBtn.clicked.connect(self.show_plot)

        self.actionAbout.triggered.connect(self.about)
        self.action_Exit.triggered.connect(self.closeEvent)

    def calculate_action(self):
        omega = self.omegaSpin.value()
        numSteps = self.stepSpin.value()
        phi = self.phiSpin.value()

        if phi < 0:
            # Check if the parcel is below equator
            # and invert the rotation rate
            omega = -omega

        radius = self.radiusSpin.value()
        x0 = self.xSpin.value()
        y0 = self.ySpin.value()
        u0 = self.uSpin.value()
        v0 = self.vSpin.value()

        if v0 == 0 and u0 == 0:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Please set different initial velocity.')
        elif phi == 0:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Please set different φ.\n'
                                                      'Coriolis force cannot be calculated on the equator.')
        else:
            self.calculateBtn.setEnabled(False)
            self.showBtn.setEnabled(False)
            self.stopBtn.setEnabled(True)
            self.computationThread = ThreadClass(omega, numSteps, phi, radius, x0, y0, u0, v0)

            self.stopBtn.clicked.connect(self.computationThread.terminate)

            self.computationThread.finished.connect(self.done)
            self.computationThread.start()

    def show_plot(self):
        animate = self.animateChk.isChecked()
        speed = self.speedSpin.value()
        calculate_traj.plot(radius, xc, yc, xi, yi, animate, speed)

    def done(self):
        self.stopBtn.setEnabled(False)
        self.calculateBtn.setEnabled(True)
        self.showBtn.setEnabled(True)
        self.fEdit.setText('{0:1.2e}'.format(f))
        self.rossbyEdit.setText('{0:1.2e}'.format(Ro))
        self.tEdit.setText('{0:1.2f}'.format(Th))
        QtWidgets.QMessageBox.information(self, 'Done', 'Calculations are completed!')
        self.show_plot()

    def about(self):
        QtWidgets.QMessageBox.information(self, 'About', 'This program calculates the trajectory of parcel under'
                                                         'the effect of the fictitious force, Coriolis. \n'
                                                         'Created by: Nick Andreakos')

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
            self, "Close",
            "Are you sure you want to quit?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            app.quit()
        else:
            pass


class ThreadClass(QtCore.QThread):
    def __init__(self, omega, numSteps, phi, R, x0, y0, u0, v0):
        QtCore.QThread.__init__(self)
        self.omega = omega
        self.numSteps = numSteps
        self.phi = phi
        self.R = R
        self.x0 = x0
        self.y0 = y0
        self.u0 = u0
        self.v0 = v0

    def __del__(self):
        self.wait()

    def run(self):
        global f, Ro, Th, xc, yc, xi, yi, radius
        radius = self.R
        # Thread logic goes here
        [f, Ro, Th, xc, yc, xi, yi] = calculate_traj.calculate(self.omega, self.numSteps, self.phi, self.R, self.x0,
                                                               self.y0, self.u0, self.v0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    if hasattr(QtWidgets.QStyleFactory, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    form = MainUiClass()
    form.show()
    sys.exit(app.exec_())
