# import sys
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')

# Christopher Morris HW 1 Phys 305 

import math
import matplotlib.pyplot as plt
import numpy as np

GM = 1
epsilon = .1

def theta(r):
    return -1/np.sqrt(np.power(r, 2) + epsilon**2)

def v2(r):
    return 2/((r**2 + epsilon**2)**.5) - 1/(2*r**2) - 1

def bisection(a, b, h, error):
    if h(a) < 0:
        while abs(a-b) > error:
            m = (a+b)/2
            y = h(m)
            if y < 0:
                a = m
            elif y > 0:
                b = m
    else:
        while abs(a-b) > error:
            m = (a+b)/2
            y = h(m)
            if y < 0:
                b = m
            elif y > 0:
                a = m
    return m


rl = bisection(.001, 1, v2, 1e-9)
ru = bisection(1.2, 2, v2, 1e-9)

print('\n3A)')
print('\nroot 1:', rl)
print('root 2:', ru)


def gauss_cheb(f, n):

    x = []
    r = []
    for i in range(n):
        #x.append(math.cos((2*i+1)*math.pi/(2.*n)))
        xi = math.cos((2*i+1)*math.pi/(2*n))
        ri = (ru + rl)/2 + xi*(ru - rl)/2
        r.append(ri)

    w = math.pi/n

    sum = 0.0
    for i in range(len(r)):
        sum += w*f(r[i])
    return sum

def func(r):
    return 2 * np.power((r - rl), .5)* np.power((ru - r), .5) * np.power(v2(r), -.5)

integral = gauss_cheb(func, 10)
print('integral =', integral)

GM = 1
epsilon = 0

def theta(r):
    return -1/np.sqrt(np.power(r, 2) + epsilon**2)

def v2(r):
    return 2/((r**2 + epsilon**2)**.5) - 1/(2*r**2) - 1

def bisection(a, b, h, error):
    if h(a) < 0:
        while abs(a-b) > error:
            m = (a+b)/2
            y = h(m)
            if y < 0:
                a = m
            elif y > 0:
                b = m
    else:
        while abs(a-b) > error:
            m = (a+b)/2
            y = h(m)
            if y < 0:
                b = m
            elif y > 0:
                a = m
    return m

def gauss_cheb(f, n):

    x = []
    r = []
    for i in range(n):
        #x.append(math.cos((2*i+1)*math.pi/(2.*n)))
        xi = math.cos((2*i+1)*math.pi/(2*n))
        ri = (ru + rl)/2 + xi*(ru - rl)/2
        r.append(ri)

    w = math.pi/n

    sum = 0.0
    for i in range(len(r)):
        sum += w*f(r[i])
    return sum

def func(r):
    return 2 * np.power((r - rl), .5)* np.power((ru - r), .5) * np.power(v2(r), -.5)

rl = bisection(.001, 1, v2, 1e-9)
ru = bisection(1.2, 2, v2, 1e-9)


integral = gauss_cheb(func, 10)
actual_integral = 2*np.pi*np.power((2*.5), -3/2)

print('\n3B)')
print('\nroot 1:', rl)
print('root 2:', ru)
print('\ncomputed integral =', integral)
print('Actual integral:', actual_integral )
