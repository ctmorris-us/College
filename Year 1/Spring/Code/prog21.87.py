from vpython import *
'''
Made Jan 18, 2019

Made to model a rotating rod that is acted on by at first a constant then a variable torque.

The process is covered in greater detail below, but a torque is applied to a rod and the angular momentum, angular velocity, and theta
is calculated. The rod is rotated about an object axle by a theta (dtheta). Graphs are made to then model the different parameters vs Time.
The rod is also moved perpindicular to the plane of rotation by a constant force F that is applied on the axle. There is also a part of
the code made to have an adjustable axle that is user adjusted using the mouse which is a little slow and glitchy.

Vpython is a little iffy, the simulation may glitch on the screen but the calculations should run fine. I'm getting fairly large theta values
compared to others, but I can't find out why.
'''
'''
Initializing variables:
Mass of rod, length of rod, radius of rod, length of axle, inertia of the rod, angular momentum, torque, rotational kinetic energy, force.
Change in time, time, the max time of simulation, theta, change in theta.
'''

M = 2
Lrod = 1
R = .1
Laxle = 4 * R
I = (1/12) * M * Lrod ** 2 + (1/4) * M * R**2
L = vec(0,0,0)
torque = vec(0,0,2)
rot_KE = vec(0,0,0)
force = vec(.1,0,0)

deltat = .0001
t = 0
tmax = 7
theta = 0
dtheta = 0
zero_omega = []

'''
Initializing the graphs.
'''

g1 = graph(height = 600, width = 400, title = 'Angular Graph', xtitle = 'Time', xmax = tmax, ymax = 10)
theta_vs_t = gcurve(graph = g1, label = 'Theta vs Time', color = color.red)
omega_vs_t = gcurve(graph = g1, label = 'Omega vs Time', color = color.cyan)

rod = cylinder(pos = vec(-1,0,0), radius = R, color = color.orange, axis = vec(Lrod,0,0), v = vec(0,0,0), mass = M)
axle = cylinder(pos = vec(-1 + Lrod/2,0,-Laxle/2), radius = R/6, color = color.red, axis = vec(0,0,Laxle), v = vec(0,0,0))

'''
Pre-simulation: This allows the user to drag their mouse and move the axle so that the rod can rotate about a different origin. I
modified the given code of the assignment so that the axle wasn't able to be moved past the rod. It can be a little slow but it works as
intended.
'''

print('Drag axle left or right to set start position!')
drag = False
position = vec(0,0,0)
movement = True

def down():
    global drag
    drag = True
    scene.bind('mousemove', move)
    scene.bind('mouseup', up)

def move():
    global drag
    if drag:
        if scene.mouse.pos.x < rod.pos.x:
            axle.pos.x = rod.pos.x
        elif scene.mouse.pos.x > rod.pos.x + rod.axis.x:
            axle.pos.x = rod.pos.x + rod.axis.x
        else:
            axle.pos.x = scene.mouse.pos.x
def up():
    global drag
    global position
    global movement
    if drag:
        position = scene.mouse.pos
        scene.unbind('mousedown', down)
        scene.unbind('mousemove', move)
        scene.unbind('mouseup', up)
        movement = False

scene.bind('mousedown', down)

#Necessary to keep the simulation from going before the mouse is released.
while movement == True:
    continue

'''
Main body of the simulation:
Updates the torque, then L (angular momentum) based on torque. The angular velcity omega is updated from L and interia (I).
The change in theta is found using a scalar found from doting omega and the axis of rotation. The rod is rotated and the position is also updated
using the momentum principle by a force. Theta is updated, everything is graphed, and time is updated.
'''

while t<tmax:
    rate(3000)
    torque.z = 3 * cos(5 * t)
    L = L + torque * deltat
    omega = L/I
    omega_scalar = dot(omega, norm(axle.axis))
    dtheta = omega_scalar * deltat
    rod.rotate(angle = theta, axis = axle.axis, origin = vec(axle.pos.x,0,-.2))
    theta += dtheta

    rod.v = rod.v + force * deltat / rod.mass
    rod.pos = rod.pos + rod.v * deltat
    axle.pos = axle.pos + rod.v * deltat

    theta_vs_t.plot([t,theta])
    omega_vs_t.plot([t,mag(omega)])

    t = t + deltat

print('The final value of theta is {}\n and the final value of the angular speed is {}'.format(theta, mag(omega)))
