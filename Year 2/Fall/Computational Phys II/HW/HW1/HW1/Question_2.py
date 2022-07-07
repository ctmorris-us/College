# import sys
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')


# Christopher Morris HW 1 Phys 305


import math
import matplotlib.pyplot as plt
import numpy as np

dx = 0

def f(x):
    return x * np.cos(x)

def fi(x):
    return x*np.sin(x) + np.cos(x)

def basic(f, x, dx):
    return dx * f(x).sum()

def trapezoidal(f, x, dx):
    return dx*(.5*(f(x[0]) + f(x[-1])) + f(x[1:-1]).sum())

def simpsons(f, x, dx):
    return dx*(f(x[0]) + f(x[-1]) + 4*f(x[1:-1:2]).sum() + 2*f(x[2:-2:2]).sum())/3

basic_error = []
trapezoidal_error = []
simpsons_error = []
dxplot = []

xmax = 2
xmin = 0

N = 4
Nmax = 2 ** 20
true_int = fi(xmax) - fi(xmin)



while N <= Nmax:

    x = np.linspace(xmin, xmax, N+1) #add another rectangle
    dx = (xmax-xmin)/N
    dxplot.append(dx)

    basic_error.append(abs(basic(f, x, dx) - true_int))
    trapezoidal_error.append(abs(trapezoidal(f, x, dx) - true_int))
    simpsons_error.append(abs(simpsons(f, x, dx) - true_int))


    N *= 2


fig, ax = plt.subplots(1,3, figsize = (14, 6))
fig.suptitle('Question 2A')
plt.subplots_adjust(wspace=.25)

ax[0].loglog(dxplot, basic_error, 'r-')
ax[0].set(xlabel = 'log($\Delta$x)', ylabel = 'log(error)', title = 'Basic Integration Scheme')

ax[1].loglog(dxplot, trapezoidal_error, 'b--')
ax[1].set(xlabel = 'log($\Delta$x)', ylabel = 'log(error)', title = 'Trapezoidal Integration Scheme')

ax[2].loglog(dxplot, simpsons_error, 'g--')
ax[2].set(xlabel = 'log($\Delta$x)', ylabel = 'log(error)', title = 'Simpson Integration Scheme')

plt.show()


print('The final errors for N = 20^20; Basic:', basic_error[-1], 'Trapezoidal:', trapezoidal_error[-1], 'Simpsons:', simpsons_error[-1])

N = 4
Nmax = 32
trapezoidal_vals = []

dxplot = []


while N <= Nmax:

    x = np.linspace(xmin, xmax, N+1) #add another rectangle
    dx = (xmax-xmin)/N



    dxplot.append(dx)
    trapezoidal_vals.append(trapezoidal(f, x, dx))

    N *= 2

trapezoidal_error = abs(trapezoidal_vals - true_int)

p = np.polyfit(dxplot, trapezoidal_vals, 3)
print('p1:', p[0], 'p2:', p[1], 'p3:', p[2],'p4:', p[3], '\n')

print('True integral:', true_int)
print('Extrapolated integral from polynomial fitting:', p[3], 'with an error of:', abs(p[3] - true_int))
print('The error with dx = 1/16:', trapezoidal_error[2])
