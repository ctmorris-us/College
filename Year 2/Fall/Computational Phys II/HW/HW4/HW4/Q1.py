# Phys 305 HW 4
# Christopher Morris
# Q1



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

huge = 1.e20

def acceleration2(mass, pos, vel, eps2):
    n = len(mass)
    acc = np.zeros((n,3))
    tau = huge
    for i in range(n):
        dx = pos - pos[i]
        dr2 = (dx**2).sum(axis=1) + eps2
        dv = vel - vel[i]
        vdotx = np.abs((dx*dv).sum(axis=1)) + tiny
        dr3 = dr2*np.sqrt(dr2)
        dr3i = mass/dr3
        dx *= dr3i.reshape(n,1)
        acc[i] = dx.sum(axis=0)

        dr3[i] = huge
        tau2 = dr2/vdotx
        tau3 = dr3/(mass+mass[i])
        tau2[i] = huge
        tau3[i] = huge
        tau = min(tau, tau2.min(), math.sqrt(tau3.min()))

    return acc, tau

def alt_acceleration2(mass, pos, vel, eps2):
    n = len(mass)
    acc = np.zeros((n,3))
    tau = huge
    for i in range(n):
        for j in range(i+1,n):
            dr2 = eps2
            for k in range(3):
                dr2 += (pos[j,k]-pos[i,k])**2

            rij = math.sqrt(dr2)
            dvr = 0.
            for k in range(3):
                dvr += (pos[j,k]-pos[i,k])*(vel[j,k]-vel[i,k])
            vrij = dvr/rij

            dr2i = 1./dr2
            dr3i = dr2i*math.sqrt(dr2i)
            for k in range(3):
                dxij = (pos[j,k]-pos[i,k])*dr3i
                acc[i,k] += mass[j]*dxij
                acc[j,k] -= mass[i]*dxij

            da2 = 0.
            for k in range(3):
                da2 += (acc[j,k]-acc[i,k])**2
            aij = math.sqrt(da2)

            tau2ij = huge
            if vrij > 0: tau2ij = rij/vrij
            tau3ij = math.sqrt(rij/aij)

            tau = min(tau, tau2ij, tau3ij)

    return acc,tau

acc2 = acceleration2

def step(t, mass, pos, vel, eps2, dt):

    # Second-order predictor-corrector.

    acc,tau = acc2(mass, pos, vel, eps2)
    pos += dt*(vel+0.5*dt*acc)
    anew,tau = acc2(mass, pos, vel, eps2)
    vel += 0.5*dt*(acc+anew)
    return t+dt,pos,vel,tau

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

### Q1A

tiny = 1.e-20
def main(N, seed, eps, dt, t_end, v0, eta):
    if eps <= 0.0: eps = tiny
    dt0 = dt

    # Initial conditions.

    t = 0.0
    mass,pos,vel = initialize(N, seed, v0)
    steps = 0
    acc,tau = acc2(mass, pos, vel, eps**2)
    dt = dt0*tau

    tau0 = tau

    # Initial diagnostics.

    E0 = energy(mass, pos, vel, eps**2)
    print('Initial E =', E0)
    output(t, E0, mass, pos, vel, eps**2, steps)
    a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0], pos[1],
                                  vel[0], vel[1], eps**2)
    print('semimajor axis =', a, ' eccentricity =', e)

    # Run forward to specified time.

    tplot = []
    dEplot = []
    hplot = []
    smaplot = []
    eccplot = []

    tot_E_plot = []
    tot_T_plot = []
    tot_U_plot = []
    virial_radius_plot = []
    tau_variation_plot = []

    max_error = .0001
    t_increment = 0


    while t < t_end-0.5*dt:
        t,pos,vel,tau = step(t, mass, pos, vel, eps**2, dt)
        steps += 1

        #dt = dt0
        #r = math.sqrt(((pos[1]-pos[0])**2).sum())
        #dt = dt0*r**1.5
        tau *= eta
        dt = dt0*tau													# <-- new

        E = energy(mass, pos, vel, eps**2)

        tplot.append(t)
        dEplot.append(E-E0)
        hplot.append(h)
        smaplot.append(a)
        eccplot.append(e)


        if t >= t_increment:
            t_increment += .5
            print('Energy error is = {} at t = {}'.format(abs(E - E0),t))
            print('dt = {}'.format(dt))

        if abs(E-E0) >= max_error:
            print('Error greater than max error = {}, error = {}, at t = {}'.format(max_error, abs(E-E0), t))
            print('dt = {}'.format(dt))
            break

#             j = 0
#             for i in range(50):
#                 temp_pos = np.concatenate(pos[i],j)

    # Final diagnostics.
    print('\n Answer to Q1a)')
    print('dt = {}'.format(dt))
    print('\nThe number of steps = {}'.format(np.size(tplot)))


N = 50
seed = 12345
eps = .005
dt = .01
t_end = 20
v0 = .1
eta = .5


main(N, seed, eps, dt, t_end, v0, eta)


## Q1 B&C

tiny = 1.e-20
def main(N, seed, eps, dt, t_end, v0, eta):
    if eps <= 0.0: eps = tiny
    dt0 = dt

    # Initial conditions.

    t = 0.0
    mass,pos,vel = initialize(N, seed, v0)
    steps = 0
    acc,tau = acc2(mass, pos, vel, eps**2)
    dt = dt0*tau

    tau0 = tau

    # Initial diagnostics.

    E0 = energy(mass, pos, vel, eps**2)
    print('Initial E =', E0)
    output(t, E0, mass, pos, vel, eps**2, steps)
#     a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0], pos[1],
#                                   vel[0], vel[1], eps**2)
#     print('semimajor axis =', a, ' eccentricity =', e)

    # Run forward to specified time.

    tplot = []
    dEplot = []
    hplot = []
    smaplot = []
    eccplot = []

    tot_E_plot = []
    tot_T_plot = []
    tot_U_plot = []
    virial_radius_plot = []
    tau_variation_plot = []

    half_time_unit = 0


    while t < t_end-0.5*dt:
        t,pos,vel,tau = step(t, mass, pos, vel, eps**2, dt)
        steps += 1

        #dt = dt0
        #r = math.sqrt(((pos[1]-pos[0])**2).sum())
        #dt = dt0*r**1.5
        tau *= eta
        dt = dt0*tau													# <-- new

        E = energy(mass, pos, vel, eps**2)
#         a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0],
#                                       pos[1], vel[0], vel[1], eps**2)

        T = kinetic_energy(mass, vel)
        U = potential_energy(mass, pos, eps**2)
        R_virial = -(mass.sum()**2)/(2*U)
        variation_tau = tau - tau0
        tau0 = tau

        tot_E_plot.append(E)
        tot_T_plot.append(T)
        tot_U_plot.append(U)
        virial_radius_plot.append(R_virial)
        tau_variation_plot.append(variation_tau)


        tplot.append(t)
        dEplot.append(E-E0)
#         hplot.append(h)
#         smaplot.append(a)
#         eccplot.append(e)
#         print(E0/N)

        if t >= half_time_unit:
            print('\nTime = {}, Energy Error = {}\n'.format(t, abs(E - E0)))
            half_time_unit += .5
            number_of_bound_parts = 0

            for i_temp in range(N):
                for j_temp in range(i_temp + 1, N):
                    dr2 = eps**2
                    rel_U = 0
                    for k in range(3):
                        dr2 += (pos[i_temp,k]-pos[j_temp,k])**2
                        rel_U -= mass[i_temp]*mass[j_temp]/math.sqrt(dr2)

                    rel_T = .5*mass[i_temp]*(vel[i_temp]**2).sum() + .5*mass[j_temp]*(vel[j_temp]**2).sum()
                    rel_E = rel_U + rel_T
#                     print(rel_U, rel_T, rel_E)
#                     print(E0/N)

                    sma, ecc, E_orb, h2 = orbital_elements(mass[i_temp], mass[j_temp],
                                                               pos[i_temp], pos[j_temp],
                                                               vel[i_temp], vel[j_temp], eps**2)
#                     if E_orb < E0/N:
                    if rel_E < E0/N:
#                         print(i_temp, j_temp)
                        number_of_bound_parts += 1
                        rel_orbital_period = 2*np.pi*np.sqrt(abs(sma**3)/(2*mass[i_temp]))
                        print('Bound Particles {} and {} with orbital energy = {} and period = {}'.format(i_temp, j_temp,E_orb, rel_orbital_period))
            print('Number of Bound Partices = {}'.format(number_of_bound_parts))


    # Final diagnostics.
    print('\n Q1 B&C Answer')
    print(t, abs(E - E0))
    print('Total time steps =', np.size(tplot))
    output(t, E0, mass, pos, vel, eps**2, steps)

    fig, ax = plt.subplots(2, 1, figsize = (8, 8))
    fig.suptitle('Question 1c')
    plt.subplots_adjust(wspace=.25)


    ax[0].plot(tplot, tot_E_plot, label = 'Total Energy')
    ax[0].plot(tplot, tot_T_plot, label = 'Total Kinetic Energy')
    ax[0].plot(tplot, tot_U_plot, label = 'Total Potential Energy')
    ax[0].plot(tplot, virial_radius_plot, label = 'Virial Radius')

    ax[0].set(xlabel = 'x', title = 'Phase Portrait')
    ax[0].legend()

    ax[1].plot(tplot, tau_variation_plot)
    ax[1].set(xlabel = 't', ylabel = 'change in tau', title = 'Varation in tau')
    ax[1].set_yscale('log')

    # plt.savefig('Q1c')

#     plt.subplot(2,2,1)
#     plt.plot(tplot, dEplot)
#     plt.xlabel('time')
#     plt.ylabel('energy error')

#     plt.subplot(2,2,2)
#     plt.plot(tplot, hplot)
#     plt.xlabel('time')
#     plt.ylabel('angular momentum')

#     plt.subplot(2,2,3)
#     plt.plot(tplot, smaplot)
#     plt.xlabel('time')
#     plt.ylabel('semimajor axis')

#     plt.subplot(2,2,4)
#     plt.plot(tplot, eccplot)
#     plt.xlabel('time')
#     plt.ylabel('eccentricity')

    plt.tight_layout()
    plt.show()

N = 50
seed = 12345
eps = .005
dt = .01
t_end = 20
v0 = .1
eta = .5

main(N, seed, eps, dt, t_end, v0, eta)


## Q1d


def main(N, seed, eps, dt, t_end, v0, eta):
    if eps <= 0.0: eps = tiny
    dt0 = dt

    # Initial conditions.

    t = 0.0
    mass,pos,vel = initialize(N, seed, v0)
    steps = 0
    acc,tau = acc2(mass, pos, vel, eps**2)

    # Initial diagnostics.

    E0 = energy(mass, pos, vel, eps**2)
    print('Initial E =', E0)
    output(t, E0, mass, pos, vel, eps**2, steps)
    a,e,Erel,h = orbital_elements(mass[0], mass[1], pos[0], pos[1],
                                  vel[0], vel[1], eps**2)
    print('semimajor axis =', a, ' eccentricity =', e)

    # Run forward to specified time.

    tplot = []
    dEplot = []

    max_error = .0001
    t_increment = 0


    while t < t_end-0.5*dt:
        t,pos,vel,tau = step(t, mass, pos, vel, eps**2, dt0)
        steps += 1

        E = energy(mass, pos, vel, eps**2)
        tplot.append(t)


        if t >= t_increment:
                t_increment += .5
                print('Energy error is = {} at t = {}'.format(abs(E - E0),t))
                print('dt = {}'.format(dt))

        if abs(E-E0) >= max_error:
            print('Error greater than max error = {}, error = {}, at t = {}'.format(max_error, abs(E-E0), t))
            print('dt = {}'.format(dt))
            break

#             j = 0
#             for i in range(50):
#                 temp_pos = np.concatenate(pos[i],j)

    # Final diagnostics.

    print('\n Q1d answer')
    print('dt = {}'.format(dt))
    print('\nThe number of steps = {}'.format(np.size(tplot)))

N = 50
seed = 12345
eps = .005
dt = .00005
t_end = 20
v0 = .1
eta = 10

main(N, seed, eps, dt, t_end, v0, eta)
