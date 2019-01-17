import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot_circle(center, radius):
    """
    Plots a circle using the parametric equations
    :param center: A list of the circle's center: [x,y]
    :param radius: The radius of the circle
    :return: None
    """
    fig = plt.figure(facecolor='#969696')
    fig.canvas.set_window_title('Coriolis Trajectory')

    center = tuple(center)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)

    ax.tick_params(axis='both', which='major', labelsize=9)

    tickfmt = ticker.ScalarFormatter(useMathText=True)
    tickfmt.set_powerlimits((-3, 3))
    ax.xaxis.set_major_formatter(tickfmt)
    ax.yaxis.set_major_formatter(tickfmt)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')

    ax.grid(color='#969696', linestyle='--')
    circle = plt.Circle(center, radius, color='k', fill=False)
    ax.add_patch(circle)

    ax.plot()
    plt.show(block=False)
    return

def update(num, x1, y1, x2, y2, line01, line02):
    line01.set_data(x1[:num], y1[:num])
    line02.set_data(x2[:num], y2[:num])
    return line01, line02

def calculate(omega, numSteps, phi, R, x0, y0, u0, v0):
    # Calculation of the Coriolis parameter
    f = 2 * omega * np.sin(np.deg2rad(phi))

    # Calculation of the inertial oscillation characteristics
    T = 2 * np.pi / abs(f)
    Th = T / 3600  # Period in hours

    Dt = T / numSteps

    if not u0 == v0:
        vel = max(abs(u0), abs(v0))
        Ro = abs(vel / (R * omega))
    else:
        Ro = abs(u0 / (R * omega))

    xi = [x0]
    yi = [y0]
    xc = [x0]
    yc = [y0]

    theta = 0
    t = 0
    i = 0

    while True:
        i = i + 1
        t = t + Dt
        theta = theta + omega * Dt

        # Parcel's Position on the Inertial
        x1 = x0 + Dt * u0
        y1 = y0 + Dt * v0

        # Parcel's Position translated to the
        # rotating frame
        xc1 = x1 * np.cos(theta) + y1 * np.sin(theta)
        yc1 = x1 * np.sin(theta) + y1 * np.cos(theta)
        if xc1 ** 2 + yc1 ** 2 > R ** 2:
            break

        xi.append(x1)
        yi.append(y1)
        xc.append(xc1)
        yc.append(yc1)

        x0 = x1
        y0 = y1

    return [f, Ro, Th, xc, yc, xi, yi]

def plot(radius, xc, yc, xi, yi, animate, speed):
    plot_circle([0, 0], radius)

    ax = plt.gca()
    ax.plot(xc[0], yc[0], 'ro')
    if animate:
        line1, = ax.plot([], [], 'b')
        line2, = ax.plot([], [], 'g--')
        ani = animation.FuncAnimation(plt.gcf(), update,
                                      len(xc),
                                      fargs=[xc, yc,
                                             xi, yi,
                                             line1, line2],
                                      interval=speed,
                                      blit=True, repeat=False)
    else:
        ax.plot(xi, yi, 'g--')
        ax.plot(xc, yc, 'b')
    ax.plot(xc[len(xc) - 1], yc[len(yc) - 1], 'r*')
    plt.show()

def run_cli(omega, numSteps, phi, R,
            x0, y0, u0, v0,
            animate, speed):
    [f, Ro, Th, xc, yc, xi, yi] = calculate(omega,
                                            numSteps,
                                            phi, R,
                                            x0, y0,
                                            u0, v0)

    print('f: ', f)
    print('Rossby: ', Ro)
    print('T: ', Th)

    plot(R, xc, yc, xi, yi, animate, speed)

if __name__ == '__main__':
    # Test Case 1
    omega = -0.0000724
    numSteps = 1500
    phi = 30
    R = 100000
    x0 = 100000
    y0 = 0
    u0 = -1
    v0 = 0
    run_cli(omega, numSteps, phi, R, x0, y0, u0, v0,
            animate=False, speed=5)

    # Test Case 2
    omega = -0.0000724
    numSteps = 500
    phi = 30
    R = 100000
    x0 = 0
    y0 = -100000
    u0 = 0
    v0 = 1
    run_cli(omega, numSteps, phi, R, x0, y0, u0, v0,
            animate=True, speed=5)
