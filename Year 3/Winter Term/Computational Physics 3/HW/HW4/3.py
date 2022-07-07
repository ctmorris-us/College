import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


# Lax for 2D Advection

doAnimate = True 

class Problem3():
    def __init__(self):

        # Initialize xmax, ymax, tmax

        self.numxpoints = 201
        self.numypoints = 201
        self.xmin = -10
        self.xmax = 10
        self.ymin = -10
        self.ymax = 10
        self.tmax = 10

        self.t = 0
        self.dx = (self.xmax - self.xmin) / (self.numxpoints - 1)
        self.dy = (self.ymax - self.ymin) / (self.numypoints - 1)
        self.dt = self.dx/np.sqrt(2)

        #The velocity of the waves
        self.vx = .5 * np.sqrt(3)
        self.vy = .5
        self.v = np.array([self.vx, self.vy])

        #Initialize x, y
        self.x = np.linspace(self.xmin, self.xmax, self.numxpoints)
        self.y = np.linspace(self.ymin, self.ymax, self.numypoints)

        self.xx, self.yy = np.meshgrid(self.x, self.y)

        self.u = np.zeros((self.numxpoints, self.numypoints))

        for i in range(self.numxpoints):
            for j in range(self.numypoints):
                rprime = np.sqrt((self.x[i] + 3)**2 + self.y[j]**2)
                if rprime < 2:
                    self.u[i,j] = np.sin(np.pi * rprime)
                else:
                    self.u[i,j] = 0

        self.alpha = self.v * self.dt / self.dx

    def step(self):
        # --------------------- #
        # Transcription of Lax indexing in numpy terms
        # Uj = self.u[1:-1]
        # Uj+1 = self.u[2:]
        # Uj-1 = self.u[0:-2]
        # --------------------- #

        self.u[0, :]  = 0
        self.u[-1, :] = 0
        self.u[:, 0]  = 0
        self.u[:, -1] = 0

        FirstSum  = .25 * (self.u[2:,1:-1] + self.u[0:-2,1:-1] + self.u[1:-1,2:] + self.u[1:-1,0:-2])
        SecondSum = (self.vx * (self.u[2:,1:-1] - self.u[0:-2,1:-1]) + self.vy * (self.u[1:-1,2:] - self.u[1:-1,0:-2]))
        MultiplicativeTerm = (self.dt / (2 * self.dx))
        self.u[1:-1, 1:-1] = FirstSum - MultiplicativeTerm * SecondSum

        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------  part a ------
wave = Problem3()
#-----------

# fig = plt.figure()
# # ax = p3.Axes3D(fig)
# ax = fig.add_subplot(projection = '3d')
#
# parts = [ax.scatter(wave.xx, wave.yy, wave.u)]#ax.plot_wireframe(wave.xx, wave.yy, wave.u)]
# # parts.set_data(wave.xx, wave.yy, wave.u)
#
# ax.set_xlim3d([wave.xmin, wave.xmax])
# ax.set_ylim3d([wave.ymin, wave.ymax])
#
# def animate(i):
#     temp = wave.step()
#     # parts[0].remove()
#     # parts[0] = ax.plot_wireframe(wave.xx, wave.yy, wave.u)
#     parts[0]._offsets3d = (wave.xx, wave.yy, wave.u)
#     return parts
#
# ani = animation.FuncAnimation(fig, animate, frames=600,
#                           interval=1, blit=True)
#
# plt.show()

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
                              interval=100, blit=True)

    plt.show()
else:
    tpoint = [0, 1, 2, 5, 10]
    fig, axes = plt.subplots(ncols = 5, sharex = True, sharey = True, figsize = (10, 8))
    axes = axes.flatten()
    index = 0

    while True:
        temp = wave.step()
        if (wave.t - wave.dt) <= tpoint[index] <= (wave.t + wave.dt): #Have to round because of floating point issues in python
            axes[index].imshow(np.flip(wave.u, axis=0), extent=(wave.xmin, wave.xmax, wave.ymin, wave.ymax),
                                 vmin=0.0, vmax=1.0)
            axes[index].set_title('t = {}'.format(round(wave.t)))
            index += 1
        if index == len(tpoint) or temp:
            break

    fig.subplots_adjust(wspace=.1, hspace=0)
    plt.savefig('p3a.png', dpi = 600)
    plt.show()


#------------ Part b ---------
wave = Problem3()
wave.dt = wave.dt * np.sqrt(2)
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
                              interval=100, blit=True)

    plt.show()

else:
    tpoint = [0, 1, 2, 5, 10]
    fig, axes = plt.subplots(ncols = 5, sharex = True, sharey = True, figsize = (10, 8))
    axes = axes.flatten() #Done to axis the axes by only one index
    index = 0

    while True:
        temp = wave.step()
        if (wave.t - wave.dt) <= tpoint[index] <= (wave.t + wave.dt): #Have to round because of floating point issues in python
            axes[index].imshow(np.flip(wave.u, axis=0), extent=(wave.xmin, wave.xmax, wave.ymin, wave.ymax),
                                 vmin=0.0, vmax=1.0)
            axes[index].set_title('t = {}'.format(round(wave.t)))
            index += 1
        if index == len(tpoint) or temp:
            break

    fig.subplots_adjust(wspace=.1, hspace=0)
    plt.savefig('p3b.png', dpi = 600)
    plt.show()
