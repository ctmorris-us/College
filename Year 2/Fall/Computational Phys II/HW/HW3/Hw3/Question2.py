import numpy as np
import math
import matplotlib.pyplot as plt
import sys

## HW 3
# Phys 305
# Christopher Morris


tiny = 1.e-20

delta = 0.0
alpha = -2.0
beta = 1.0

def deriv2(x, y):
    return -delta*y[1] - alpha*y[0] - beta*y[0]**3

def phi(x, y):
    return 0.5*alpha*y[0]**2 + 0.25*beta*y[0]**4

def energy(x, y):
    return 0.5*y[1]**2 + phi(x, y)

def f(x, y):
    return np.array([y[1], deriv2(x, y)])

def kick_drift_step(f, x, y, dx):

    s = 4
    p = 2**(1/3)
    q = 1 - p
    r = 4 - 2*p

    c = [1/r, q/r, q/r, 1/r]
    d = [0, 2/r, -2*p/r, 2/r]

    a = f(x, y)[1]
    v = y[1]
    y = y[0]

    for i in range(len(c)):

        v += d[i]*a*dx
        y += c[i]*v*dx

    y = np.array([y, v])
    x += dx

    return x, y

def initialize_hw(rj, mj): #sun, earth, jupiter
    mass = np.array([1, 3e-6, mj])
    pos = np.array([[0,0,0], [1,0,0], [0,rj,0]])

    ve = np.sqrt((mass[0] + mass[1])/1)
    vj = np.sqrt((mass[0] + mass[2])/rj)

    vel = np.array([[0,0,0], [0,ve,0], [-vj,0,0]])

    return mass,pos,vel


def initialize(n, seed, v0):
    mass = np.ones(n)/n
    pos = np.zeros((n,3))
    vel = np.zeros((n,3))
    if n == 2:
        pos = np.array([[1.0,0,0],[-1.0,0,0]])
        vel = np.array([[0,v0,0],[0,-v0,0]])
    return mass,pos,vel

def potential_energy(mass, pos, eps2):
    n = len(mass)
    pot = 0.0
    dx = np.zeros((n,3))
    for i in range(n):
        dx[i+1:] = pos[i+1:] - pos[i]
        dr2 = (dx[i+1:]**2).sum(axis=1) + eps2
        pot -= mass[i]*(mass[i+1:]/np.sqrt(dr2)).sum()
    return pot

def alt_potential_energy(mass, pos, eps2):
    n = len(mass)
    pot = 0.0
    for i in range(n):
        for j in range(i+1,n):
            dr2 = eps2
            for k in range(3):
                dr2 += (pos[i,k]-pos[j,k])**2
            pot -= mass[i]*mass[j]/math.sqrt(dr2)
    return pot

def kinetic_energy(mass, vel):
    return 0.5*(mass*(vel**2).sum(axis=1)).sum()

def alt_kinetic_energy(mass, vel):
    n = len(mass)
    kin = 0.0
    for i in range(n):
        vi2 = 0.0
        for k in range(3):
            vi2 += vel[i,k]**2
        kin += 0.5*mass[i]*vi2
    return kin

def energy(mass, pos, vel, eps2):
    T = kinetic_energy(mass, vel)
    U = potential_energy(mass, pos, eps2)
    return T+U

def output(t, E0, mass, pos, vel, eps2):
    E = energy(mass, pos, vel, eps2)
    print('t =', t, 'dE =', E-E0)

def acceleration(mass, pos, eps2):
    n = len(mass)
    acc = np.zeros((n,3))
    for i in range(n):
        dx   = pos - pos[i]
        dr2  = (dx**2.0).sum(axis=1) + eps2
        dr2i = 1./dr2
        dr3i = mass*np.sqrt(dr2i)*dr2i
        dx  *= dr3i.reshape(n,1)
        acc[i] = dx.sum(axis=0)
    return acc*1.0

def alt_acceleration(mass, pos, eps2):
    n = len(mass)
    acc = np.zeros((n,3))
    for i in range(n):
        for j in range(i+1,n):
            dr2 = eps2
            for k in range(3):
                dr2 += (pos[j,k]-pos[i,k])**2
            dr2i = 1./dr2
            dr3i = dr2i*math.sqrt(dr2i)
            for k in range(3):
                dxij = (pos[j,k]-pos[i,k])*dr3i
                acc[i,k] += mass[j]*dxij
                acc[j,k] -= mass[i]*dxij
    return acc

def step(t, mass, pos, vel, eps2, dt):

    # Second-order predictor-corrector.

    acc = acceleration(mass, pos, eps2)
    pos += dt*(vel+0.5*dt*acc)
    anew = acceleration(mass, pos, eps2)
    vel += 0.5*dt*(acc+anew)

    return t+dt,pos,vel

def kdk_step(t, mass, pos, vel, eps2, dt):
    vel += 0.5*acceleration(mass, pos, eps2)*dt
    pos += vel*dt
    vel += 0.5*acceleration(mass, pos, eps2)*dt
    t += dt
    return t, pos, vel

def orbital_elements(m1, m2, x1, x2, v1, v2, eps2):
    M = m1+m2
    x = x2-x1
    v = v2-v1
    r2 = (x**2).sum() + eps2
    v2 = (v**2).sum()
    E = 0.5*v2 - M/math.sqrt(r2)
    sma = -0.5*M/E
    h2 = ((np.cross(x,v))**2).sum()
    ecc = (1 + 2*E*h2/M**2)**0.5

    return sma, ecc, E, h2**0.5


def main(N, seed, eps, dt, t_end, v0):
    if eps <= 0.0: eps = tiny

    # Initial conditions.

    t = 0.0
#     mass,pos,vel = initialize(N, seed, v0)

    Mj = 0.1
    Rj = 3.0

    mass,pos,vel = initialize_hw(Rj, Mj)

    # Initial diagnostics.

    E0 = energy(mass, pos, vel, eps**2)
#     print('Initial E =', E0)
#     output(t, E0, mass, pos, vel, eps**2)
    a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0], pos[1],
                                  vel[0], vel[1], eps**2)
#     print('semimajor axis =', a, ' eccentricity =', e)

    # Run forward to specified time.

    tplot = []
    dEplot = []
    hplot = []
    smaplot = []
    eccplot = []

    x1plot = []
    y1plot = []

    x2plot = []
    y2plot = []

    x3plot = []
    y3plot = []

    emax = 0

    rp = 1.e6
    rpp = rp+1.
    posp = np.zeros(3)
    pospp = np.ones(3)
    while t < t_end-0.5*dt:
        t,pos,vel = step(t, mass, pos, vel, eps**2, dt)
        E = energy(mass, pos, vel, eps**2)
        a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0],
                                      pos[1], vel[0], vel[1], eps**2)
        r = (((pos[0]-pos[1])**2).sum())**0.5

        if e > emax:
            emax = e

#         if r < rp and rp >= rpp:
#             v1 = (rp-rpp)/dt
#             v2 = (r-rp)/dt
#             tmax = t - 1.5*dt + dt*(-v1)/(v2-v1)
#             xmax = 0.5*(pospp+posp) + 0.5*(pos[0]-pos[1]-pospp)*(-v1)/(v2-v1)
#             print('maximum:  t =', tmax,
#                   'r =', (xmax**2).sum()**0.5,
#                   'angle =', math.atan2(xmax[1], xmax[0]) )

        if a < 0:
            print('unbound orbit')
            break

        tplot.append(t)
        dEplot.append(E-E0)
        hplot.append(h)
        smaplot.append(a)
        eccplot.append(e)

        x1plot.append(pos[0][0])
        y1plot.append(pos[0][1])

        x2plot.append(pos[1][0])
        y2plot.append(pos[1][1])

        x3plot.append(pos[2][0])
        y3plot.append(pos[2][1])

        rpp = rp
        rp = r
        pospp = posp.copy()
        posp = pos[0]-pos[1]

    # Final diagnostics.

    output(t, E0, mass, pos, vel, eps**2)

    plt.figure()

    if 1:
        plt.plot(x1plot, y1plot)
        plt.plot(x2plot, y2plot)
        plt.plot(x3plot, y3plot)
        plt.title('Trajectory')
        plt.xlabel('X')
        plt.ylabel('Y')

    plt.tight_layout()
    plt.show()

N = 3
seed = 42
eps = 0
dt = .1
t_end = 100
v0 = .25


main(N, seed, eps, dt, t_end, v0)

def main(N, seed, eps, dt, t_end, v0):
    if eps <= 0.0: eps = tiny
    Mj_Rj_list = [(0.01,3.0), (0.02, 2.1), (0.03,2.0)]

    for Mj, Rj in Mj_Rj_list:
        # Initial conditions.

        t = 0.0
    #     mass,pos,vel = initialize(N, seed, v0)


        mass,pos,vel = initialize_hw(Rj, Mj)

        # Initial diagnostics.

        E0 = energy(mass, pos, vel, eps**2)
        print('Initial E =', E0)
        output(t, E0, mass, pos, vel, eps**2)
        a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0], pos[1],
                                      vel[0], vel[1], eps**2)
        print('semimajor axis =', a, ' eccentricity =', e)

        # Run forward to specified time.

        tplot = []
        dEplot = []
        hplot = []
        smaplot = []
        eccplot = []

        x1plot = []
        y1plot = []

        x2plot = []
        y2plot = []

        x3plot = []
        y3plot = []

        emax = 0

        rp = 1.e6
        rpp = rp+1.
        posp = np.zeros(3)
        pospp = np.ones(3)
        while t < t_end-0.5*dt:
            t,pos,vel = step(t, mass, pos, vel, eps**2, dt)
            E = energy(mass, pos, vel, eps**2)
            a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0],
                                          pos[1], vel[0], vel[1], eps**2)
            r = (((pos[0]-pos[1])**2).sum())**0.5

            if e > emax:
                emax = e

            if r < rp and rp >= rpp:
                v1 = (rp-rpp)/dt
                v2 = (r-rp)/dt
                tmax = t - 1.5*dt + dt*(-v1)/(v2-v1)
                xmax = 0.5*(pospp+posp) + 0.5*(pos[0]-pos[1]-pospp)*(-v1)/(v2-v1)
    #             print('maximum:  t =', tmax,
    #                   'r =', (xmax**2).sum()**0.5,
    #                   'angle =', math.atan2(xmax[1], xmax[0]) )

            if a < 0:
                print('unbound orbit')
                break

            tplot.append(t)
            dEplot.append(E-E0)
            hplot.append(h)
            smaplot.append(a)
            eccplot.append(e)

            x1plot.append(pos[0][0])
            y1plot.append(pos[0][1])

            x2plot.append(pos[1][0])
            y2plot.append(pos[1][1])

            x3plot.append(pos[2][0])
            y3plot.append(pos[2][1])

            rpp = rp
            rp = r
            pospp = posp.copy()
            posp = pos[0]-pos[1]

        # Final diagnostics.

        output(t, E0, mass, pos, vel, eps**2)

        plt.figure(figsize = (10, 6))

        if 0:
            plt.plot(x1plot, y1plot)
            plt.plot(x2plot, y2plot)
            plt.plot(x3plot, y3plot)
        elif 1:
            plt.subplot(2,1,1)
            plt.plot(tplot, eccplot)
            plt.title('Rj: {}, Mj:{}'.format(Rj,Mj))
            plt.xlabel('Time')
            plt.ylabel('Eccentricity')

            plt.subplot(2,1,2)
            plt.plot(tplot, smaplot)
            plt.title('Rj: {}, Mj:{}'.format(Rj,Mj))
            plt.xlabel('Time')
            plt.ylabel('Semi-Major Axis')

            print('Eccentricity max for Rj: {}, Mj:{} is = {}'.format(Rj, Mj, emax))

        plt.tight_layout()
        plt.show()

N = 3
seed = 42
eps = 0
dt = .01
t_end = 100
v0 = .25


main(N, seed, eps, dt, t_end, v0)

def main(N, seed, eps, dt, t_end, v0):
    if eps <= 0.0: eps = tiny

    Mj_list = np.arange(.01, .21, .01)
    Rj_list = np.arange(1.2, 2.5, .1)
#     Mj_Rj_list = [(0.01,3.0), (0.02, 2.1), (0.03,2.0)]
    plt.figure(figsize = (10, 10))

    for Mj in Mj_list:
        for Rj in Rj_list:
            # Initial conditions.
            stability = True
            t = 0.0
        #     mass,pos,vel = initialize(N, seed, v0)


            mass,pos,vel = initialize_hw(Rj, Mj)

            # Initial diagnostics.

            E0 = energy(mass, pos, vel, eps**2)
            print('Initial E =', E0)
            output(t, E0, mass, pos, vel, eps**2)
            a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0], pos[1],
                                          vel[0], vel[1], eps**2)
            print('semimajor axis =', a, ' eccentricity =', e)

            # Run forward to specified time.

            emax = 0

            rp = 1.e6
            rpp = rp+1.
            posp = np.zeros(3)
            pospp = np.ones(3)
            while t < t_end-0.5*dt:
                t,pos,vel = step(t, mass, pos, vel, eps**2, dt)
                E = energy(mass, pos, vel, eps**2)
                a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0],
                                              pos[1], vel[0], vel[1], eps**2)
                r = (((pos[0]-pos[1])**2).sum())**0.5

                if e > emax:
                    emax = e

                if r < rp and rp >= rpp:
                    v1 = (rp-rpp)/dt
                    v2 = (r-rp)/dt
                    tmax = t - 1.5*dt + dt*(-v1)/(v2-v1)
                    xmax = 0.5*(pospp+posp) + 0.5*(pos[0]-pos[1]-pospp)*(-v1)/(v2-v1)
        #             print('maximum:  t =', tmax,
        #                   'r =', (xmax**2).sum()**0.5,
        #                   'angle =', math.atan2(xmax[1], xmax[0]) )

                if a < 0:
                    stability = False
                    print('unbound orbit')
                    break

                rpp = rp
                rp = r
                pospp = posp.copy()
                posp = pos[0]-pos[1]

            # Final diagnostics.

            output(t, E0, mass, pos, vel, eps**2)

            if emax  > .5:
                stability = False
            if stability == True:
                plt.plot(Mj, Rj, 'go', label = 'Stable')
            else:
                plt.plot(Mj, Rj, 'ro', label = 'Unstable')


    plt.tight_layout()
    plt.legend()
    plt.xlabel('Mj')
    plt.ylabel('Rj')
    plt.title('Stability of Orbits')
    plt.show()

N = 3
seed = 42
eps = 0
dt = .01
t_end = 1000
v0 = .25


main(N, seed, eps, dt, t_end, v0)
