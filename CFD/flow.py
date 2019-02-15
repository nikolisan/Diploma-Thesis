# -*- coding: utf-8 -*-
# -----------------------------------------------------------------
# Model of a tidal flow in a closed gulf,
# with one open sea boundary.
# Assumptions:
#   * Linearized eqn's (no non linear convection, friction)
#   * No bed friction
#   * Flow is not affected by the Coriolis force
#   * Bed elevation is constant
#   * Eqn's integrated over depth
#   * Sinusoidal incoming wave at the open boundary
# Numerical Method: Finite Differences
#   * Forward differences in time (time - marching solver)
#   * Central differences in space
#   * Central differences in space & time for the wave
# -----------------------------------------------------------------

import numpy
import plotting
import water_level

import pickle
import os
import math
import time
filename = '5a'
isWaterProf = os.path.isfile(filename)

# Dimensions: space in (m), time in (sec)
Lx = 25000  # length in x direction
Ly = 40000  # length in y direction
H = 50      # depth
g = 9.807   # gravity acceleration

# Incoming Wave properties
T = 4000             # incoming tidal wave period -> 12h, 25h
A = 0.4               # wave amplitude (m) -> 0.4m
c = numpy.sqrt(g * H)   # wave celerity

# Discretization variables
Nx = 25  # Number of cells in x direction
Ny = 25  # Number of cells in y direction

# Variables for run
days = 5

# # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # #              Calculations           # # # # #
# * Calculate the water surface after given  days * #
x, y, dx, dy, dt = water_level.variables(Nx, Ny, Lx, Ly, c, g, H, T, A)
if not isWaterProf:
    timeseriesPoint = (25, 12)
    heta, u_vel, v_vel, h_, uvel_, vvel_, t_ = water_level.calculate_water_level(Lx, Ly, Nx, Ny, dx, dy, dt, c, days, timeseriesPoint)
    waterProfToSave = {
        "heta": heta,
        "h_": h_,
        "t_": t_,
        "u_vel": u_vel,
        "v_vel": v_vel,
        "uvel_": uvel_,
        "vvel_": vvel_
    }
    with open(filename, 'wb') as f:
        # Pickle the 'waterProf' dictionary using the highest protocol available.
        pickle.dump(waterProfToSave, f, pickle.HIGHEST_PROTOCOL)
        print('Results saved')
else:
    print('Results loading')
    with open(filename, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        waterProf = pickle.load(f)
        heta, h_, t_, u_vel, v_vel, uvel_, vvel_ = waterProf.values()


# # # # # # # # # # # # # # # # # # # # # # #
# # # #        Plotting results     # # # # #
# # # # # # # # # # # # # # # # # # # # # # #
plotting.final_2d(x, y, heta, v_vel, u_vel, filename)
# time.sleep(10)
plotting.contour(x, y, u_vel, filename)
# time.sleep(10)
plotting.timeseries(t_, h_, 'Χρονοσειρά ανύψωσης ελεύθερης επιφάνειας', 'Χρόνος (s)', 'Ανύψωση (m)', filename+'_h')
# time.sleep(10)
plotting.timeseries(t_, uvel_, 'Χρονοσειρά ταχύτητας', 'Χρόνος (s)', 'Ταχύτητα (m/s)', filename+'_u')
