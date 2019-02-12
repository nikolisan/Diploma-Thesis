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
isWaterProf = os.path.isfile("waterProf.pickle")

# Dimensions: space in (m), time in (sec)
Lx = 25000  # length in x direction
Ly = 25000  # length in y direction
H = 50      # depth
g = 9.807   # gravity acceleration

# Incoming Wave properties
T = 4000             # incoming tidal wave period -> 12h, 25h
A = 0.4                # wave amplitude (m) -> 0.4m
c = numpy.sqrt(g * H)   # wave celerity

# Discretization variables
Nx = 50  # Number of cells in x direction
Ny = 50  # Number of cells in y direction

# Variables for run
days = 0.5

# # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # #              Calculations           # # # # #
# * Calculate the water surface after given  days * #
x, y, dx, dy, dt = water_level.variables(Nx, Ny, Lx, Ly, c, T, A)
if not isWaterProf:
    timeseriesPoint = (50, 25)
    heta, h_, t_= water_level.calculate_water_level(Lx, Nx, Ny, dx, dy, dt, c, days, timeseriesPoint)
    waterProfToSave = {
        "heta": heta,
        "h_": h_,
        "t_": t_
    }
    with open('waterProf.pickle', 'wb') as f:
        # Pickle the 'waterProf' dictionary using the highest protocol available.
        pickle.dump(waterProfToSave, f, pickle.HIGHEST_PROTOCOL)
        print('Water profile result saved')
else:
    print('Water profile result loading')
    with open('waterProf.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        waterProf = pickle.load(f)
        heta, h_, t_ = waterProf.values()


# # # # # # # # # # # # # # # # # # # # # # #
# # # #        Plotting results     # # # # #
# * Plot the contour of the water surface * #
plotting.contour_plot(x, y, heta)

import matplotlib.pyplot as plt
plt.plot(t_, h_)
plt.show()
