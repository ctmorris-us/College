import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.linalg import solve

# --- Physics Constants ---- #
HBar = 1.0 #Planks
M = 1.0
DELX = 2.5 #STD X

I = 1j

# Shrodinger Equation Crank-Nikelson
# Shows colliding minium wave packets
class Exercise10i():
    def __init__(self):

        self.numpoints = 1001
        self.xmin = -40
        self.xmax = 40
        self.tmax = 10

        self.t = 1
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = .01

        self.D = 1
        self.alpha = HBar * self.dt / (2 * M * self.dx**2)

        #Plots as u as a function of x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints, dtype=complex)
        self.xBar1 = 20.0
        self.pBar1 = -5.0
        self.xBar2 = -20.0
        self.pBar2 = 5.0

        self.u = self.getWavePacket(self.xBar1, self.pBar1) + self.getWavePacket(self.xBar2, self.pBar2)
        self.A = np.zeros((self.numpoints, self.numpoints), dtype =complex)
        self.V = 0 * self.x #Momentum

        for i in range(self.numpoints):
            if i == 0: #Boundary Condition
                self.A[0, 0]  = 1
                self.A[0, 1]  = 0
            elif i == (self.numpoints - 1): #Boundary Condition
                self.A[-1,-1] = 1
                self.A[-1,-2] = 0
            else:
                self.A[i, i-1] = -.5*I*self.alpha
                self.A[i, i]   = 1 + I*self.alpha + .5*I*self.V[i]*self.dt/HBar
                self.A[i, i+1] = -.5*I*self.alpha

    def getWavePacket(self, xb, pb):
        return (2*np.pi*DELX**2)**(-1/4) * np.exp((-(self.x - xb)**2/(4*DELX**2) + I*pb*self.x/HBar), dtype =complex)

    def getFundementalSolution(self):
        multiplicativeTerm = 1 / np.sqrt(4 * np.pi * self.D * self.t, dtype =complex)
        return multiplicativeTerm * np.exp(-(self.x**2 / (4 * self.D * self.t)), dtype =complex)

    def step(self):
        # Uj = self.u[1:-1]
        # Uj+1 = self.u[2:]
        # Uj-1 = self.u[0:-2]
        # Enforce boundary conditions

        #------ This is for Problem 9.4 with a rod held at constant temp 1 at the left end and the right end has the derivative == 0 #
        r = self.x * 0 # Cheap way to get a zero array properly sized
        r[1:-1] = .5*I*self.alpha * self.u[2:] +\
                  (1 - I*self.alpha - .5*I*self.V[1:-1]*self.dt/HBar) * self.u[1:-1] +\
                  .5*I*self.alpha * self.u[0:-2]
        r[0]    = 0 # To force boundary conditions, therefore the left side is held always constant
        r[-1]   = 0

        self.u = solve(self.A, r)

        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------
diffusion = Exercise10i()
#-----------

fig = plt.figure()
ax = fig.add_subplot(111, xlim = (diffusion.xmin, diffusion.xmax), ylim = (0, 1))

parts, = ax.plot([], [], 'b-')
parts.set_data([], [])


def animate(i):
    temp = diffusion.step()
    parts.set_data(np.real(diffusion.x), np.abs(diffusion.u)**2)
    return parts,

ani = animation.FuncAnimation(fig, animate, frames=600,
                          interval=1, blit=True)

plt.show()
