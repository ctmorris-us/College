# Phys 305 HW 5
# Christopher Morris
# Q1

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------
#
# Define the problem.

nonlin = 1

def deriv2(x, y):
    if nonlin == 0:
        return -y[0]
    else:
        return -y[0] - 10*y[0]**3

# Boundary conditions.

BC_a = 0.0
BC_ya = 1.0
BC_b = 1.0
BC_yb = 2.0

# Integration step and bisection tolerance.

dx = 0.001
tol = 1.e-4

# Range to search for a solution.

if nonlin == 0:
    zlin = -1.0
    zrin = 5.0
else:
    zlin = -100.0
    zrin = 100.0

#-----------------------------------------------------------------------

def f(x, y):
    return np.array([y[1], deriv2(x, y)])

def rk4_step(func, x, y, dx):
    dy1 = dx*func(x, y)
    dy2 = dx*func(x+0.5*dx, y+0.5*dy1)
    dy3 = dx*func(x+0.5*dx, y+0.5*dy2)
    dy4 = dx*func(x+dx, y+dy3)
    y += (dy1 + 2*dy2 + 2*dy3 + dy4)/6.
    x += dx
    return x, y

def integrate(func, a, ya, ypa, b, dx):
    x = a
    y = np.array([ya, ypa])
    while x < b-0.5*dx:
        x, y = rk4_step(f, x, y, dx)
    return x, y

def g(z):
    x, y = integrate(f, BC_a, BC_ya, z, BC_b, dx)
    return y[0]-BC_yb

def bisect(func, zl, zr, tol):
    n = 0
    while zr-zl > tol:
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
    return zl + (zr-zl)*(-gl)/(gr-gl)

def plotz(f, z):
    x = BC_a
    y = np.array([BC_ya, z])
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

    zl = zlin
    zr = zrin

    n = 501
    zz = np.linspace(zl, zr, n)
    gg = np.zeros(n)
    for i in range(n):
        gg[i] = g(zz[i])

    plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    plt.plot(zz, gg)
    plt.plot([zl,zr], [0.,0.], 'r--')
    plt.xlim(zl, zr)
    plt.xlabel('z')
    plt.ylabel('g(z)')
    plt.title('Q1 g(z) vs z')

    # Adjust limits if they don't straddle a root.

#     gl = g(zl)
#     while gl*g(zr) > 0: zr -= 1

    i = 0
    temp_zl = zz[i]
    temp_gl = gg[i]
    temp_zr = 0
    temp_gr = 0
    root_list = []
    root_pos_list = []

    while i != (n-1):
        i += 1
#         print(temp_zl, zz[i], i, n)
        if (np.sign(gg[i]) != np.sign(temp_gl)):
            if gg[i] == 0:
                root_list.append(gg[i])
            else:

#                 print(temp_zl, val)
                temp_zr = zz[i]
                m,zzl,zzr = bisect(g, temp_zl, temp_zr, 1.e-6)
                zs = secant1(g, zzl, zzr)
                root_list.append(zs)
                print('Root at =',zs)

            temp_zl = zz[i]
            temp_gl = gg[i]



#     for val in gg:
#         if (np.sign(temp_zl)) == np.sign(val)) and (val != 0):
#             pass
#         elif (np.sign(g(temp_zl)) != np.sign(val)) and (val != 0):
#             print(temp_zl, val)
#             temp_zr = val
#             n,zzl,zzr = bisect(g, temp_zl, temp_zr, 1.e-6)
#             zs = secant1(g, zzl, zzr)
#             root_list.append(zs)
#             print('Root at =',zs)
#             temp_zl = val
#         else:
#             pass

    plt.subplot(1,2,2)
    #n,zzl,zzr = bisect(g, zl, zr, 1.e-6)
    #print "Root lies in (%f, %f) after %d iterations"%(zzl, zzr, n)
    #print "Function value =", g(0.5*(zzl+zzr))
    #zs = secant1(g, zzl, zzr)
    for z_i in root_list:
        plotz(f, z_i)
    print('z =', zs, 'g(z) =', g(zs))
    plotz(f, zs)
    plt.legend(loc='best')
    plt.title('Q1) Solutions to equation')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.tight_layout()

    plt.show()
    # plt.savefig('Q1.jpg')

main()
