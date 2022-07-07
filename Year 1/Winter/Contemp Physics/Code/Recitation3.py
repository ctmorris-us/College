#Recitation 3
import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')
'''
Recitation 3
Name: Christopher Morris
Date: May 22, 2019

Purpose:
A simple program made to model the effects of multiple different fields on a particle with an initial velocity (3,0,0).
The different fields available are: no field, a magentic field in (0,0,1), a magnetic field in (1,1,1), and an electric field in (0,1,0).
The particle has an initial velocity, and at every time step an acceleration is calculated by the force of each field by the mass.
A single curve is made for each loop of the particle.

Notes:
The orange curve is the zero field
The magenta curve is the (0,1,0) E field
The Blue curve is the (0,0,1) B field
The red curve is the (1,1,1) B field

The curves are also very jumpy on my computer.
'''


from vpython import *

#No electric or magnetic field
def F_BE(v, q):
    return vec(0,0,0)

#B field in (0,0,1) direction
def F_B1(v, q):
    B = vec(0,0,1)
    return cross(q*v, B)

#B field in (1,1,1) direction
def F_B2(v, q):
    B = vec(1,1,1)
    return cross(q*v, B)

#Electric field in (0,1,0) direction
def F_E(v, q):
    E = vec(0,1,0)
    return q*E

m, q = 1, 1 #charge and mass
r0 = vec(0,0,0) #starting position
v0 = vec(3,0,0) #initial velocity

colors_list = [color.red, color.blue, color.magenta, color.orange] #colors to choose from
particle = sphere(pos = vec(0,0,0), velocity = vec(0,0,0), acceleration = vec(0,0,0), radius = 1, mass = m, charge = q) #particle to manipulate
curves = []

functions = [F_BE, F_E, F_B1, F_B2]
for func in functions: #uses each field function to model the movement
    color = colors_list.pop() #gets color
    particle.color = color
    particle.pos = r0
    particle.velocity = v0
    particle.trail_color = color
    #sets particle and trail color, particle position, particle velocity

    curves.append(curve(color = particle.color, emissive = True)) #Makes curve to append points to
    curves[-1].append(particle.pos)

    rate(60)
    t = 0
    dt = .001
    while t < 10:
        #updates acceleration, velocity, and position, and appends the particle position to the curve
        particle.acceleration = func(particle.velocity, particle.charge) * particle.mass
        particle.velocity += particle.acceleration * dt
        particle.pos += particle.velocity * dt
        curves[-1].append(particle.pos)
        t += dt
