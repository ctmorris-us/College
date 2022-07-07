import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.linalg import solve


# Diffusion Equation Crank-Nikelson
class Exercise9iii():
    def __init__(self):

        self.numpoints = 1001
        self.xmin = -10
        self.xmax = 10
        self.tmax = 10

        self.t = 1
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = .1

        self.D = 1
        self.alpha = self.D * self.dt / self.dx**2

        #Plots as u as a function of x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints)
        self.u = 0 * self.x
        self.A = np.zeros((self.numpoints, self.numpoints))

        for i in range(self.numpoints):
            if i == 0: #Boundary Condition
                self.A[0, 0]  = 1
                self.A[0, 1]  = 0
            elif i == (self.numpoints - 1): #Boundary Condition
                self.A[-1,-1] = -1
                self.A[-1,-2] = 1
            else:
                self.A[i, i-1] = -.5*self.alpha
                self.A[i, i]   = 1 + self.alpha
                self.A[i, i+1] = -.5*self.alpha

    def getFundementalSolution(self):
        multiplicativeTerm = 1 / np.sqrt(4 * np.pi * self.D * self.t)
        return multiplicativeTerm * np.exp(-(self.x**2 / (4 * self.D * self.t)))

    def step(self):
        # Uj = self.u[1:-1]
        # Uj+1 = self.u[2:]
        # Uj-1 = self.u[0:-2]
        # Enforce boundary conditions

        #------ This is for Problem 9.4 with a rod held at constant temp 1 at the left end and the right end has the derivative == 0 #
        r = self.x * 0 # Cheap way to get a zero array properly sized
        r[1:-1] = .5 * self.alpha * self.u[2:] + (1 - self.alpha) * self.u[1:-1] + .5 * self.alpha * self.u[0:-2]
        r[0]    = 1 # To force boundary conditions, therefore the left side is held always constant
        r[-1]   = 0

        self.u = solve(self.A, r)

        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------
diffusion = Exercise9iii()
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
