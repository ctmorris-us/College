# Phys 305 HW 5
# Christopher Morris
# Q3

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------
#
# Define the problem.

def U(x):
    return x**2

def deriv2(x, y):
    return -1*(y[2] - U(x))*y[0]				# y[2] is the eigenvalue z

# Boundary conditions.



BC_a = 0
BC_b = 6
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
    return y[1] + eta * y[0]

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
    ax.set(xlabel = 'x', ylabel = 'y', title = 'Q3 Eigenfunctions')
    plt.plot()
    parity_vals = [0.0, 1.0]
    plt.plot([0, 4], [0,0], 'k-')


    global parity
    for val in parity_vals:
        parity = val
        number_of_eigs = 0

        zl = 0.0
        zr = U0

        n = 100
        zz = np.linspace(zl, zr, n)
        gg = np.zeros(n)
        for i in range(n):
            gg[i] = g(zz[i])

        i = 0

        temp_zl = zz[i]
        temp_gl = gg[i]
        temp_zr = 0
        temp_gr = 0
        root_list = []
        root_pos_list = []


        while number_of_eigs != 5:
            i += 1
            if i == n-1:
                print('Found all solutions')
                break
            if (np.sign(gg[i]) != np.sign(temp_gl)):
                number_of_eigs += 1

                if gg[i] == 0:
                    root_list.append(gg[i])
                else:
                    temp_zr = zz[i]
                    m,zzl,zzr = bisect(g, temp_zl, temp_zr, 1.e-6)
                    zs = secant1(g, zzl, zzr)
                    root_list.append(zs)
                    print('z =', zs, 'g(z) =', g(zs), 'With Parity = ',parity)


                temp_zl = zz[i]
                temp_gl = gg[i]

        for z_i in root_list:
            x = BC_a
            y = np.array([parity, 1-parity, z_i])
            xx = [x]
            yy = [y[0]]
            while x < BC_b-0.05*dx:
                x, y = rk4_step(f, x, y, dx)
                xx.append(x)
                yy.append(y[0])
            if parity == 1.0:
                plt.plot(xx, yy, label = 'z = {}, parity = {}'.format(z_i, parity))
            else:
                plt.plot(xx, yy, '--', label = 'z = {}, parity = {}'.format(z_i, parity))



#             n,zzl,zzr = bisect(g, zl, zr, 1.e-6)
#             zs = secant1(g, zzl, zzr)

# #                 if parity == 1.0:
# #                     ax.plot(U0, zs, 'ko', markersize = 2, label = 'Parity = 1')
# #                 else:
# #                     ax.plot(U0, zs, 'go', markersize = 2, label = 'Parity = 0')

#             print('z =', zs, 'g(z) =', g(zs), 'With Parity = ',parity)
#             zl = zs




    ax.legend()
    plt.show()

    # plt.savefig('Q3.jpg')

main()
