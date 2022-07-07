'''
Name: prog2.py

The program is a basic simulation of a ball bouncing off of a solid surface.
Date made: Oct. 7, 2018

The program creates both a box object and sphere object. The sphere is given components of its velocity
as well as its acceleration which is -9.8 m/s^2. The ball is accelerates towards the table and when its
y-position reaches the point where it touches the table it then 'bounces' off the table with a y-velocity
directed away from the table. The sphere follows the process of accelerating towards the table and bouncing
off of the table until it falls of the table ini which the program ends.

The program was created to better understand the abilities of V-Python and to implement our studies of
kinematics into practice.

The program has both an option for elastic and inelastic bouncing and is set to inelastic by default.
The elasticity of the bouncing is changed by a changing the damping factor. A zero damp factor means
perfectly elastic collisions where as anything greater than zero is inelastic collisions. The creator of
the program has found the settings already pre-set have the best effect.
'''
from vpython import *
from math import *

'''
Initialization
'''
# Length, Height, Radius of the circle
L = 20
H = .2
R = .5

# Damp factor, Change in time, max time to reach, starting time = 0, force of gravity, initial velocity, angle
Damp = 2 # If Damp > 0, causes the ball to not bounce elastically. *Damp at 2 is the best*
dt = .01
tmax = 30
t = 0
g = -9.8
v0 = 8
theta = pi/3

# Setting the scene
scene.autoscale = 0
scene.center = vec(L/2, .4 * L, 0)
scene.forward = vec(0,-.2,-.9)
scene.scale = .7 * L

# Creating the Objects: Wood surface, sphere, and trail of the ball.
xaxis = box(pos = vec(L/2, -H/2, 0), length = L, height = H, width = L/3, texture = textures.wood)
ball = sphere(pos = vec(0, R+3, 0), radius = R)
ball.v = vec(v0 * cos(theta), v0 * sin(theta), 0)
ball.a = vec(0, g, 0)
trail = curve(color = color.red)


'''
Working code
'''
while t < tmax:
    rate(1/dt) # Sets rate to make the simulation visible.

    # Updating the time, ball's position and velocity, and the curve.
    t = t + dt
    ball.pos = ball.pos + ball.v*dt
    ball.v = ball.v + ball.a*dt
    trail.append(ball.pos)

    # Checks to see if the ball touches the table. If the ball touches the table then it will bounce up.
    # Also checks to make sure the ball is within the length of the table.
    if (ball.pos.y < ball.radius) & (ball.v.y < 0) & (ball.pos.x < L):
        print(ball.pos.x)
        print('Bounce!')
        ball.v.y = -ball.v.y - Damp # Reverses the velocity making it positive.


    # Checks to see if the ball falls off the table.
    if ball.pos.y < -3:
        print('Ball has fallen off the table.')
        break

print('Now I am done. ')
