import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Wave Equation Lax-Wendroff 
class Exercise7iii():
    def __init__(self):

        # Initialize xmax, tmax
        self.numpoints = 201
        self.xmin = -10
        self.xmax = 10
        self.tmax = 10

        #Pick which boundary condition
            # 1 = Terminating at end
            # 2 = Reflecting

        self.BoundaryCondition = 3

        self.t = 0
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = .01

        #The velocity of the waves
        self.v = 1

        #Initialize x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints)

        #-------- Initializing two waves with Amplitude = A, width = w, and centering = xc -----#
        # This first wave travels to the right and the other travels to the left

        firstxc = -6.5
        self.utemp = self.gaussian(A = 3, xc = firstxc, w = 1.5) #Must match arguments
        self.uderivtemp = self.derivegaussian(A = 3, xc = firstxc, w = 1.5)
        self.u1 = np.where(self.x < 0, self.utemp, 0) #initilizes this wave for x<0 so returs array of style [a b c d 0 0 0 0 0 ]
        self.r1 = np.where(self.x < 0, self.uderivtemp * self.v, 0)
        self.s1 = -1 * self.r1 #Moving to the right

        secondxc = 6.5
        self.utemp = self.gaussian(A = 2, xc = secondxc, w = 2) #Must match arguments
        self.uderivtemp = self.derivegaussian(A = 2, xc = secondxc, w = 2)
        self.u2 = np.where(self.x > 0, self.utemp, 0) #Initializes this wave for x>- so returns array of style [0 0 0 0 0 a b c d]
        self.r2 = np.where(self.x > 0, self.uderivtemp * self.v, 0)
        self.s2 = 1 * self.r2 #Moving to the left

        self.u = self.u1 + self.u2 #Joins [a b c d 0 0 0 0] + [0 0 0 0 e f g h]
        self.r = self.r1 + self.r2
        self.s = self.s1 + self.s2

        # Check to make sure provides the same results as 7.2
        # self.u = self.gaussian(A = 1, xc = -7, w = 1)
        # self.r = self.derivegaussian(A = 1, xc = -7, w = 1) * self.v
        # self.s = -self.r

        self.alpha = self.v * self.dt / self.dx

    def gaussian(self, A, xc, w): #Returns numpy gaussian
        return A * np.exp(-(self.x - xc)**2/w**2)

    def derivegaussian(self, A, xc, w): #Returns derivative of numpy boundary
        return -2*(self.x - xc)/w**2 * self.gaussian(A, xc, w)

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
        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------
wave = Exercise7iii()
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
