import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.linalg import solve
from timeit import default_timer as timer
# --- Physics Constants ---- #
HBar = 1.0 #Planks
M = 1.0
DELX = 2.5 #STD X

I = 1j

# Diffusion Equation Crank-Nikelson

doAnimate = False

class Q3():
    def __init__(self, pbar, numpoints, dt):

        self.numpoints = numpoints
        self.xmin = -40
        self.xmax = 40
        self.tmax = 10

        self.t = dt
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = dt

        self.D = 1
        self.alpha = HBar * self.dt / (2 * M * self.dx**2)

        #Plots as u as a function of x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints, dtype=complex)
        self.xBar = -30.0
        self.pBar = pbar

        self.u = self.getWavePacket(self.xBar, self.pBar)
        self.A = np.zeros((self.numpoints, self.numpoints), dtype =complex)
        self.V = 0 * self.x

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
diffusion = Q3(pbar = 5, numpoints =  1501, dt = .01)
#-----------

if doAnimate:
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

else:
    pbar_tmax_list = [[5, 10], [10, 5], [20, 2.5]] #pbar, tmax pair
    dt_list = [.0005]
    dx_list = [2501]
    good_tlist = []

    for pbartmax_pair in pbar_tmax_list:
        print('\n pbar: {}, tmax: {}'.format(pbartmax_pair[0], pbartmax_pair[1]))

        for dt_index, dt_val in enumerate(dt_list):
            for dx_index, dx_val in enumerate(dx_list):
                print('pbar: {}, tmax: {}'.format(pbartmax_pair[0], pbartmax_pair[1]))
                temp = Q3(pbar = pbartmax_pair[0], numpoints = dx_val, dt = dt_val)

                start_time  = timer()
                while temp.t < pbartmax_pair[1]:
                    temp.step()

                end_time = timer()
                print('\t\t time done')

                elapsed_time = end_time - start_time

                maxindex = np.argmax(np.abs(temp.u)**2)

                if np.abs(20 - temp.x[maxindex]) <= 1:
                    good_tlist.append([pbartmax_pair[0], pbartmax_pair[1], dt_val, dx_val, elapsed_time])

                    print('dt: {}, dx: {}, elapsed_time: {}'.format(dt_val, dx_val, elapsed_time))
