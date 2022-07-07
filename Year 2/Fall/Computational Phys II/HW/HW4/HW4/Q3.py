# Phys 305 HW 4
# Christopher Morris
# Q3


import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# def initialize(n, seed, v0):
#     mass = np.ones(n)/n
#     pos = np.zeros((n,3))
#     vel = np.zeros((n,3))
#     if n == 2:
#         pos = np.array([[1.0,0,0],[-1.0,0,0]])
#         vel = np.array([[0,v0,0],[0,-v0,0]])
#     return mass,pos,vel

def initialize(n, seed, v0):
    mass = np.ones(n)/n
    mass_for_cm = np.ones((n,1))/n

    pos = np.zeros((n,3))
    vel = np.zeros((n,3))

    q = np.random.random(n)
    r = q**(1./3)
    mu = 2*np.random.random(n) - 1
    theta = np.arccos(mu)
    phi = 2*np.pi*np.random.random(n)
    x = np.sin(theta)*np.cos(phi)
    y = np.sin(theta)*np.sin(phi)
    z = np.cos(theta)

    pos[:,0] = x * r
    pos[:,1] = y * r
    pos[:,2] = z * r

    r = v0
#     mu = 2*np.random.random(n) - 1
#     theta = np.arccos(mu)
#     phi = 2*np.pi*np.random.random(n)
#     vx = r*np.sin(theta)*np.cos(phi)
#     vy = r*np.sin(theta)*np.sin(phi)
#     vz = r*np.cos(theta)

    vx = r * x
    vy = r * y
    vz = r * z

    vel[:,0] = vx
    vel[:,1] = vy
    vel[:,2] = vz

    M = mass.sum()

    rcm = (1/M)*(mass_for_cm*pos).sum(axis = 0)
    vcm = (1/M)*(mass_for_cm*vel).sum(axis = 0)

    pos = pos - rcm
    vel = vel - vcm

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

def output(t, E0, mass, pos, vel, eps2, steps):
    E = energy(mass, pos, vel, eps2)
    print('t =', t, 'dE =', E-E0, 'steps =', steps)

def acceleration(mass, pos, eps2):
    n = len(mass)
    acc = np.zeros((n,3))
    for i in range(n):
        dx   = pos - pos[i]
        dr2  = (dx**2).sum(axis=1) + eps2
        dr2i = 1./dr2
        dr3i = mass*np.sqrt(dr2i)*dr2i
        dx  *= dr3i.reshape(n,1)
        acc[i] = dx.sum(axis=0)
    return acc

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

tiny = 1.e-20
def main(N, seed, eps, dt, t_end, v0, dEtol):

    if eps <= 0.0: eps = tiny

    dt0 = dt		# dt0 is now a time step parameter

    # Initial conditions.

    t = 0.0
    mass,pos,vel = initialize(N, seed, v0)
    steps = 0

    # Initial diagnostics.

    E0 = energy(mass, pos, vel, eps**2)
    print('Initial E =', E0)
    output(t, E0, mass, pos, vel, eps**2, steps)
    a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0], pos[1],
                                  vel[0], vel[1], eps**2)
    print('semimajor axis =', a, ' eccentricity =', e)

    # Run forward to specified time.

    tplot = [0.0]
    dEplot = [0.0]
    hplot = [h]
    smaplot = [a]
    eccplot = [e]
    xplot = [pos[0][0]]
    yplot = [pos[0][1]]
    max_error = 0.0001
    t_increment = 0

    step_count = 0
    while t < t_end-0.5*dt:

        t0 = t
        pos0 = pos.copy()
        vel0 = vel.copy()

        t,pos,vel = step(t, mass, pos, vel, eps**2, dt)
        t,pos,vel = step(t, mass, pos, vel, eps**2, dt)
        E1 = energy(mass, pos, vel, eps**2)


        step_count += 1

        t2,pos2,vel2 = step(t0, mass, pos0, vel0, eps**2, 2*dt)
        E2 = energy(mass, pos2, vel2, eps**2)

        DeltaE = abs(E2 - E1)
        dtnext = dt*(DeltaE/dEtol)**(-1./3)


        if dtnext > 1.5*dt:
            dt = 1.5*dt
        else:
            dt = dtnext

#         r = math.sqrt(((pos[1]-pos[0])**2).sum())

#         E = energy(mass, pos, vel, eps**2)
#         a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0],
#                                       pos[1], vel[0], vel[1], eps**2)
        if t >= t_increment:
            t_increment += .5
            print('Energy error is = {} at t = {}'.format(abs(E1 - E0),t))
            print('dt = {}'.format(dt))

        if abs(E1-E0) >= max_error:
            print('Error greater than max error = {}, error = {}, at t = {}'.format(max_error, abs(E1-E0), t))
            print('dt = {}'.format(dt))
            break

        tplot.append(t)
        dEplot.append(E1-E0)

    print('\n Q3 Answer')
    print('dt = {}'.format(dt))
    print('\nThe number of steps = {}'.format(step_count))

#         hplot.append(h)
#         smaplot.append(a)
#         eccplot.append(e)
#         xplot.append(pos[0][0])
#         yplot.append(pos[0][1])

    # Final diagnostics.

#     output(t, E0, mass, pos, vel, eps**2, steps)

#     plt.figure()

#     if 0:
#         plt.plot(xplot, yplot)
#     else:
#         plt.subplot(2,2,1)
#         plt.plot(tplot, dEplot)
#         plt.xlabel('time')
#         plt.ylabel('energy error')

#         plt.subplot(2,2,2)
#         plt.plot(tplot, hplot)
#         plt.xlabel('time')
#         plt.ylabel('angular momentum')

#         plt.subplot(2,2,3)
#         plt.plot(tplot, smaplot)
#         plt.xlabel('time')
#         plt.ylabel('semimajor axis')

#         plt.subplot(2,2,4)
#         plt.plot(tplot, eccplot)
#         plt.xlabel('time')
#         plt.ylabel('eccentricity')

    # plt.tight_layout()
    # plt.show()

N = 50
seed = 12345
eps = .005
dt = .01
t_end = 20
v0 = .1
dEtol = (10e-8)/2

main(N, seed, eps, dt, t_end, v0, dEtol)
