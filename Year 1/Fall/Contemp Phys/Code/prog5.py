'''
Name: prog5.py

Program is a simulation of a rocket ship traveling from earth to alpha centari and experiencing
relativistic length contraction and time dialation.

Date Made: Oct 31, 2018

The simulation works by updating a rockets momentum by a constant force and then using the
updated momentum to update the velocity and then position. A gamma value is calculated from
momentum. The gamma value then is used to calculate time dialation and length contraction.
The force is applied towards alpha centari until the ship reaches half the distance and then
the force is applied backwards.

The program was created with Vpython to study relativistic principles

The program is set up with lengths in light years between the planets and the position of the
middle of the ship is used to calculate when the force should be applied in the opposite direction.

'''

from vpython import *
from math import *
'''
Initializing values for the program. The speed of light is given and then calculated for lightyears.
The rocket length, gamma, earth radius, alpha centari radius, and distance to alpha centari are set.
The force is given and then calculated to fit lightyears/years.
The variables for time on earth, distance from earth's perspective, time on ship, distance from
the ship's perspective, the mass of the rocket, and dt are set.
'''
c_regular = 3e8
c_light = c_regular * 1.05e-16 * 3.15e8
light_year = 1.057

rocket_length = 1
gamma = 1
earth_radius = 1
alpha_radius = 1
alpha_distance = 4.3

force = vec(9800,0,0)
force_lightyr = vec(9800 * ((3.17e8)**2) * (1.057e-16),0,0)

time_earth = 0
distance_earth = 0
time_ship = 0
distance_ship = 0
rocket_mass = 1000
dt = .001 #yr
k = 1


'''
Initializing earth and alpha centari.
'''
earth = sphere(radius = earth_radius, color = color.green, pos = vec(0,0,0))
alpha = sphere(radius = alpha_radius, color = color.red)
alpha.pos = vec(alpha_distance + earth.radius + alpha.radius,0,0)

'''
Initialzing rocket and compounding it. Also setting the distance when the force is reversed.
'''
rocket_rod = cylinder(radius = .1, pos = vec(0,0,0), axis = vec(rocket_length/2,0,0))
rocket_tip = cone(pos = vec(rocket_rod.axis.x,0,0), axis = vec(rocket_length/2,0,0), radius = .1)

# tri = [[0,0],[.3*rocket_rod.axis.x,0],[0,.5*rocket_rod.axis.x],[0,0]]
# tripath = [vec(tri[1][0]/2,rocket_rod.radius,0),vec(tri[1][0]/2,rocket_rod.radius,.1)]
# wing = extrusion(path = tripath, shape = tri)
# Attempts to make wings but they don't allign with the ship.

rocket = compound([rocket_rod, rocket_tip])
rocket.pos = vec(earth.radius,0,0)


middle_distance = rocket.pos.x + (.5 * alpha_distance)

rocket.v = vec(0,0,0)
rocket.momentum = vec(0,0,0)
rocket.mass = rocket_mass

'''
Setting scene.
'''

scene.autoscale = 0
scene.range = 3 * alpha_distance

'''
Main body of the simulation. Goes until it is stopped.
'''

while True:
    rate(100)

    rocket.momentum = rocket.momentum + k * force_lightyr * dt
    rocket.v.x = rocket.momentum.x / sqrt(rocket.mass**2 + (rocket.momentum.x/c_light)**2)
    rocket.pos = rocket.pos + rocket.v * dt
    #updates momentum, velocity, and position of the rocket.

    if k == 1:
        if (rocket.pos.x) >= (middle_distance):
            k = -1
        # Checks to see if placeholder k is 1 and if the position of the rocket reaches the
        # middle distance. If it does, then the place holder k is set to -1 so to have negative force.

    if (rocket.v.x <= 0) and (k == -1):
        break
        # checks to see if the rocket is not moving and the force is being applied backwards.
        # If it is then the simulation is stopped.

    gamma_2 = 1 / sqrt(1 - (rocket.v.x/c_light)**2)
    # Calculates Gamma

    time_earth += dt
    time_ship += dt/gamma_2
    #Updates the time from the earth's and ship's perspective.

    if gamma_2 != 0:
        rocket.axis.x = rocket_length/gamma_2
        #Updates the rocket's length

    print(gamma_2)

    distance_ship += rocket.v.x * dt * gamma_2
    distance_earth += rocket.v.x * dt
    #Updates the distance from the earth's and ship's perspective.

print('done')
print('The distance in light-years the ship traveled from the earth perspective:' + str(distance_earth))
print('The distance in light-years the ship traveled from the ship perspective:' + str(distance_ship))
print('The time in years the ship traveled from the earth perspective:' + str(time_earth))
print('The time in years the ship traveled from the ship perspective:' + str(time_ship))
# Prints the given values.
