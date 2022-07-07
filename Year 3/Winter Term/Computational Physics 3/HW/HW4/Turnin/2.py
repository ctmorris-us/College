import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Lax for Wave Equation

doAnimate = False #Set True if want to animate

class Problem2():
    def __init__(self):

        # Initialize xmax, tmax
        self.numpoints = 501
        self.xmin = -10
        self.xmax = 10
        self.tmax = 10

        #Pick which boundary condition
            # 1 = Terminating at end
            # 2 = Reflecting
            # 3 = Periodic

        self.BoundaryCondition = 1

        self.t = 0
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = self.dx

        #The velocity of the waves
        self.v = 1

        #Initialize x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints)

        #-------- Initializing two waves with centering = xc -----#
        # This first wave travels to the right and the other travels to the left

        self.xc = 0 #Centering
        self.u = self.sinfunc(self.xc)
        self.r = self.v * self.derivesinfunc(self.xc)
        self.s = 0 * self.r

        self.alpha = self.v * self.dt / self.dx

    def sinfunc(self, xc):
        return np.where(np.abs(self.x - xc) <= 1, np.sin(np.pi * self.x), 0)

    def derivesinfunc(self, xc):
        return np.where(np.abs(self.x - xc) <= 1, np.pi * np.cos(np.pi * self.x), 0)

    def step(self):
        # --------------------- #
        # Transcription of Lax indexing in numpy terms
        # Uj = self.u[1:-1]
        # Uj+1 = self.u[2:]
        # Uj-1 = self.u[0:-2]
        # --------------------- #

        # Enforce boundary conditions
        self.u[0] = 0
        self.u[-1] = 0

        if self.BoundaryCondition == 1: #Terminating
            self.r[0] = 0
            self.r[-1] = 0
            self.s[0] = 0
            self.s[-1] = 0
        elif self.BoundaryCondition == 2: #Reflecting
            self.r[0] = 0
            self.r[-1] = 0
            self.s[0] = self.s[1]
            self.s[-1] = self.s[-2]
        elif self.BoundaryCondition == 3: #Periodic
            self.r[0] = self.r[-2]
            self.r[-1] = self.r[1]
            self.s[0] = self.s[-2]
            self.s[-1] = self.s[1]

        self.u += .5 * self.s * self.dt #Integrate u over half interval

        # -------- Lax-wendroff implementation -------- #
        # LargeSum_r = .5*(self.s[2:] - self.s[0:-2]) + .5*self.alpha*(self.r[2:] - 2*self.r[1:-1] + self.r[0:-2])
        # LargeSum_s = .5*(self.r[2:] - self.r[0:-2]) + .5*self.alpha*(self.s[2:] - 2*self.s[1:-1] + self.s[0:-2])

        # self.r[1:-1] = self.r[1:-1] + self.alpha * LargeSum_r
        # self.s[1:-1] = self.s[1:-1] + self.alpha * LargeSum_s

        #---------- Lax implementation ----------------#
        LargeSum_r = .5 * (self.r[2:] + self.r[0:-2]) + .5 * self.alpha * (self.s[2:] - self.s[0:-2])
        LargeSum_s = .5 * (self.s[2:] + self.s[0:-2]) + .5 * self.alpha * (self.r[2:] - self.r[0:-2])

        self.r[1:-1] = LargeSum_r
        self.s[1:-1] = LargeSum_s

        self.u += .5 * self.s * self.dt # update u over half interval
        self.t += self.dt

        if self.t >= self.tmax:
            return True

    def getRealUSolution(self):
        #Following general d'Almbert's solution
        return .5 * (self.sinfunc(self.xc - self.v * self.t) + self.sinfunc(self.xc + self.v * self.t))

    def getRealrSolution(self):
        return .5 * (self.derivesinfunc(self.xc - self.v * self.t) + self.derivesinfunc(self.xc + self.v * self.t))

#------------
wave = Problem2()
#-----------

if doAnimate:
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

else:
    tpoint = [5]
    fig, axes = plt.subplots(nrows = 2, ncols = 1, figsize = (10, 8))
    index = 0


    while True:
        temp = wave.step()

        if round(wave.t, 2) in tpoint: #Have to round because of floating point issues in python
            axes[0].plot(wave.x, wave.u, 'k-', label = 'Lax')
            axes[0].plot(wave.x, wave.getRealUSolution(), 'r--', label = 'True')
            axes[0].set_title('U Solution; t = {}'.format(round(wave.t)))
            axes[0].legend()

            axes[1].plot(wave.x, wave.r, label = 'Lax')
            axes[1].plot(wave.x, wave.getRealrSolution(), label = 'True')
            axes[1].set_title('r Solution')
            axes[1].legend()

            index += 1

        if temp:
            print('Done')
            break

    plt.legend()
    plt.savefig('p2.png', dpi = 600)
    plt.show()
