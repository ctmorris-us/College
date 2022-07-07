'''
Name: prog3.py

The program is a simulation of a three body system
based on a model solar system with only the sun, earth, and jupiter.

Date made: Oct. 13, 2018

The simulation works by having three bodies and calculating the total gravitational force between all
three of them. The gravitational force is then used to update the velocity of each body which is then
used to update all the positions. The simulation runs for approximately 20 years.

The program was created with VPython to implement our studies of gravity and momentumself.

The program is set up with realistic masses and velocities of all of the bodies. However, when the masses
are changed (ex. 400 * MJupiter) the simulation becomes chaotic.


'''

from vpython import *
import numpy as np

'''
Initialization:
Initializing distance as astronomical unit, the gravitational constant, masses of the planets, a length of a year,
the change in time, and the initial time.
'''
AU=1.5e11
G=6.67e-11
Msun=2e30
Mearth=6e24
Mjupiter=1.9e27
yr=3.15e7
dt=0.001*yr
t=0

'''
Setting the scene and initializing each planet with their color, position, radius (not important to the simulation)
mass, and initial velocity.
'''

scene.range=6*AU
scene.autoscale=0

earth = sphere(pos = vec(1*AU, 0, 0), color = color.green, radius = .1*AU, mass = Mearth, v = vec(0,30000,0), texture = textures.earth)
sun = sphere(pos = vec(0,0,0), color = color.yellow, radius = .3*AU, mass = .6*Msun, v = vec(3000,0,5000))
jupiter = sphere(pos = vec(5.2*AU,0,0), color = color.red, radius = .2*AU, mass = Mjupiter, v = vec(0,13000,0))

trail = curve(color = color.blue)
trailJ = curve(color = color.orange)


'''
Unimportant code kept by the creator for possible future implementation
'''
# def initialize_matrix(*args):
#
#     mass_vector = np.array([x.mass for x in iter(*args)])
#     mass_vector.shape = (len(mass_vector), 1)
#     mass_matrix = np.dot(mass_vector, mass_vector.T)
#
#     distance_vector_x = np.array([x.pos for x in iter(*args)])
#     distance_vector_x.shape = (len(distance_vector_x), 1)
#     # distance_vector_y = np.array([y.pos.y for y in iter(*args)])
#     # distance_vector_y.shape = (len(distance_vector_y), 1)
#     # distance_vector_z = np.array([z.pos.z for z in iter(*args)])
#     # distance_vector_z.shape = (len(distance_vector_z), 1)
#     #
#     distance_matrix_x = np.add(distance_vector_x, -1*distance_vector_x.T)
#     # distance_matrix_y = np.add(distance_vector_y, -1*distance_vector_y.T)
#     #distance_matrix_z = np.add(distance_vector_z, -1*distance_vector_z.T)
#
#
#     force_matrix = G * mass_matrix * distance_matrix /

'''
This function calculates the total force on each planet.
'''

def force():
    r1 = sun.pos-earth.pos
    r2 = sun.pos-jupiter.pos
    r3 = earth.pos - jupiter.pos

    f1 = G*earth.mass*sun.mass*r1/(mag(r1)**3)
    f2 = G*jupiter.mass*sun.mass*r2/(mag(r2)**3)
    f3 = G*earth.mass*jupiter.mass*r3/(mag(r3)**3)

    tf_sun = -1*(f1+f2) #Multiplied by negative one because it's on the left side at the start
    tf_earth = f1+f3
    tf_jup = f2+f3

    return(tf_sun, tf_earth, tf_jup)

'''
Main body of the simulation:
It goes for 20 years.
'''
while (t < 20*yr):
    rate(800)
    #Sets the number of calculations per second.

    earth.pos = earth.pos + earth.v*dt
    sun.pos = sun.pos + sun.v*dt
    jupiter.pos = jupiter.pos + jupiter.v*dt
    # Updating the position of each planet

    trail.append(earth.pos)
    trailJ.append(jupiter.pos)
    # updates the trails

    tf_sun, tf_earth,tf_jup = force()
    earth.v = earth.v + tf_earth*dt/earth.mass
    jupiter.v = jupiter.v + tf_jup*dt/jupiter.mass
    sun.v = sun.v + tf_sun*dt/sun.mass
    #Updates the velocities based on the forces returned by the force function

    t = t + dt
    #Updates the time
