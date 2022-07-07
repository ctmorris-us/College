
"""
Computational Physics 3 HW 2
Problem 2
Christopher Morris

The code is written as a class in order to be able to animate for learning purposes
Unfortunately, the animation function does not seem to be working for this particular problem, however
p3.py, p4a.py, and p4b.py all are able to animate.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import matplotlib.animation as animation

seed = 42
np.random.seed(seed)

doanimate = True

class p2:
    def __init__(self):
        self.xa = 0
        self.xb = 1
        self.ya = 1
        self.yb = 1

        self.N = 21
        self.x = np.linspace(self.xa, self.xb, self.N+1)
        self.dx = self.x[1:] - self.x[:-1]

        #self.y = np.linspace(xa, xb, N+1)
        self.y = np.zeros((self.N + 1))
        self.y[0] = self.ya
        self.y[self.N] = self.yb
        self.y[1:self.N] = np.random.uniform(0,1,self.N-1)

        self.C = 1

        self.deltay = .01
        self.noreduce = 0
        self.tcurrent = self.transit()
        self.trials = 0
        self.maxsuccess = 5000
        self.docheck = False

    def refr(self, x, y): # return the refractive index at (x, y)
        return 1 + .5*y**4


    def transit(self):
        dy = self.y[1:] - self.y[:-1]
        xx = .5*(self.x[1:] + self.x[:-1])
        yy = .5*(self.y[1:] + self.y[:-1])
        return np.sum(self.refr(xx, yy) * np.sqrt(self.dx**2 + dy**2)) / self.C #Doesn't consider the last element



    def step(self):
        self.trials += 1
        i = np.random.randint(1, self.N)
        y0 = self.y[i]
        self.y[i] += np.random.uniform(-self.deltay, self.deltay)
        t = self.transit()

        if t < self.tcurrent:
            self.noreduce = 0
            self.tcurrent = t
        else:
            self.y[i] = y0 #Keep the original y
            self.noreduce += 1

        if self.noreduce >= self.maxsuccess:
            print('done')
            return True #After 1000 attempts to reduce t have failed
        return False

#-------------------------
variation = p2()
#------------------------

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False,
                     xlim=(0,1), ylim=(-2,2))

parts, = ax.plot([], [], 'b-')

def init():
    parts.set_data([], [])
    return parts,

def animate(i):
    temp = variation.step()
    parts.set_data(variation.x, variation.y)
    return parts,

if doanimate:
    ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=1, blit=True, init_func=init)

    plt.show()

if not doanimate:

    fig, axes = plt.subplots(2,1)
    axes[0].set_title('Initial')
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('y')
    axes[0].plot(variation.x, variation.y, 'b-')

    # start = timer()
    while True:
        stop = variation.step()
        if stop: break
    # stop = timer()
    axes[1].set_title('Final')
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('y')
    axes[1].plot(variation.x, variation.y, 'b-')
    # plt.plot(particles.x, particles.y, 'ko', markersize = 2)
    # print('Time elasped', (stop - start))
    print('Trials:', variation.trials, 'Tmin:', variation.tcurrent)

    ymin = 100
    xmin = 0
    for i,xi in enumerate(variation.x):
        if variation.y[i] <= ymin:
            xmin = variation.x[i]
            ymin = variation.y[i]

    print('Min x {:.2f}, and Min y {:.2f}'.format(xmin, ymin))
    plt.plot(xmin, ymin, 'ro', label = 'min')
    # plt.savefig('p2.png', dpi = 600)

plt.show()
