# Phys 305 HW 5
# Christopher Morris
# Q2

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------
#
# Define the problem.

def U(x):
    if abs(x) < 1:
        return 0
    else:
        return U0

def deriv2(x, y):
    return -1*(y[2] - U(x))*y[0]				# y[2] is the eigenvalue z

# Boundary conditions.



BC_a = 0
BC_b = 1.0


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
    x, y = integrate(f, 0.0, parity, 1-parity, z, BC_b, dx)
    eta = np.sqrt(max((U0-z), 0))
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
    x = BC_a
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
    ax.set(xlabel = 'U0', ylabel = 'z', title = 'Bound energy vs U0')
    parity_vals = [0.0, 1.0]


    global U0, parity
    U0_end = 100

    for val in parity_vals:
        parity = val
        U0 = 0.0

        while U0 < U0_end:

            #Different Integrator
            zl = 0
            zr = 1e-4
            temp_gl = g(zl)
            temp_gr = g(zr)

            while zr <= U0-.1/2:

                if np.sign(temp_gl) != np.sign(temp_gr):
                    if temp_gr == 0:
                        print('z =', zs, 'g(z) =', g(zs), 'For U0 = ',U0, 'With Parity = ',parity)
                        if parity == 1.0:
                            ax.plot(U0, zs, 'ko', markersize = 2, label = 'Parity = 1')
                        else:
                            ax.plot(U0, zs, 'go', markersize = 2, label = 'Parity = 0')

                    else:
                        m,zzl,zzr = bisect(g, zl, zr, 1.e-6)
                        zs = secant1(g, zzl, zzr)
                        print('z =', zs, 'g(z) =', g(zs), 'For U0 = ',U0, 'With Parity = ',parity)

                        if parity == 1.0:
                            ax.plot(U0, zs, 'ko', markersize = 2, label = 'Parity = 1')
                        else:
                            ax.plot(U0, zs, 'go', markersize = 2, label = 'Parity = 0')
                    zl = zr
                    zr = zl + .1
                    temp_gl = temp_gr

                else:
                    zr += .1
                    temp_gr = g(zr)
            U0 += .1

            #Different Integrator

#             zl = 0.0
#             zr = U0

#             n = 500
#             zz = np.linspace(zl, zr, n)
#             gg = np.zeros(n)
#             for i in range(n):
#                 gg[i] = g(zz[i])

#             i = 0

#             temp_zl = zz[i]
#             temp_gl = gg[i]
#             temp_zr = 0
#             temp_gr = 0
#             root_list = []
#             root_pos_list = []


#             while i != n-1:
#                 i += 1
#                 if (np.sign(gg[i]) != np.sign(temp_gl)):
#                     if gg[i] == 0:
#                         print('z =', zs, 'g(z) =', g(zs), 'For U0 = ',U0, 'With Parity = ',parity)
#                         if parity == 1.0:
#                             ax.plot(U0, zs, 'ko', markersize = 2, label = 'Parity = 1')
#                         else:
#                             ax.plot(U0, zs, 'go', markersize = 2, label = 'Parity = 0')
#                     else:
#                         temp_zr = zz[i]
#                         m,zzl,zzr = bisect(g, temp_zl, temp_zr, 1.e-6)
#                         zs = secant1(g, zzl, zzr)
#                         print('z =', zs, 'g(z) =', g(zs), 'For U0 = ',U0, 'With Parity = ',parity)

#                         if parity == 1.0:
#                             ax.plot(U0, zs, 'ko', markersize = 2, label = 'Parity = 1')
#                         else:
#                             ax.plot(U0, zs, 'go', markersize = 2, label = 'Parity = 0')




#                     temp_zl = zz[i]
#                     temp_gl = gg[i]


           ###Other Integrator


    #             zl = 0.0
    #             zr = U0

    #             while True:
    #                 n,zzl,zzr = bisect(g, zl, zr, 1.e-6)

    #                 if abs(U0 - zzl)  < tol:
    # #                     print('The left side has reached max energy')
    #                     break

    #                 zs = secant1(g, zzl, zzr)

    #                 if parity == 1.0:
    #                     ax.plot(U0, zs, 'ko', markersize = 2, label = 'Parity = 1')
    #                 else:
    #                     ax.plot(U0, zs, 'go', markersize = 2, label = 'Parity = 0')

    #                 print('z =', zs, 'g(z) =', g(zs), 'For U0 = ',U0, 'With Parity = ',parity)
    #                 zl = zs + 10e-6

#             U0 += .1

    ax.legend()
    plt.show()

    # plt.savefig('Q2.jpg')


main()
