import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


# Lax-Wendroff for 2D Wave

doAnimate = True

class Week8i():
    def __init__(self):

        # Initialize xmax, ymax, tmax

        self.numxpoints = 101
        self.numypoints = 101
        self.xmin = -5
        self.xmax = 5
        self.ymin = -5
        self.ymax = 5
        self.tmax = 10

        self.t = 0
        self.dx = (self.xmax - self.xmin) / (self.numxpoints - 1)
        self.dy = (self.ymax - self.ymin) / (self.numypoints - 1)
        self.dt = 1e-2
        #The velocity of the waves
        self.vx = 1
        self.vy = 1
        self.v = np.linalg.norm(np.array([self.vx, self.vy]))

        #Initialize x, y
        self.x = np.linspace(self.xmin, self.xmax, self.numxpoints)
        self.y = np.linspace(self.ymin, self.ymax, self.numypoints)

        #Initialize U
        self.u = np.zeros((self.numxpoints, self.numypoints))

        #Initialize r, l, s where
            # r = v * du/dx
            # l = v * du/dy
            # s = du/dt

        self.r = np.zeros((self.numxpoints, self.numypoints))
        self.l = np.zeros((self.numxpoints, self.numypoints))
        self.s = np.zeros((self.numxpoints, self.numypoints))

        self.WaveSource = True
        if self.WaveSource:
            self.updateWaveSource()

        self.PointSources =  False
        if self.PointSources:
            # Get Index for when 2.5, -2.5
            for index, val in enumerate(self.x):
                if val == 2.5:
                    self.IndexWhenXisPlus2_5 = index
                if val == -2.5:
                    self.IndexWhenXisMinus2_5 = index


            self.updatePointSource()

        self.alphax = self.vx * self.dt / self.dx
        self.alphay = self.vy * self.dt / self.dy

        self.ForceBoundaryDerivesToZero = True #A Small Changes that forces the boundary derivatives to zero to prevent any weird boundary effect
        self.PutAbsorbingBarrier = True #Puts a Barrier That Absorbs the Waves ---> Diffraction

        #Get index for when x = 0
        for index, val in enumerate(self.x):
            if val == 0:
                self.IndexWhenXisZero = index
                break
    def updateWaveSource(self):
        self.u[0, :] = np.sin(np.pi * self.t) #Problem Specific
        self.s[0, :] = np.pi * np.cos(np.pi * self.t)

    def updatePointSource(self):
        self.u[0, self.IndexWhenXisMinus2_5] = 5 * np.sin(np.pi * self.t) + .25
        self.u[0, self.IndexWhenXisPlus2_5]  = 5 * np.sin(np.pi * self.t) + .25
        self.s[0, self.IndexWhenXisPlus2_5]  = 5 * np.pi * np.cos(np.pi * self.t)
        self.s[0, self.IndexWhenXisMinus2_5] = 5 * np.pi * np.cos(np.pi * self.t)

    def step(self):
        # --------------------- #
        # Transcription of Lax indexing in numpy terms
        # Uj = self.u[1:-1]
        # Uj+1 = self.u[2:]
        # Uj-1 = self.u[0:-2]
        # --------------------- #

        #Boundary Conditions
        self.u[0, :], self.u[-1, :], self.u[:, 0], self.u[:, -1] = [0.0, 0.0, 0.0, 0.0]
        self.r[0, :], self.r[-1, :], self.r[:, 0], self.r[:, -1] = [0.0, 0.0, 0.0, 0.0]
        self.l[0, :], self.l[-1, :], self.l[:, 0], self.l[:, -1] = [0.0, 0.0, 0.0, 0.0]
        self.s[0, :], self.s[-1, :], self.s[:, 0], self.s[:, -1] = [0.0, 0.0, 0.0, 0.0]

        # Problem Specific
        # This Case make oscillating Waves Generator at the -x edge
        if self.WaveSource:
            self.updateWaveSource()

        if self.PointSources:
            self.updatePointSource()

        if self.ForceBoundaryDerivesToZero: #A Smoothing Condition that Forces the Boundary Derivatives to Zero On Left-Right Edge (Not where sources are)
            self.r[:,0] = self.r[:,1]
            self.r[:,-1] = self.r[:,-2]

            self.l[:,0] = self.l[:,1]
            self.l[:,-1] = self.l[:,-2]

            self.s[:,0] = self.s[:,1]
            self.s[:,-1] = self.s[:,-2]

        if self.PutAbsorbingBarrier:
            self.u[self.IndexWhenXisZero,:] = np.where((-2 < self.y) &  (self.y < 2), self.u[self.IndexWhenXisZero,:] * 0, self.u[self.IndexWhenXisZero,:])
            self.r[self.IndexWhenXisZero,:] = np.where((-2 < self.y) &  (self.y < 2), self.r[self.IndexWhenXisZero,:] * 0, self.r[self.IndexWhenXisZero,:])
            self.l[self.IndexWhenXisZero,:] = np.where((-2 < self.y) &  (self.y < 2), self.l[self.IndexWhenXisZero,:] * 0, self.l[self.IndexWhenXisZero,:])
            self.s[self.IndexWhenXisZero,:] = np.where((-2 < self.y) &  (self.y < 2), self.s[self.IndexWhenXisZero,:] * 0, self.s[self.IndexWhenXisZero,:])

        self.u[1:-1, 1:-1] += .5 * self.s[1:-1, 1:-1] * self.dt # update u over half interval

        # ------- LAX-WENDROFF -------- #
        RSum = self.alphax * (.5 * (self.s[2:, 1:-1] - self.s[0:-2, 1:-1]) + self.alphax/2 * (self.r[2:, 1:-1] - 2 * self.r[1:-1, 1:-1] + self.r[0:-2, 1:-1]))
        LSum = self.alphay * (.5 * (self.s[1:-1, 2:] - self.s[1:-1, 0:-2]) + self.alphax/2 * (self.l[1:-1, 2:] - 2 * self.l[1:-1, 1:-1] + self.l[1:-1, 0:-2]))

        SSum = self.alphax/2 * ((self.r[2:, 1:-1] - self.r[0:-2, 1:-1]) + self.alphax * (self.s[2:, 1:-1] - 2 * self.s[1:-1, 1:-1] + self.s[0:-2, 1:-1])) +\
               self.alphay/2 * ((self.l[1:-1, 2:] - self.l[1:-1, 0:-2]) + self.alphay * (self.s[1:-1, 2:] - 2 * self.s[1:-1, 1:-1] + self.s[1:-1, 0:-2]))

        self.r[1:-1, 1:-1] = self.r[1:-1, 1:-1] + RSum
        self.l[1:-1, 1:-1] = self.l[1:-1, 1:-1] + LSum
        self.s[1:-1, 1:-1] = self.s[1:-1, 1:-1] + SSum

        self.u[1:-1, 1:-1] += .5 * self.s[1:-1, 1:-1] * self.dt # update u over half interval

        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------  part a ------
wave = Week8i()
#-----------

if doAnimate:
    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False,
                         xlim=(wave.xmin, wave.xmax), ylim=(wave.ymin, wave.ymax))

    cax = [ax.imshow(np.flip(wave.u, axis=0),
                         extent=(wave.xmin, wave.xmax, wave.ymin, wave.ymax),
                         vmin=0.0, vmax=1.0)]

    # parts, = ax.plot([], [], 'b-')
    # parts.set_data([], [])

    def animate(i):
        temp = wave.step()
        cax[0].set_data(np.flip(wave.u, axis=0))
        return cax

    ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=1, blit=True)

    plt.show()
