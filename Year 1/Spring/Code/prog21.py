# Initializing Graphs
'''
Preamble
'''
from vpython import *

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

g1 = graph(height = 600, width = 400, title = 'Angular Graph', xtitle = 'Time', xmax = tmax, ymax = 10)
theta_vs_t = gcurve(graph = g1, label = 'Theta vs Time', color = color.red)
omega_vs_t = gcurve(graph = g1, label = 'Omega vs Time', color = color.cyan)
rot_KE_vs_t = gcurve(graph = g1, label = 'Rotational Kinetic Energy vs time', color = color.magenta)
torque_vs_t = gcurve(graph = g1, label = 'Torque vs Time', color = color.purple)

rod = cylinder(pos = vec(-1,0,0), radius = R, color = color.orange, axis = vec(Lrod,0,0), v = vec(0,0,0), mass = M)
axle = cylinder(pos = vec(-1 + Lrod/2,0,-Laxle/2), radius = R/6, color = color.red, axis = vec(0,0,Laxle), v = vec(0,0,0))

print('Drag axle left or right to start')
drag = False
wait = True
position = vec(0,0,0)

def down(evt):
    scene.bind('mousemove', move)
    scene.bind('mouseup', up)


def move(evt):
    global drag
    drag = True

    axle.pos.x = scene.mouse.pos.x
    if scene.mouse.pos.x < -2*Laxle:
        rod.pos.x = -2*Laxle
    elif scene.mouse.pos.x > 2*Laxle:
        rod.pos.x = 2*Laxle
    else:
        rod.pos.x = scene.mouse.pos.x

def up(evt):
    global drag
    if drag:
        scene.unbind('mousdown', down)
        scene.unbind('mousemove', move)
        scene.unbind('mouseup', up)
    drag = False

# scene.bind('keydown', key_down)
scene.bind('mousedown', down)

while True:
    if drag == True:
        break
    continue

while True:
    if drag == False:
        break
    continue

while t<tmax:
    rate(50)
    torque.z = 3 * cos(5 * t)
    L = L + torque * deltat
    omega = L/I
    omega_scalar = dot(omega, norm(axle.axis))
    dtheta = omega_scalar * deltat
    rod.rotate(angle = theta, axis = axle.axis, origin = axle.pos)
    theta += dtheta
    rot_KE = (.5) * I * omega.dot(omega)

    rod.v = rod.v + force * deltat / rod.mass
    rod.pos = rod.pos + rod.v * deltat
    axle.pos = axle.pos + rod.v * deltat


    theta_vs_t.plot([t,theta])
    omega_vs_t.plot([t,mag(omega)])
    rot_KE_vs_t.plot([t, rot_KE])
    torque_vs_t.plot([t, mag(torque)])


    t = t + deltat

print('The final value of theta is {}\n and the final value of the angular speed is {}'.format(theta, mag(omega)))
