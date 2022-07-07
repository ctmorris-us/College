
# Template program for the simple integration scheme

import math, sys 

def interp(x0, y0, x1, y1, x):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

def acc(k, x, v, t):
    # acceleration
    return -1                   

def potential(k, x):
    # potential: MUST be consistent with acc!
    return -1                   

def energy(k, x, v):
    return potential(k, x) + 0.5*v*v

def output(K, x, v, t, E0):
    print t, x, v, energy(K, x,v) - E0

def take_a_step(k, x, v, t, dt):

    # Set the acceleration.
    a = acc(k, x, v, t)

    # Take the step.
    x += v*dt + 0.5*a*dt*dt
    v += a*dt

    return x,v

# Declaration and initialization.

K  = 
t  = 0.0
x  = 
v  = 
dt = 
tmax = 

E0 = energy(K, x, v)
output(K, x, v, t, E0)

# Integrate the motion to the specified time.

while ():
    
    (x,v) = take_a_step(K, x, v, t, dt)
    
    #t += dt
    #x += dx
    
    output(K, x, v, t, E0)  
