import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Diffusion Equation FTCS
class Exercise9i():
    def __init__(self):

        self.numpoints = 201
        self.xmin = -10
        self.xmax = 10
        self.tmax = 10

        self.t = 1
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = .0051

        self.D = 1
        self.alpha = self.D * self.dt / self.dx**2

        #Plots as u as a function of x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints)
        self.u = 10 * self.getFundementalSolution()

        self.uBoundMin = 0
        self.uBoundMax = 0

    def getFundementalSolution(self):
        multiplicativeTerm = 1 / np.sqrt(4 * np.pi * self.D * self.t)
        return multiplicativeTerm * np.exp(-(self.x**2 / (4 * self.D * self.t)))

    def step(self):
        # Uj = self.u[1:-1]
        # Uj+1 = self.u[2:]
        # Uj-1 = self.u[0:-2]
        # Enforce boundary conditions

        self.u[0]  = self.uBoundMin
        self.u[-1] = self.uBoundMax

        LargeSum_u = self.alpha * (self.u[2:] - 2*self.u[1:-1] + self.u[0:-2])

        self.u[1:-1] = self.u[1:-1] + LargeSum_u

        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------
diffusion = Exercise9i()
#-----------

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-10, 10), ylim=(-10,10))

parts, = ax.plot([], [], 'b-')
parts.set_data([], [])

def animate(i):
    temp = diffusion.step()
    parts.set_data(diffusion.x, diffusion.u)
    return parts,

ani = animation.FuncAnimation(fig, animate, frames=600,
                          interval=1, blit=True)

plt.show()
