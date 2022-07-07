import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.linalg import solve
from scipy import integrate

# --- Physics Constants ---- #
HBar = 1.0 #Planks
M = 1.0
DELX = 2 #STD X

I = 1j

dontAnimateforPlots = True
# Shrodinger Equation Crank-Nikelson
class Exercise10ii():
    def __init__(self, V0):

        self.numpoints = 1501
        self.xmin = -40
        self.xmax = 40
        self.tmax = 15

        self.t = 0
        self.dx = (self.xmax - self.xmin) / (self.numpoints - 1)
        self.dt = .005

        self.D = 1
        self.alpha = HBar * self.dt / (2 * M * self.dx**2)

        #Plots as u as a function of x
        self.x = np.linspace(self.xmin, self.xmax, self.numpoints, dtype=complex)
        self.xBar = -5.0
        self.pBar = 5.0

        self.u = self.getWavePacket(self.xBar, self.pBar)
        self.A = np.zeros((self.numpoints, self.numpoints), dtype =complex)

        #Finite Potenial well
        self.a = 1
        self.V0 = V0

        self.V = np.where((self.x > 0) & (self.x < self.a), self.V0, 0)

        for i in range(self.numpoints):
            if i == 0: #Boundary Condition
                self.A[0, 0]  = 1 #b0
                self.A[0, 1]  = 0 #c0
            elif i == (self.numpoints - 1): #Boundary Condition
                self.A[-1,-1] = 1 #bj-1
                self.A[-1,-2] = 0 #aj-1
            else:
                self.A[i, i-1] = -.5*I*self.alpha
                self.A[i, i]   = 1 + I*self.alpha + .5*I*self.V[i]*self.dt/HBar
                self.A[i, i+1] = -.5*I*self.alpha

    def getWavePacket(self, xb, pb):
        return (2*np.pi*DELX**2)**(-1/4) * np.exp((-(self.x - xb)**2/(4*DELX**2) + I*pb*self.x/HBar), dtype =complex)

    def getFundementalSolution(self):
        multiplicativeTerm = 1 / np.sqrt(4 * np.pi * self.D * self.t, dtype =complex)
        return multiplicativeTerm * np.exp(-(self.x**2 / (4 * self.D * self.t)), dtype =complex)

    def step(self):
        # Uj = self.u[1:-1]
        # Uj+1 = self.u[2:]
        # Uj-1 = self.u[0:-2]
        # Enforce boundary conditions

        #------ This is for Problem 9.4 with a rod held at constant temp 1 at the left end and the right end has the derivative == 0 #
        r = self.x * 0 # Cheap way to get a zero array properly sized
        r[1:-1] = .5*I*self.alpha * self.u[2:] +\
                  (1 - I*self.alpha - .5*I*self.V[1:-1]*self.dt/HBar) * self.u[1:-1] +\
                  .5*I*self.alpha * self.u[0:-2]
        r[0]    = 0 # To force boundary conditions, therefore the left side is held always constant
        r[-1]   = 0

        self.u = solve(self.A, r)

        self.t += self.dt

        if self.t >= self.tmax:
            return True

#------------
diffusion = Exercise10ii(V0=4)
#-----------

if not dontAnimateforPlots: #Just Animate to see
    fig = plt.figure()
    ax = fig.add_subplot(111, xlim = (diffusion.xmin, diffusion.xmax), ylim = (0, 1))

    parts, = ax.plot([], [], 'b-')
    parts.set_data([], [])


    def animate(i):
        temp = diffusion.step()
        parts.set_data(np.real(diffusion.x), np.abs(diffusion.u)**2)
        print(diffusion.t)
        return parts,

    ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=1, blit=True)

    plt.show()

else: #Get answers
    plotstuff = True
    V0_list = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    t_plot = [0, 1, 2, 3, 4]

    T_list = []
    R_list = []

    for V0_val in V0_list:

        print('starting V0: {}'.format(V0_val))

        fig, axes = plt.subplots(len(t_plot), 1, sharex = True, figsize = (10, 10))
        diffusion = Exercise10ii(V0=V0_val)
        plt.suptitle('V0: {}'.format(V0_val))

        while True:
            if plotstuff:
                if V0_val in [8, 10, 12]:
                    for tindex, t in enumerate(t_plot):
                        if (diffusion.t - diffusion.dt) < t < (diffusion.t + diffusion.dt):
                            print(t, diffusion.dt, diffusion.t)
                            axes[tindex].plot(np.real(diffusion.x), np.abs(diffusion.u)**2, 'k-')
                            axes[tindex].set_title('t: {}'.format(t), loc = 'Right')

                    if diffusion.t > 8:
                        print("Saving, V0: {}".format(V0_val))
                        plt.savefig('V0_{}'.format(V0_val), dpi = 600)

            if diffusion.t > 8:
                inftozero = np.where(np.real(diffusion.x) <= 0, np.abs(diffusion.u)**2, 0)
                atoinf = np.where(np.real(diffusion.x) >= diffusion.a, np.abs(diffusion.u)**2, 0)

                T = np.trapz(atoinf, np.real(diffusion.x))
                R = np.trapz(inftozero, np.real(diffusion.x))

                T_list.append(T)
                R_list.append(R)

                print('V0: {}, T:{}, R:{}, R+T:{}'.format(V0_val, T, R, T+R))

                break

            temp = diffusion.step()

    plt.figure()

    E = (5**2)/(2*M)
    V0_array = np.linspace(2, 20, 1000)

    def EgreaterV0(V0): #a = 1
        alpha = np.sqrt(2*M*(E - V0)/HBar**2)
        return 1 / (1 + (V0**2)*(np.sin(alpha*1)**2)/(4*E*(E-V0)))

    def ElessV0(V0): #a = 1
        beta  = np.sqrt(2*M*(V0 - E)/HBar**2)
        return 1 / (1 + (V0**2)*(np.sinh(beta*1)**2)/(4*E*(V0-E)))

    T_calc_list = []
    R_calc_list = []
    E_over_V0_list = []

    for V0_index, V0_val in enumerate(V0_array):
        if V0_val == 0:
            continue
        if E > V0_val:
            E_over_V0_list.append(E/V0_val)
            T_calc_list.append(EgreaterV0(V0_val))
            R_calc_list.append(1 - EgreaterV0(V0_val))
        if E < V0_val:
            E_over_V0_list.append(E/V0_val)
            T_calc_list.append(ElessV0(V0_val))
            R_calc_list.append(1 - ElessV0(V0_val))

    plt.plot(E_over_V0_list, T_calc_list, label = 'T from expression')
    plt.plot(E_over_V0_list, R_calc_list, label = 'R from expression')


    for V0_index, V0_val in enumerate(V0_list):
        plt.plot(E/V0_val, T_list[V0_index], 'ko')
        plt.plot(E/V0_val, R_list[V0_index], 'ro')

    plt.legend()
    plt.xlabel('E/V0')
    plt.savefig('Q3b.png', dpi = 600)
    plt.show()
