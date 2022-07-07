import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Lax-Wendroff
# Advectionx
class Exercise7i():
    def __init__(self):

        self.numpoints = 201
        self.xmin = -10
        self.xmax = 10
        self.tmax = 10

        self.t = 0
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = .05
        # dt of .2 is unstable
        # dt of .05 is stable

        self.v = 1

        #Plots as u as a function of x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints)
        self.u = np.where( (self.x >= -2) & (self.x <= 0), 5 * np.sin(np.pi * self.x), 0) #t = 0

        self.alpha = self.v * self.dt / self.dx

    def step(self):
        # Uj = self.u[1:-1]
        # Uj+1 = self.u[2:]
        # Uj-1 = self.u[0:-2]
        # Enforce boundary conditions
        self.u[0] = 0
        self.u[-1] = 0

        #Terms 1 - 4 in the Lax Wendroff
        # LargeSum = .5*(self.u[2:] + self.u[1:-1]) - .5*self.alpha*(self.u[2:]-self.u[1:-1]) -\
                   # .5*(self.u[1:-1]+self.u[0:-2]) + .5*self.alpha*(self.u[1:-1]-self.u[0:-2])

        LargeSum = .5*(self.u[2:] - self.u[0:-2]) - .5*self.alpha*(self.u[2:] - 2*self.u[1:-1] + self.u[0:-2])

        self.u[1:-1] = self.u[1:-1] - self.alpha * LargeSum

        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------
wave = Exercise7i()
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
                          interval=100, blit=True)

plt.show()
