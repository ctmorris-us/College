
"""
Computational Physics 3 HW 2
Problem 4a
Christopher Morris
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import matplotlib.animation as animation

doanimate = False

K = 9.0e9

def potential(x, y, q, xq, yq): #Gets potential at location x,y from charges q at locations xq, yq
    global particles
    phi = 0

    q = q.T

    #xq, yq must be 1-D array so that the proper concatenation works
    dx = -xq.T + x
    dy = -yq.T + y

    r = np.concatenate((dx, dy), axis = 1)
    dr = np.linalg.norm(r, axis = 1, keepdims = True)
    phi = np.sum(K*q/dr)

    return phi #- particles.Eexternal[0] * x

def Efield(x, y, q, xq, yq): #Gets E-field at location x,y from charges q at locations xq, yq
    global particles
    E = -1

    #Need to reshape everything from 1-D to D-1 arrays

    q = q.T

    dx = -xq.T + x
    dy = -yq.T + y

    r = np.concatenate((dx, dy), axis = 1)
    dr = np.linalg.norm(r, axis = 1, keepdims = True)
    E = np.sum(K*q*r/(dr**3), axis = 0)
    # E[0] += particles.Eexternal[0]
    return E

PHI_0 = 2e8 # limit the potential
def compute_field_line(xi, yi,		# starting point
                       q, xq, yq,	# charges
                       direction):
    R_MAX = 2 # limit the radius
    DS = 0.01 # target step size
    D_PHI = 1e3 # limit the step

    x = [xi]
    y = [yi]

    # Loop until the line is too far from the origin
    # or too close to a charge.
    while abs(potential(xi, yi, q, xq, yq)) < PHI_0 \
        and xi*xi+yi*yi < R_MAX*R_MAX:

        # Compute the field.
        Ex,Ey = Efield(xi, yi, q, xq, yq)
        E = np.sqrt(Ex*Ex + Ey*Ey)

        # Choose the step length and limit the change in potential.
        ds = DS
        if ds > D_PHI/E: ds = D_PHI/E

        # Take a step in the direction (or opposite) of the field.
        xi += direction*ds*Ex/E
        yi += direction*ds*Ey/E

        x.append(xi)
        y.append(yi)

    return x, y

def plotfullfieldlines(axi,q, xq, yq, ntheta):

    number_of_charges = np.size(q)
    print(number_of_charges)

    for i in range(number_of_charges):
        if i % 100 != 0: continue
        charge = q[0,i] #Have to use two indices because q is a 1xn array
        r = 2 * K * charge / PHI_0

        for n in range(ntheta): #initiates the field lines are ntheta equil positions in a circle
            theta = 2 * np.pi * n / ntheta
            xi = xq[0,i] + r * np.cos(theta)
            yi = yq[0,i] + r * np.sin(theta)

            xfieldline, yfieldline = compute_field_line(xi, yi, q, xq, yq, 1)
            print(i,' +', xfieldline, yfieldline)
            axi.plot(xfieldline, yfieldline, 'k-', linewidth = .5)

            xfieldline, yfieldline = compute_field_line(xi, yi, q, xq, yq, -1)
            print(i,' -', xfieldline, yfieldline)
            axi.plot(xfieldline, yfieldline, 'k-',  linewidth = .5)
        print('Charge {:n}'.format(i))

class p4b:
    def __init__(self):
        #Physical Constants
        self.K = 9.0e9
        self.Eexternal = np.array([1e7,0])

        #Accept-Reject Uniform Points in Circle
        self.a = 1
        self.b = 1
        self.R = max(self.a,self.b)
        self.N = 1000 #This is number of charges

        self.x = np.array([])
        self.y = np.array([])
        self.q = np.array([])

        #Define Constants
        self.deltarange = .1
        self.numsuccess = 0
        self.maxsuccess = 5000
        self.currentindex = 0

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

        return np.sum(phi) - self.Eexternal[0] * self.x[index]


    #Calculates the 2-D Efield at the location of the source charge at xq, yq from the other charges
    def getEfieldatCharge(self,index):
        #get's dr between the source charge and all other charges (includes source charge) and rx,ry components
        dr2 = (self.x-self.x[index])**2+(self.y-self.y[index])**2
        rx = (self.x-self.x[index])
        ry = (self.y-self.y[index])

        #Gets E by taking dr and removing the dr = 0 (which is from source charge to source charge)
        #Since in 2-D; V = -kqln(r)  ==>  E = kq/|r| rhat ==>  E = kqr/|r|^2
        Ex = np.sum(self.K*self.q[dr2>0] * rx[dr2>0] /(dr2[dr2>0])) + self.Eexternal[0]
        Ey = np.sum(self.K*self.q[dr2>0] * ry[dr2>0] /(dr2[dr2>0]))

        Emag = np.sqrt(Ex**2 + Ey**2)

        return Ex/Emag, Ey/Emag

    def step(self):
            #Get charge (index number) and deltas for x and y

        charge = self.currentindex #Index for charge, not numcharge because random is exclusive
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

        self.currentindex += 1
        if self.currentindex == self.N: self.currentindex = 0
        return False
#--------------------------------
particles = p4b()
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
    axes[0].set_aspect('equal')
    axes[0].set_xlim(-1.5,1.5)
    axes[0].set_ylim(-1.5,1.5)
    axes[0].plot(particles.x, particles.y, 'bo', markersize=2)
    while True:
        stop = particles.step()
        if stop: break
    axes[1].set_title('Final')
    axes[1].set_aspect('equal')
    axes[1].set_xlim(-1.5,1.5)
    axes[1].set_ylim(-1.5,1.5)
    axes[1].plot(particles.x, particles.y, 'bo', markersize=3)

    plotfullfieldlines(axes[1],particles.q.reshape(1,particles.N), particles.x.reshape(1,particles.N), particles.y.reshape(1,particles.N), 6) #Plots Fields

    plt.savefig('p4b.png', dpi = 600)

    EfieldOrigin = Efield(0,0,particles.q.reshape(1,particles.N),particles.x.reshape(1,particles.N), particles.y.reshape(1,particles.N))
    ExfieldOrigin = EfieldOrigin[0]
    EyfieldOrigin = EfieldOrigin[1]
    print(ExfieldOrigin)
    # ExfieldOrigin += particles.Eexternal[0]
    print('The Ex field at the origin before adding external: {} and the Ey field:{}'.format(ExfieldOrigin, EyfieldOrigin))
    print('The Ex field at the origin with external: {} and the Ey field:{}'.format(ExfieldOrigin+ particles.Eexternal[0], EyfieldOrigin))

    Potentialatcharges = []
    for i in range(len(particles.q)):
        Potentialatcharges.append(potential(particles.x[i]+.01,particles.y[i]+.01,
                                  particles.q.reshape(1,particles.N),particles.x.reshape(1,particles.N),
                                  particles.y.reshape(1,particles.N)))
    # print(Potentialatcharges)
    # plt.plot(particles.x, particles.y, 'ko', markersize = 2)
plt.show()
#
# q = np.array([[1.e-6, -1.e-6, 1.e-6, -1.e-6, 1.e-6, -1.e-6]])
# xq = np.zeros(np.shape(q))
# yq = np.zeros(np.shape(q))
# for i in range(5):
#     xq[0,i] = np.cos(2*i*np.pi/5)
#     yq[0,i] = np.sin(2*i*np.pi/5)
#
# xq[0,5] = 0
# yq[0,5] = 0
# # Plot Field Lines
# fig, axes = plt.subplots()
#
# print('field lines')
# plotfullfieldlines(axes, q, xq, yq, 16) #Plots Fields
# plt.savefig('Exercise1_a.png', dpi = 600)
# plt.show()
