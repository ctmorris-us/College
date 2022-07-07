import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import interpolate

# Wave Equation Lax-Wendroff 1-D
class Problemi():
    def __init__(self):

        # Initialize xmax, tmax
        self.numpoints = 501
        self.xmin = -15
        self.xmax = 15
        self.tmax = 10

        #Pick which boundary condition
            # 1 = Terminating at end
            # 2 = Reflecting
            # 3 = Periodic

        self.BoundaryCondition = 1

        self.t = 0
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = .005

        #The velocity of the waves
        self.v = 1

        #Initialize x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints)

        #-------- Initializing two waves with Amplitude = A, width = w, and centering = xc -----#
        # This first wave travels to the right and the other travels to the left

        firstAmp = 1
        firstWavelength = 2
        self.utemp = firstAmp * np.sin(2 * np.pi * self.x / firstWavelength) #Must match arguments
        self.uderivtemp = firstAmp * 2 * np.pi / firstWavelength * np.cos(2 * np.pi * self.x / firstWavelength)

        lowerboundleft = -12.0
        upperboundleft = -9.8

        lowerboundright = -6.2
        upperboundright = -4.0


        self.u1 = np.where((self.x < -6) & (self.x > -10), self.utemp, 0) #initilizes this wave for x<0 so returs array of style [a b c d 0 0 0 0 0 ]
        self.smoothedge(lowerboundleft, upperboundleft, self.u1)
        self.smoothedge(lowerboundright, upperboundright, self.u1)

        self.r1 = np.where((self.x < -6) & (self.x > -10), self.uderivtemp * self.v, 0)
        self.smoothedge(lowerboundleft, upperboundleft, self.r1)
        self.smoothedge(lowerboundright, upperboundright, self.r1)

        self.s1 = -1 * self.r1 #Moving to the right

        secondAmp = .5
        secondWavelength = 2
        self.utemp = secondAmp * np.sin(2 * np.pi * self.x / secondWavelength) #Must match arguments
        self.uderivtemp = secondAmp * 2 * np.pi / secondWavelength * np.cos(2 * np.pi * self.x / secondWavelength)

        lowerboundleft = 4.0
        upperboundleft = 6.2

        lowerboundright = 9.8
        upperboundright = 12.0

        self.u2 = np.where((self.x < 10) & (self.x > 6), self.utemp, 0) #initilizes this wave for x<0 so returs array of style [a b c d 0 0 0 0 0 ]
        self.smoothedge(lowerboundleft, upperboundleft, self.u2)
        self.smoothedge(lowerboundright, upperboundright, self.u2)

        self.r2 = np.where((self.x < 10) & (self.x > 6), self.uderivtemp * self.v, 0)
        self.smoothedge(lowerboundleft, upperboundleft, self.r2)
        self.smoothedge(lowerboundright, upperboundright, self.r2)

        self.s2 = 1 * self.r2 #Moving to the left

        self.u = self.u1 + self.u2 #Joins [a b c d 0 0 0 0] + [0 0 0 0 e f g h]
        self.r = self.r1 + self.r2
        self.s = self.s1 + self.s2

        # Check to make sure provides the same results as 7.2
        # self.u = self.gaussian(A = 1, xc = -7, w = 1)
        # self.r = self.derivegaussian(A = 1, xc = -7, w = 1) * self.v
        # self.s = -self.r

        self.alpha = self.v * self.dt / self.dx

        self.umax = 0
        self.tmax = 0

    def gaussian(self, A, xc, w): #Returns numpy gaussian
        return A * np.exp(-(self.x - xc)**2/w**2)

    def derivegaussian(self, A, xc, w): #Returns derivative of numpy boundary
        return -2*(self.x - xc)/w**2 * self.gaussian(A, xc, w)

    def smoothedge(self, lowerrange, upperrange, component):
        f = interpolate.interp1d(self.x[(self.x < upperrange) & (self.x > lowerrange)],
                          component[(self.x < upperrange) & (self.x > lowerrange)], kind = 'cubic')
        component[(self.x < upperrange) & (self.x > lowerrange)] = f(self.x[(self.x < upperrange) & (self.x > lowerrange)])

    def step(self):
        # --------------------- #
        # Transcription of Lax-Wendroff indexing in numpy terms
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
        LargeSum_r = .5*(self.s[2:] - self.s[0:-2]) + .5*self.alpha*(self.r[2:] - 2*self.r[1:-1] + self.r[0:-2])
        LargeSum_s = .5*(self.r[2:] - self.r[0:-2]) + .5*self.alpha*(self.s[2:] - 2*self.s[1:-1] + self.s[0:-2])

        self.r[1:-1] = self.r[1:-1] + self.alpha * LargeSum_r
        self.s[1:-1] = self.s[1:-1] + self.alpha * LargeSum_s

        self.u += .5 * self.s * self.dt # update u over half interval

        #Determine max u
        if (np.max(self.u) > np.max(self.umax)) and (self.t < 15):
            self.tmax = self.t
            self.umax = np.copy(self.u)

        self.t += self.dt


        if self.t >= self.tmax:
            return True

#------------
wave = Problemi()
#-----------

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(wave.xmax, wave.xmin), ylim=(-10,10))

parts, = ax.plot([], [], 'b-')
parts.set_data([], [])

def animate(i):
    temp = wave.step()
    parts.set_data(wave.x, wave.u)
    return parts,

ani = animation.FuncAnimation(fig, animate, frames=600,
                          interval=1, blit=True)

plt.show()

#------------- Plot Umax vs t ---------- #

plt.title('U(x,t) for t = {}'.format(wave.tmax))
plt.plot(wave.x, wave.umax)
print('Umax = {}'.format(np.max(wave.umax)))
plt.savefig('Problem1.png', dpi = 600)
plt.show()
