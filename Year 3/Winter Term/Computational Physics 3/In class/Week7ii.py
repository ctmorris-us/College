import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Lax-Wendroff
class Exercise7ii():
    def __init__(self):

        self.numpoints = 201
        self.xmin = -10
        self.xmax = 10
        self.tmax = 10

        self.t = 0
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = .008

        self.v = 1

        #Plots as u as a function of x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints)
        self.u = np.exp(-(self.x - 7)**2) #t = 0

        self.r = self.v * -2 * (self.x - 7) * np.exp(-(self.x - 7)**2)
        self.s = 1 * self.r

        self.alpha = self.v * self.dt / self.dx

    def step(self):
        # Uj = self.u[1:-1]
        # Uj+1 = self.u[2:]
        # Uj-1 = self.u[0:-2]
        # Enforce boundary conditions
        self.u[0] = 0
        self.u[-1] = 0
        self.r[0] = 0
        self.r[-1] = 0
        self.s[0] = 0
        self.s[-1] = 0

        self.u += .5 * self.s * self.dt

        LargeSum_r = .5*(self.s[2:] - self.s[0:-2]) + .5*self.alpha*(self.r[2:] - 2*self.r[1:-1] + self.r[0:-2])
        LargeSum_s = .5*(self.r[2:] - self.r[0:-2]) + .5*self.alpha*(self.s[2:] - 2*self.s[1:-1] + self.s[0:-2])

        self.r[1:-1] = self.r[1:-1] + self.alpha * LargeSum_r
        self.s[1:-1] = self.s[1:-1] + self.alpha * LargeSum_s

        self.u += .5 * self.s * self.dt
        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------
wave = Exercise7ii()
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
                          interval=5, blit=True)

plt.show()
