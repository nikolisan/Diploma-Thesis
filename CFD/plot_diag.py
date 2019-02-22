import numpy
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm
import pickle
import numpy as np

def timeseries(t1, u1, t2, u2, f1, f2, title, xaxis, yaxis):
    plt.plot(t1, u1, 'b', alpha=0.5, label=f1)
    plt.plot(t2, u2, 'r-', alpha=0.5, label=f2)
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.xticks(np.arange(8100, 8300, step=1))
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,4))
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.show()

def newPlot(x_axis, y_axis, color, legend):
    plt.plot(x_axis, y_axis, color , alpha=0.5, label=legend)
    
def plotShow(title, xaxis_title, yaxis_title,):
    plt.title(title)
    plt.xlabel(xaxis_title)
    plt.ylabel(yaxis_title)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,4))
    plt.legend(loc='right')
    plt.grid(True)
    plt.show()
    
filename1 = '1a'
filename2 = '2a'

with open(filename1, 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    waterProf = pickle.load(f)
    heta, h_1, t_1, u_vel, v_vel, uvel_1, vvel_ = waterProf.values()

with open(filename2, 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    waterProf = pickle.load(f)
    heta, h_2, t_2, u_vel, v_vel, uvel_2, vvel_ = waterProf.values()

timeseries(t_1, h_1, t_2, h_2, filename1, filename2, 'Χρονοσειρά ανύψωσης ελεύθερης επιφάνειας', 'Χρόνος (s)', 'Ανύψωση (m)')
timeseries(t_1, uvel_1, t_2, uvel_2, filename1, filename2, 'Χρονοσειρά ταχύτητας', 'Χρόνος (s)', 'Ταχύτητα (m/s)')