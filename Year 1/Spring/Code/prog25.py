import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')

'''
Recitation 5
Christopher Morris

Date Made: March 13, 2019

Program made to numerically simulate the electric field at a selected observation point for a ring, disk, and capacitor.
The program works by generating a set of spheres each with a portion of the total electric charge, at each sphere the Electric
field is calculated at the observation point and added to the total. Once the certain object is created and the electric field is
measured, then an arrow is made pointing in the direction with a scaled down value of the electric field.

The Cyan balls are the actual spheres created, and the red balls are vpython generated rings.

For the ring, the electric field is made by generating 30 balls along a ring with a preset radius.
For the disk, the electric field is made by generating multiple rings with increasing radi.
For the capacitor, two disks are created of the same radi and are seperated by a user specified distance.

The obersavtion location is specified as (3, 1.1, 0).

The program has to be ran newly each time a new shape is to be created due to the difficulty of deleting objects in V-Python.
'''

from vpython import *
import math as math

#Setting Axis and Scene
scene.width = 800
scene.height = 600
scene.background = color.white
axes = curve(pos = ([(3,0,0), (-4,0,0), (-3,0,0), (-3,-4,0), (-3,4,0), (-3,0,0), (-3,0,-3), (-3,0,3)]), color = color.black)

#Function made that finds the value after E (ex: 5E9 would return 9).
#This is made so that the electric field can be scaled down with the axis of the arrow.
def get_exponential(num):
    if abs(num) > 10:
        n = 0
        while abs(num) > 10:
            num /= 10
            n -= 1
        return n
    if abs(num) < 1:
        n = 0
        while abs(num) < 1:
            num *= 10
            n += 1
        return n

#Function that when called will make a ring of charge with a set observation location, ring postion, ring radius
#Total charge on the ring, and any other electric field already made (this is for the disk and capacitor)
def get_E_Ring(obs_pos, ring_pos, ring_radius, tot_charge, E_residual):
    # one over four pi epsilon not, number of balls, total charge, delta theta, delta charge, radius of ring, and observation location
    k = 9e9
    N = 30
    Q = tot_charge
    dtheta = 2 * pi/N
    dQ = Q/N
    R = ring_radius
    obs = obs_pos
    ri = ring(pos = ring_pos, axis = vec(1,0,0), radius = R, color = color.red, thickness = .05)

    E = vec(0,0,0) + E_residual #Done so that the total electric field is a sum of all electric fields
    for n in range(N):
        # Makes a sphere with dQ charge, finds the vector to the observation location, and calulates the electric field at that obs point.
        rate = (N/10)
        slice = sphere(pos = ri.pos + vec(0,R * sin(n *dtheta),R * cos(n * dtheta)), radius = .1, color = color.cyan)
        r = obs - slice.pos
        dE = k * dQ * norm(r) / mag(r)**2
        E = E + dE
    return E

def get_E_Disk(obs_pos, disk_pos, disk_radius, tot_charge, E_residual):
    # Disk of Radius, delta radius, total charge, observation location, disk position, and residual electric field
    R = disk_radius
    dr = .05
    obs = obs_pos
    disk_pos = disk_pos
    E_residual = E_residual

    r = 0
    #Runs by creating rings with increasing radi so to make a disk of charge.
    #The electric field is summed so to get the total electric field.
    while r<R:
        r += dr
        dQ = tot_charge * (2 * r * dr) / R
        E_residual += get_E_Ring(obs, disk_pos, r, dQ, E_residual)
    return E_residual

def get_E_capacitor(obs_pos, capacitor_pos1, capacitor_radius, s, tot_charge, E_residual):
    # Total charge, distance between capactors, residual charge, capacitor radi, observation location,
    # Position of capacitor 1, and position of capacitor 2.
    Q = tot_charge
    s = s
    E_residual = E_residual
    capacitor_radius = capacitor_radius
    obs = obs_pos
    capacitor_pos1 = capacitor_pos1
    capacitor_pos2 = capacitor_pos1 + vec(s,0,0)

    # Runs by summing the electric fields created by two disks at capacitor 1 and 2 locations.
    E_residual += get_E_Disk(obs, capacitor_pos1, capacitor_radius, Q/2, E_residual)
    E_residual += get_E_Disk(obs, capacitor_pos2, capacitor_radius, -1 * Q/2, E_residual)

    return E_residual

# Function Created that calls the get_E_Ring, and prints the returned E-Field and plots the arrow with the scaled E-Field Value.
def ring_button():
    E_residual = vec(0,0,0)
    ring_pos = vec(-3,0,0)
    ring_radius = 2
    #obs_pos = float(input('Input the observation location: \n')
    obs_pos = vec(3,1.1,0)
    tot_charge = 1e-6

    E = get_E_Ring(obs_pos, ring_pos, ring_radius, tot_charge, E_residual)
    print('The Electric Field of a Ring is:', mag(E))
    scale = get_exponential(mag(E))
    scale = 10 ** scale
    Ea = arrow(pos = obs_pos, axis = vec(E * scale), color = vec(1,.8, 0))

# Function Created that calls the get_E_Disk, and prints the returned E-Field and plots the arrow with the scaled E-Field Value.
def disk_button():
    E_residual = vec(0,0,0)
    disk_pos = vec(-3,0,0)
    disk_radius = 2
    #obs_pos = float(input('Input the observation location: \n')
    obs_pos = vec(3,1.1,0)
    tot_charge = 1e-6
    E = get_E_Disk(obs_pos, disk_pos, disk_radius, tot_charge, E_residual)
    print('The Electric Field of a Disk is:', mag(E))
    scale = get_exponential(mag(E))
    scale = 10 ** scale
    Ea = arrow(pos = obs_pos, axis = vec(E * scale), color = vec(1,.8, 0))

# Function Created that calls the get_E_capacitor, and prints the returned E-Field and plots the arrow with the scaled E-Field Value.
def capacitor_button():
    E_residual = vec(0,0,0)
    capacitor_pos1 = vec(-3,0,0)
    capacitor_radius = 2
    #obs_pos = float(input('Input the observation location: \n')
    obs_pos = vec(3,1.1,0)
    tot_charge = 1e-6
    # Label made to alert user to input s, the distance between the capacitors.
    T = label(pos = vec(3,4,0), text='Go to Terminal\n to input the\n distance between\n capacitors', align='center', color=color.red)
    s = float(input('Input the distance between the capacitors: \n'))
    T.visible = False

    E = get_E_capacitor(obs_pos, capacitor_pos1, capacitor_radius, s, tot_charge, E_residual)
    print('The Electric Field of a Capacitor is:', mag(E))
    scale = get_exponential(mag(E))
    scale = 10 ** scale
    Ea = arrow(pos = obs_pos, axis = vec(E * scale), color = vec(1,.8, 0))

# Buttons that appear and when pressed call each respective function
b1 = button(pos=scene.caption_anchor, text='Electric Field for ring', bind=ring_button)
b2 = button(pos=scene.caption_anchor, text='Electric Field for disk', bind=disk_button)
b3 = button(pos=scene.caption_anchor, text='Electric Field for capacitors', bind=capacitor_button)
