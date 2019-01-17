import numpy as np
from PyQt5 import QtWidgets


def save_fig(fig):
    fname = QtWidgets.QFileDialog.getSaveFileName(caption='Save current figure', filter='Image (*.png)')
    if fname[0]:
        fig.savefig(fname[0], bbox_inches='tight')
