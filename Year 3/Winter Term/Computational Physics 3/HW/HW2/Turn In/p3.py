
"""
Computational Physics 3 HW 2
Problem 3
Christopher Morris
"""



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import matplotlib.animation as animation

doanimate = False

class p3:
    def __init__(self):
        #Physical Constants
        self.K = 9.0e9

        #Accept-Reject Uniform Points in Circle
        self.a = 1
        self.b = .25
        self.R = max(self.a,self.b)
        self.N = 1000 #This is number of charges

        self.x = np.array([])
        self.y = np.array([])
        self.q = np.array([])

        #Define Constants
        self.deltarange = .1
        self.numsuccess = 0
        self.maxsuccess = 10000

        self.initializeposition()
        self.initializecharge()

    def getepsilon(self,xi,yi):
        return (xi/self.a)**2 + (yi/self.b)**2

    def initializeposition(self):
        while True:
            n = self.N - self.x.size

            xbox = np.random.uniform(-self.R, self.R, n)
            ybox = np.random.uniform(-self.R, self.R, n)

            self.x = np.concatenate((self.x, xbox[((xbox/self.a)**2 + (ybox/self.b)**2) < 1]), axis = 0)
            self.y = np.concatenate((self.y, ybox[((xbox/self.a)**2 + (ybox/self.b)**2) < 1]), axis = 0)

            if n == 0:
                break

    def initializecharge(self):
        self.q = np.ones(self.x.size) * 1e-6

        #Calculate 2-D potential between source charge at xq, yq between the other charges
    def getPotentialBetween(self,index):
        #get's dr between the source charge and all other charges (includes source charge)
        dr = np.sqrt((self.x-self.x[index])**2+(self.y-self.y[index])**2)

        #Gets phi by taking dr and removing the dr = 0 (which is from source charge to source charge)
        phi = -self.K*self.q[dr>0]*np.log(dr[dr>0])

        return np.sum(phi)

    #Calculates the 2-D Efield at the location of the source charge at xq, yq from the other charges
    def getEfieldatCharge(self,index):
        #get's dr between the source charge and all other charges (includes source charge) and rx,ry components
        dr2 = (self.x-self.x[index])**2+(self.y-self.y[index])**2
        rx = (self.x-self.x[index])
        ry = (self.y-self.y[index])

        #Gets E by taking dr and removing the dr = 0 (which is from source charge to source charge)
        #Since in 2-D; V = -kqln(r)  ==>  E = kq/|r| rhat ==>  E = kqr/|r|^2
        Ex = np.sum(self.K*self.q[dr2>0] * rx[dr2>0] /(dr2[dr2>0]))
        Ey = np.sum(self.K*self.q[dr2>0] * ry[dr2>0] /(dr2[dr2>0]))

        Emag = np.sqrt(Ex**2 + Ey**2)

        return Ex/Emag, Ey/Emag

    def step(self):
            #Get charge (index number) and deltas for x and y
        charge = np.random.randint(0, self.N) #Index for charge, not numcharge because random is exclusive
        delta = np.random.uniform(-self.deltarange, self.deltarange)

        potold = self.getPotentialBetween(charge)
        Ex, Ey = self.getEfieldatCharge(charge)
        #Store original x,y values and then update
        x0 = self.x[charge]
        y0 = self.y[charge]
        self.x[charge] += delta*Ex
        self.y[charge] += delta*Ey
        x1 = self.x[charge]
        y1 = self.y[charge]

        #If charges are moved beyond a circle this places them back
        if ((x1/self.a)**2 + (y1/self.b)**2) >= 1:
            eps0 = self.getepsilon(x0, y0)
            eps1 = self.getepsilon(x1, y1)

            xnew = (1 - eps0) * (x1 - x0)/(eps1 - eps0) + x0
            ynew = (1 - eps0) * (y1 - y0)/(eps1 - eps0) + y0

            self.x[charge] = xnew  #If R != 1 then need to reconfigure this
            self.y[charge] = ynew
            #
            # rmag = np.sqrt(x1**2 + y1**2)
            # self.x[charge] = x1/rmag  #If R != 1 then need to reconfigure this
            # self.y[charge] = y1/rmag

        potnew = self.getPotentialBetween(charge)
        if potnew < potold: #The shift decreased the potential
            self.numsuccess = 0
        else:
            self.numsuccess += 1
            self.x[charge] = x0
            self.y[charge] = y0

        #If failed to decrease the potential after 1000 success tries
        if self.numsuccess >= self.maxsuccess:
            print('done')
            return True #Simulation is done

        return False
#--------------------------------
particles = p3()
#--------------------------------

# set up figure and animation
fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-particles.R, particles.R), ylim=(-particles.R, particles.R))

parts, = ax.plot([], [], 'bo', ms=2)

def init():
    parts.set_data([], [])
    return parts,

def animate(i):
    temp = particles.step()
    parts.set_data(particles.x, particles.y)
    return parts,

if doanimate:
    ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=1, blit=True, init_func=init)
if not doanimate:

    fig, axes = plt.subplots(2,1)
    fig.set_size_inches(10,10)
    axes[0].set_title('initial')
    # axes[0].set_aspect('equal')
    axes[0].autoscale(True)
    axes[0].set_xlim(-1.5,1.5)
    axes[0].set_ylim(-1.5,1.5)
    axes[0].plot(particles.x, particles.y, 'bo', markersize=2)
    while True:
        stop = particles.step()
        if stop: break
    axes[1].set_title('Final')
    # axes[1].set_aspect('equal')
    axes[1].autoscale(True)
    axes[1].set_xlim(-1.5,1.5)
    axes[1].set_ylim(-1.5,1.5)
    axes[1].plot(particles.x, particles.y, 'bo', markersize=2)
    # plt.plot(particles.x, particles.y, 'ko', markersize = 2)

    # plt.savefig('p3.png', dpi = 600)

plt.show()
