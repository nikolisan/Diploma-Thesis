# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm

def final_2d(x, y, u, v_vel, u_vel, name):
    plt.contourf(x, y, u, alpha=0.7, cmap=cm.coolwarm)
    plt.colorbar()
    plt.quiver(x, y, v_vel, u_vel)
    plt.title('Ανυψωση ελεύθερης επιφάνειας και ταχύτητα')
    plt.xlabel('Πλάτος (m)')
    plt.ylabel('Μήκος (m)')
    plt.savefig(name + 'final_2d.png', bbox_inches='tight')
    plt.show()

def contour(x, y, u, name):
    plt.contourf(x, y, u, alpha=0.7)
    plt.colorbar()
    plt.title('Ταχύτητα')
    plt.xlabel('Πλάτος (m)')
    plt.ylabel('Μήκος (m)')
    plt.savefig(name + 'contour.png', bbox_inches='tight')
    plt.show()

def timeseries(t, u, title, xaxis, yaxis, name):
    plt.plot(t, u)
    plt.grid(True)
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.savefig(name + 'ts.png', bbox_inches='tight')
    plt.show()
