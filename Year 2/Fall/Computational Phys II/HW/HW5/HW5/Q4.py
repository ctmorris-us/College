# Phys 305 HW 5
# Christopher Morris
# Q4

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------
#
# Define the problem.

def U(x):
    return -1*np.exp(-1*np.sqrt(abs(x)))

def deriv2(x, y):
    return -1*(y[2] - U(x))*y[0]				# y[2] is the eigenvalue z

# Boundary conditions.



BC_a = 0
BC_b = 35
U0 = U(BC_b)


# Integration step and bisection tolerance.

dx = 0.01
tol = 1.e-4

#

#-----------------------------------------------------------------------

def f(x, y):
    return np.array([y[1], deriv2(x, y), 0.]) 	# z' = 0

def rk4_step(func, x, y, dx):
    dy1 = dx*func(x, y)
    dy2 = dx*func(x+0.5*dx, y+0.5*dy1)
    dy3 = dx*func(x+0.5*dx, y+0.5*dy2)
    dy4 = dx*func(x+dx, y+dy3)
    y += (dy1 + 2*dy2 + 2*dy3 + dy4)/6.
    x += dx
    return x, y

def integrate(func, a, ya, ypa, z, b, dx):
    x = a
    y = np.array([ya, ypa, z])			# z is the eigenvalue
    while x < b-0.5*dx:
        x, y = rk4_step(f, x, y, dx)
    return x, y

def g(z):
    eta = np.sqrt(max((U0-z), 0))
    x, y = integrate(f, 0.0, parity, 1-parity, z, BC_b, dx)
    return y[1] - np.sqrt(2.0)*x*y[0]
#     return y[1] + eta * y[0]

def bisect(func, zl, zr, tol):
    n = 0
    while zr-zl > tol:
#         print('zr = {}, zl = {}'.format(zr, zl))
        zm = 0.5*(zl + zr)
        if func(zm)*func(zl) > 0:
            zl = zm
        else:
            zr = zm
        n += 1

    return n,zl,zr

def secant1(g, zl, zr):
    gl = g(zl)
    gr = g(zr)

#     print('gl = {}, gr = {}'.format(gl, gr))
    return zl + (zr-zl)*(-gl)/(gr-gl)

def plotz(f, z):
    x = a
    y = np.array([BC_ya, 1.0, z])
    xx = [x]
    yy = [y[0]]
    while x < BC_b-0.5*dx:
        x, y = rk4_step(f, x, y, dx)
        xx.append(x)
        yy.append(y[0])
    plt.plot(xx, yy, label='z = {:.3f}'.format(z))
    plt.xlim(BC_a, BC_b)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot([BC_a], [BC_ya], 'o', clip_on=False,
             markeredgewidth=1, markeredgecolor='r', markerfacecolor='None')
    plt.plot([BC_b], [BC_yb], 'o', clip_on=False,
             markeredgewidth=1, markeredgecolor='r', markerfacecolor='None')

def main():

    fig, ax = plt.subplots(1, 1, figsize = (10,10))
    ax.set(xlabel = 'x', ylabel = 'y', title = 'Q4 Eigenfunctions')
#     plt.plot([0, 6], [0,0], 'k-')


    parity_vals = [0.0, 1.0]


    global U0, parity

    for val in parity_vals:
        parity = val
        U0 = 0.0

        #Different Integrator
        zl = -1
        zr = -1 + 1e-4
        temp_gl = g(zl)
        temp_gr = g(zr)
        root_list = []
        while zr <= U0+1e-5/2:
            if np.sign(temp_gl) != np.sign(temp_gr):
                if temp_gr == 0:
                    print('z =', zs, 'g(z) =', g(zs),'With Parity = ',parity)
                    root_list.append(temp_gr)
                else:
                    m,zzl,zzr = bisect(g, zl, zr, 1.e-6)
                    zs = secant1(g, zzl, zzr)
                    print('z =', zs, 'g(z) =', g(zs),'With Parity = ',parity)
                    root_list.append(zs)
                zl = zr
                zr = zl + .01
                temp_gl = temp_gr

            else:
                zr += .01
                temp_gr = g(zr)

        for z_i in root_list:
            x = BC_a
            y = np.array([parity, 1-parity, z_i])
            xx = []
            yy = []
#             xx = [x]
#             yy = [y[0]]

            while x > -1*BC_b+0.5*dx:
                x, y = rk4_step(f, x, y, -1*dx)
#                 xx.append(x)
#                 yy.append(y[0])

            while x < BC_b-0.5*dx:
                x, y = rk4_step(f, x, y, dx)
                xx.append(x)
                yy.append(y[0])



            if parity == 1.0:
#                 xx += [-x for x in xx]
#                 yy += [y for y in yy]
                plt.plot(xx, yy, '-', label = 'z = {}, parity = {}'.format(z_i, parity))
            else:
#                 xx += [-x for x in xx]
#                 yy += [-y for y in yy]
                plt.plot(xx, yy, '--', label = 'z = {}, parity = {}'.format(z_i, parity))




    ax.legend()
    plt.show()

    # plt.savefig('Q4.jpg')

main()
