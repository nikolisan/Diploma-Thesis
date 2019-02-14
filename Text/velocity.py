import numpy

def velocity(dx, dy, dt, g, z, Nx, Ny):
  # where z is the calculated water profile
  # for the specific timestep we do the calculation
  # Instantiate arrays with 0s for better perfomance
  u = numpy.zeros((Ny + 2, Nx + 3))
  u1 = numpy.zeros((Ny + 2, Nx + 3))
  v = numpy.zeros((Ny + 2, Nx + 3))
  v1 = numpy.zeros((Ny + 2, Nx + 3))
  
  for i in range(1, Ny + 1):
    for j in range(1, Nx + 2):
      u1[i, j] = u[i, j] - (g*dt/dx**2) * (z[i+1, j] - 
          2*z[i, j] + z[i-1, j])
      v1[i, j] = v[i, j] - (g*dt/dy**2) * (z[i, j+1] - 
          2*z[i, j+1] + z[i, j+1])

  # * top (i = Ny)
  u1[-1, :] = u1[-2, :]
  v1[-1, :] = v1[-2, :]
  # * left (j = Nx)
  u1[:, -1] = u1[:, -2]
  v1[:, -1] = v1[:, -2]
  # * right (j = 0)
  u1[:, 0] = u1[:, 1]
  v1[:, 0] = v1[:, 1]

  u = numpy.copy(u1)
  v = numpy.copy(v1)
  
  return u, v