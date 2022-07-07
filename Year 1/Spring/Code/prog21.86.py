'''
Made Jan 18, 2019

Made to model a rotating rod that is acted on by at first a constant then a variable torque.

The process is covered in greater detail below, but a torque is applied to a rod and the angular momentum, angular velocity, and theta
is calculated. The rod is rotated about an object axle by a theta (dtheta). Graphs are made to then model the different parameters vs Time.

Vpython is a little iffy, the simulation may glitch on the screen but the calculations should run fine. I'm getting fairly large theta values
compared to others, but I can't find out why.

a)
For tmax = 5
The final value of theta is 145.63398058259966
and the final value of the angular speed is 58.25242718448566
0.3999920001599246

For tmax = 4
The final value of theta is 93.20621359227523
and the final value of the angular speed is 46.60194174761961
0.4999875003127678

For tmax = 3
The final value of theta is 52.428932038842675
and the final value of the angular speed is 34.95145631070182
0.6666444451854859

For tmax = 2
The final value of theta is 23.304466135920133
and the final value of the angular speed is 23.302135922327725
0.9999000099989925

The values of the ratio should be constant because omega will increase proportional to theta.
My values of of the ration of mag(omega) vs theta was not constant.

b) The graph of omega vs time should increase exponentially because an increase in omega will lead to a greater increase in omega.
The graph of theta vs time should also be exponential as omega increases so should the change in theta.

c) Period of theta vs time is 1.26. 2 * pi / period = 4.98. Yes the period is consistent with the frequency discounting for error.

d) No. The graphs are in reverse. As the torque increases the rotational kinetic energy decreases. In fact, the max and mins of torque vs Time
and theta vs time are in reverse.
'''

from vpython import *

'''
Initializing variables:
Mass of rod, length of rod, radius of rod, length of axle, inertia of the rod, angular momentum, torque, rotational kinetic energy.
Change in time, time, the max time of simulation, theta, change in theta.
'''

M = 2
Lrod = 1
R = .1
Laxle = 4 * R
I = (1/12) * M * Lrod ** 2 + (1/4) * M * R**2
L = vec(0,0,0)
torque = vec(0,0,0)
rot_KE = vec(0,0,0)

deltat = .0001
t = 0
tmax = 2
theta = 0
dtheta = 0
#zero_omega = []

'''
Initializing the graphs.
'''

g1 = graph(height = 600, width = 400, title = 'Angular Graph', xtitle = 'Time', xmax = tmax, ymax = 10)
theta_vs_t = gcurve(graph = g1, label = 'Theta vs Time', color = color.red)
omega_vs_t = gcurve(graph = g1, label = 'Omega vs Time', color = color.cyan)
rot_KE_vs_t = gcurve(graph = g1, label = 'Rotational Kinetic Energy vs time', color = color.magenta)
torque_vs_t = gcurve(graph = g1, label = 'Torque vs Time', color = color.purple)

rod = cylinder(pos = vec(-1,0,0), radius = R, color = color.orange, axis = vec(Lrod,0,0), v = vec(0,0,0), mass = M)
axle = cylinder(pos = vec(-1 + Lrod/2,0,-Laxle/2), radius = R/6, color = color.red, axis = vec(0,0,Laxle), v = vec(0,0,0))

'''
Main body of the simulation:
Updates the torque, then L (angular momentum) based on torque. The angular velcity omega is updated from L and interia (I).
The change in theta is found using a scalar found from doting omega and the axis of rotation. The rod is rotated.
Theta and rotational kinetic energy are updated, everything is graphed, and time is updated.
'''

while t<tmax:
    rate(10000)
    #Updaing the parameters.
    torque.z = 3 * cos(5 * t)
    L = L + torque * deltat
    omega = L/I
    omega_scalar = dot(omega, norm(axle.axis))
    dtheta = omega_scalar * deltat
    rod.rotate(angle = theta, axis = axle.axis, origin = axle.pos)
    theta += dtheta
    rot_KE = (.5) * I * omega.dot(omega)
    #Updating Graphs
    theta_vs_t.plot([t,theta])
    omega_vs_t.plot([t,mag(omega)])
    rot_KE_vs_t.plot([t, rot_KE])
    torque_vs_t.plot([t, mag(torque)])


    t = t + deltat

print('The final value of theta is {}\n and the final value of the angular speed is {}'.format(theta, mag(omega)))
print(mag(omega) / theta)
