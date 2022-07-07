'''
Name: Prog4.py
Date Created: Oct. 22, 2018

This is a simulation modeling a simple harmonic motion with a ball attached to a spring distplaced
a certain distance.

This simulation works by calculating the force of gravity on a sphere connected to the spring that is
displaced a certain intial distance. The force on the ball is calculated by the spring and gravity. The forces
are then used to update the velocity and position of the sphere. The simulation runs for 2 seconds plus
the time it takes to do a full period.

The program was created with vpython to model simple harmonic motionself.

The program is initialized by user inputted masses, spring constants, and intial displacements. An issue with
the program is that the inital length of the spring is not initialized to have a zero inital net force and thus
the spring does not oscillate around the inital length of the spring but a new intial value.

'''


from math import *

'''
Initialization
'''
k = float(input('What is the spring constant (N/m)?'))
mass = float(input('What is the mass of the ball (Kg)?'))
dis0 = float(input('What is initial displacement of the oscillator (m)?'))
# This askes the user to input an inital spring constant, mass, and displacement

from vpython import *

g = vec(0, -9.8, 0) * 1
L = vec(0,4,0)
yceiling = vec(0,1.5,0)
y0 = yceiling-L
dt = .01
t = 0
dis0 = vec(0,dis0,0)
flag = 0
flag_time_1 = 0
flag_time_3 = 0
#Initializes accerlation of gravity, length of spring, the top of the spring, the inital position of the ball
# The inital time, change in time per update, and the flags used to calculate the period.

ceiling = box(pos = yceiling, length = 6, width = 4, height = .2, texture = textures.granite)
scene.autoscale = 0
#Creates the box for the spring and ball and sets the scene

spring1 = helix(pos = yceiling, axis = -L - dis0, radius = .1 * mag(L))
ball1 = sphere(pos = y0 - dis0, radius = .2 * mag(L), mass = mass, velocity = vec(0,0,0))
#Creates the spring and the ball

'''
Main body of the simulation.
'''
while flag != 4:

    rate(1/dt) # Sets the rate
    F = (ball1.mass*g) - (k * (ball1.pos-y0))
    # Calculates the net force on the ball

    ball1.velocity = ball1.velocity + F/ball1.mass * dt
    ball1.pos = ball1.pos + ball1.velocity * dt
    # Updates the velcity and position of the ball

    spring1.axis = vec(0,-1*abs(ball1.pos.y) - ball1.radius ,0)
    # Updates the springs length

    if t > 2:
        if (ball1.velocity.y < 0) and (flag == 0):
            flag = 1
        if (ball1.velocity.y > 0) and (flag == 1):
            flag = 2
            flag_time_1 = t
        if (ball1.velocity.y < 0) and (flag == 2):
            flag = 3
        if (ball1.velocity.y > 0) and (flag == 3):
            flag = 4
            flag_time_3 = t
    #This is used to let the simulation run until t=2 and then measures the time difference between the
    #times when the ball has a positive velocity.

    t = t + dt

P = (2 * pi)/(sqrt(k/mass))
total_time_elasped = flag_time_3 - flag_time_1
#Calculates the theoretical period and measured period.

print('The theoretical period was calculated as {}'.format(P))
print('The period was measured as: {}'.format(total_time_elasped))

#Prints out the measured and theoretical period.
