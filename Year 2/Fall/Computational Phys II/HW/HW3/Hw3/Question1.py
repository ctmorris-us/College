import numpy as np
import math
import matplotlib.pyplot as plt
import sys

## HW 3
# Phys 305
# Christopher Morris

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

# Part A

xplots = []
yplots = []
vplots = []
eplots = []

xmax = 20
dx = 0.01
x = 0.0
y0 = 1
v0 = 1.5
y = np.array([y0, v0])
e_initial = energy(x, y)

xplot = [x]
yplot = [y[0]]
vplot = [y[1]]
eplot = [0]

while x < xmax:
    yp = y[0]
    vp = y[1]

    if x == 0: yp = y0 + 1

    x, y = kick_drift_step(f, x, y, dx)
    #x, y = euler_step(f, x, y, dx)

    xplot.append(x)
    yplot.append(y[0])
    vplot.append(y[1])
    eplot.append(energy(x, y) - e_initial)

    #print(x, y)
#     if yp <= y0 and y[0] > y0:
#         break


fig, ax = plt.subplots(1, 2, figsize = (10, 4))
fig.suptitle('Question 1a')
plt.subplots_adjust(wspace=.25)

# vint = vp + (y[1]-vp)*(y[0]-y0)/(y[0]-yp)
# print('vint =', vint, 'err =', abs((vint-v0)/v0))


ax[0].plot(xplot, yplot, 'k')
ax[0].set(xlabel = 'x', ylabel = 'y', title = 'Phase Portrait')

ax[1].plot(eplot, xplot, 'k')
ax[1].set(xlabel = 'x', ylabel = 'Energy error', title = 'Energy Error Plot')
plt.show()

#Part B

xmax = 20
dx = 0.01
x = 0.0
y0 = 1
v0 = 1.5
y = np.array([y0, v0])
e_initial = energy(x, y)

eplot = []
dxplot = []

for n in range(1, 14):
    x = 0.0
    y0 = 1
    v0 = 1.5
    y = np.array([y0, v0])
    e_initial = energy(x, y)
    dx = 2**(-n)

    while x < xmax:
        yp = y[0]
        vp = y[1]

        if x == 0: yp = y0 + 1

        x, y = kick_drift_step(f, x, y, dx)
        #x, y = euler_step(f, x, y, dx)


    eplot.append(abs(energy(x, y) - e_initial))
    dxplot.append(dx)

plt.loglog(dxplot, eplot, 'k')
plt.xlabel('log(dx)')
plt.ylabel('log(abs(error))')
plt.title('Question 1c')
plt.show()

# Part C


xmax = 5
dx = 0.001
x = 0.0
y0 = 1
v0 = 1.5
y = np.array([y0, v0])

def interp(x0, y0, x1, y1, x=None, y=None):
    if y == None:
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    elif x == None:
        return (y-y0) * (x1 - x0) / (y1 - y0) + x0

while x < xmax:
    xp = x
    yp = y[0]
    vp = y[1]

    if x == 0: yp = y0 + 1

    x, y = kick_drift_step(f, x, y, dx)
#     print(x, y)
    #x, y = euler_step(f, x, y, dx)

while x > 0:

    xp = x
    yp = y[0]
    vp = y[1]

    x, y = kick_drift_step(f, x, y, -dx)

#     print(x,y)
    #x, y = reverse_euler_step(f, x, y, dx)

ynew = interp(xp, yp, x, y[0], x = 0)
vnew = interp(xp, vp, x, y[1], x = 0)



print('x = {}, y = {}, v = {}, dx = {}'.format(xp, ynew, vnew, dx))
