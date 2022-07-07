import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Lax-Wendroff
# Advection

doAnimate = False

class Problem1():
    def __init__(self):

        self.numpoints = 501
        self.xmin = -10
        self.xmax = 10
        self.tmax = 11

        self.t = 0
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = self.dx
        # dt of .2 is unstable
        # dt of .05 is stable

        self.v = 1

        #Plots as u as a function of x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints)
        self.u = np.exp(-2*(self.x - 2)**2)
        self.uintial = np.exp(-2*(self.x - 2)**2)

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

    def getRealSolution(self):
        return np.exp(-2*((self.x - self.v*self.t)- 2)**2)

#------------
p1a = Problem1()
#-----------

if doAnimate:
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(-10, 10), ylim=(-10,10))

    parts, = ax.plot([], [], 'b-')

    parts.set_data([], [])

    def animate(i):
        temp = p1a.step()
        parts.set_data(p1a.x, p1a.u)
        return parts,

    ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=100, blit=True)

    plt.show()

else:
    tpoint = [1, 2, 5, 10]
    fig, axes = plt.subplots(nrows = 4, ncols = 1, sharex = True, figsize = (10, 8))
    index = 0

    maxdifferencelist = []
    tlist = []

    while True:
        temp = p1a.step()
        maxdifferencelist.append(np.max(np.abs(p1a.u - p1a.getRealSolution())))
        tlist.append(p1a.t)

        if round(p1a.t, 2) in tpoint: #Have to round because of floating point issues in python
            axes[index].plot(p1a.x, p1a.u, 'k-', label = 'Lax')
            axes[index].plot(p1a.x, p1a.getRealSolution(), 'r--', label = 'True')
            axes[index].set_title('t = {}'.format(round(p1a.t)))
            index += 1

        if temp:
            print('Done')
            break
    plt.legend()
    plt.savefig('p1ai.png', dpi = 600)
    plt.show()

    plt.figure(figsize = (10, 8))
    plt.plot(tlist, maxdifferencelist)
    plt.title('Max Difference vs t')
    plt.xlabel('t')
    plt.ylabel('Max Abs Difference')
    plt.savefig('p1aii.png', dpi = 600)
    plt.show()

#------------
p1b = Problem1()
p1b.dt = p1b.dx * .5
#-----------

if doAnimate:
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(-10, 10), ylim=(-10,10))

    parts, = ax.plot([], [], 'b-')
    parts.set_data([], [])

    def animate(i):
        temp = p1b.step()
        parts.set_data(p1b.x, p1b.u)
        return parts,

    ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=100, blit=True)

    plt.show()

else:
    tpoint = [1, 2, 5, 10]
    fig, axes = plt.subplots(nrows = 4, ncols = 1, sharex = True, figsize = (10, 8))
    index = 0

    maxdifferencelist = []
    tlist = []

    while True:
        temp = p1b.step()

        maxdifferencelist.append(np.max(np.abs(p1b.u - p1b.getRealSolution())))
        tlist.append(p1b.t)

        if round(p1b.t, 2) in tpoint: #Have to round because of floating point issues in python
            axes[index].plot(p1b.x, p1b.u, 'k-', label = 'Lax')
            axes[index].plot(p1b.x, p1b.getRealSolution(), 'r--', label = 'True')
            axes[index].set_title('t = {}'.format(round(p1b.t)))
            index += 1

        if temp:
            print('Done')
            break

    plt.legend()
    plt.savefig('p1bi.png', dpi = 600)
    plt.show()

    plt.figure(figsize = (10, 8))
    plt.plot(tlist, maxdifferencelist)
    plt.title('Max Difference vs t')
    plt.xlabel('t')
    plt.ylabel('Max Abs Difference')
    plt.savefig('p1bii.png', dpi = 600)
    plt.show()
