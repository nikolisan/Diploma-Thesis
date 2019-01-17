import random
import numpy as np
from scipy.integrate import odeint
import file_utils

def lorenz(state, t):
    x = state[0]
    y = state[1]
    z = state[2]

    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0
    # compute state derivatives
    xd = sigma * (y - x)
    yd = (rho - z) * x - y
    zd = x * y - beta * z
    # return the state derivatives
    return [xd, yd, zd]

def get_lorenz(step, ts, tf, x0):
    td = int((tf - ts) / step)
    t = np.linspace(ts, tf, td)
    x_t = np.asarray([odeint(lorenz, x0i, t) for x0i in x0])
    if len(x_t[0]) == td:
        print('New system calculated')
    return x_t

if __name__ == "__main__":
    step = 0.01
    ts = 0
    tf = 100
    num_traj = 2
    x0 = [(random.randint(-25, 25), 
           random.randint(-35, 35), 
           random.randint(5, 55)) for traj in range(num_traj)]
    x_t = get_lorenz(step, ts, tf, x0)
    file_utils.save_to_file(x_t)
    array = file_utils.open_file()
    print(array == x_t)
