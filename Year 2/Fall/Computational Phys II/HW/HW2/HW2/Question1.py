import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')

# Christopher Morris HW 2 Phys 305


import math
import matplotlib.pyplot as plt
import numpy as np

def general_rk_step(f, x, y, dx):

    a = np.array([0, 1/5, 3/10, 3/5, 1, 7/8])
    c = np.array([37/378, 0, 250/621, 125/594, 0, 512/1771])
    b = np.array([[0, 0, 0, 0, 0, 0],
                  [1/5, 0, 0, 0, 0, 0],
                  [3/40, 9/40, 0, 0, 0, 0],
                  [3/10, -9/10, 6/5, 0 ,0, 0],
                  [-11/54, 5/2, -70/27, 35/27, 0, 0],
                  [1631/55296, 175/512, 575/13824, 44275/110592, 253/4096, 0]])

    s = np.size(a)

    dy0 = dx * f(x, y)
    dy1 = dx * f(x + a[1]*dx, y + b[1,0]*dy0)
    dy2 = dx * f(x + a[2]*dx, y + b[2,0]*dy0 + b[2,1]*dy1)
    dy3 = dx * f(x + a[3]*dx, y + b[3,0]*dy0 + b[3,1]*dy1 + b[3,2]*dy2)
    dy4 = dx * f(x + a[4]*dx, y + b[4,0]*dy0 + b[4,1]*dy1 + b[4,2]*dy2 + b[4,3]*dy3)
    dy5 = dx * f(x + a[5]*dx, y + b[5,0]*dy0 + b[5,1]*dy1 + b[5,2]*dy2 + b[5,3]*dy3 + b[5,4]*dy4)

    y += c[0]*dy0 + c[1]*dy1 + c[2]*dy2 + c[3]*dy3 + c[4]*dy4 + c[5]*dy5
    x += dx


    return x, y

def general_rk_step_reverse(f, x, y, dx):
    a = np.array([0, 1/5, 3/10, 3/5, 1, 7/8])
    c = np.array([37/378, 0, 250/621, 125/594, 0, 512/1771])
    b = np.array([[0, 0, 0, 0, 0, 0],
                  [1/5, 0, 0, 0, 0, 0],
                  [3/40, 9/40, 0, 0, 0, 0],
                  [3/10, -9/10, 6/5, 0 ,0, 0],
                  [-11/54, 5/2, -70/27, 35/27, 0, 0],
                  [1631/55296, 175/512, 575/13824, 44275/110592, 253/4096, 0]])

    s = np.size(a)

    dy0 = dx * f(x, y)
    dy1 = dx * f(x - a[1]*dx, y - b[1,0]*dy0)
    dy2 = dx * f(x - a[2]*dx, y - b[2,0]*dy0 - b[2,1]*dy1)
    dy3 = dx * f(x - a[3]*dx, y - b[3,0]*dy0 - b[3,1]*dy1 - b[3,2]*dy2)
    dy4 = dx * f(x - a[4]*dx, y - b[4,0]*dy0 - b[4,1]*dy1 - b[4,2]*dy2 - b[4,3]*dy3)
    dy5 = dx * f(x - a[5]*dx, y - b[5,0]*dy0 - b[5,1]*dy1 - b[5,2]*dy2 - b[5,3]*dy3 - b[5,4]*dy4)

    y -= c[0]*dy0 + c[1]*dy1 + c[2]*dy2 + c[3]*dy3 + c[4]*dy4 + c[5]*dy5
    x -= dx


    return x, y


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

def euler_step(func, x, y, dx):
    y += dx*func(x, y)
    x += dx
    return x, y


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

    x, y = general_rk_step(f, x, y, dx)
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

        x, y = general_rk_step(f, x, y, dx)
        #x, y = euler_step(f, x, y, dx)


    eplot.append(abs(energy(x, y) - e_initial))
    dxplot.append(dx)

plt.figure()

plt.loglog(dxplot, eplot, 'k')
plt.xlabel('log(dx)')
plt.ylabel('log(abs(error))')
plt.title('Question 1b')

xmax = 20
dx = 0.01
x = 0.0
y0 = 1
v0 = 1.5
y = np.array([y0, v0])

while x < xmax:
    xp = x
    yp = y[0]
    vp = y[1]

    if x == 0: yp = y0 + 1

    x, y = general_rk_step(f, x, y, dx)
    #x, y = euler_step(f, x, y, dx)

while x > 0:

    xp = x
    yp = y[0]
    vp = y[1]

    x, y = general_rk_step_reverse(f, x, y, dx)

    #x, y = euler_step(f, x, y, dx)
print('The Final Values after reversing the scheme is:')
print('x:  {}; y:  {}; v:  {}'.format(xp, yp, vp))

plt.show()
