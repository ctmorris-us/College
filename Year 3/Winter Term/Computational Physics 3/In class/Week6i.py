import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Exercise6i():
    def __init__(self):

        self.numpoints = 201
        self.xmin = -10
        self.xmax = 10
        self.tmax = 10

        self.t = 0
        self.dx = .1
        self.dt = .1

        self.v = 1

        self.x = np.linspace(self.xmin, self.xmax, self.numpoints)
        self.u = np.where( (self.x >= -2) & (self.x <= 0), np.sin(np.pi * self.x), 0) #t = 0

        self.alpha = self.v * self.dt / (2 * self.dx)

    def step(self):

        # Enforce boundary conditions
        self.u[0] = 0
        self.u[-1] = 0
        self.u[1:-1] = self.u[1:-1] - self.alpha * (self.u[2:] - self.u[0:-2])

        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------
wave = Exercise6i()
#-----------

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-10, 10), ylim=(-10,10))

parts, = ax.plot([], [], 'b-')
parts.set_data([], [])

def animate(i):
    temp = wave.step()
    parts.set_data(wave.x, wave.u)
    return parts,

ani = animation.FuncAnimation(fig, animate, frames=600,
                          interval=1, blit=True)

plt.show()
