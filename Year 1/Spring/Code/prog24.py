
# For Creator
# import sys
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')

'''
Date Finished: Feb 28, 19
Created by: Christopher Morris

Purpose: Made to model the electric field at certain points along a rod with a fixed total charge.
The rod is made by a collection of point charges that equally share the initial fixed charge.
The number of point charges is determined by oberserving the average of the total change in the electric field at each point.
Once the average of the change drops below a set level, the simulation is stopped and the number of particles is noted and
printed.

Features: The total charge is initialized at -60e-9 Coloumbs, and the average value of the total change in the electric field
is set at .005. This means that once the average of the total change in the electric field is equal to or below .005, the
simulation is stopped and the number of particles used to make the rod is stored and printed.

How it works: The program works by initializing a set number of particles that are stupposed to combine to make the length of
the rod. The total charge is divided amoung the particles. Six rings are created along the length of the rod with
points along each ring. The electric field is calculated at each point on each ot the rings by calculating electric field from
the observation location and each particle, and they are added together. The direction of the electric field is used to
plot each arrow. The electric field has to be scaled down so not to be too large.

a) 320 Particles required for the rod such that the average change in the electric field is less than .005

'''

import vpython as vp
import numpy as np


'''
Function defined that finds the electric field at each point and adds each element to a numpy array to be accessed
later in the program.
'''
def plot_electricfield(balls):
    '''
    Initialization of variables
    length of rod, total charge in rod, number of particles that make the rod, charge per particle, empty lists for later,
    scaling factor to scale electric field for arrows, one over four pi epsilon not, max theta for ring, change in theta
    (set so there are 12 points per ring), number of rings, distance between each ring, starting postion of the first ring,
    radius of particle, starting position of particle, radius from particle to observation point.
    '''
    length = 2
    chargeTot = -60e-9
    numParticle = balls
    q_source = chargeTot / numParticle
    particleList = []
    arrowList = []

    sf = 1e-3
    oofpez = 9e9
    thetamax = 2 * (np.pi)
    dtheta = np.pi/6
    # R = 1e-36

    numRing = 6
    ringDist = length / numRing / 2
    ringStart = (-length / 2) + ringDist

    radius = (length / numParticle / 2)
    starting_position = (-length / 2) + radius

    R = radius + 1

    '''
    Main function:
    '''

    Elist = np.array([])
    for i in range(numParticle):
        particleList.append(vp.sphere(pos = vp.vec(0,0,starting_position + (2 * radius * i)), radius = radius, color = vp.color.red))
        # Adds all the particles in the rod to a single list to be accessed.
    for i in range(numRing):
        theta = 0
        while theta < thetamax:
            # For each observation point calculates it's position along a ring extended out in the y-direction
            Etot = vp.vec(0,0,0)
            r_obs = vp.vec(R * np.cos(theta), R * np.sin(theta), (ringStart + (2 * ringDist * i)))
            for particle in particleList:
                # Caculates the electric field for each particle in the particle list for the single observation point
                r = r_obs - particle.pos
                rhat = r / vp.mag(r)
                Etot += (oofpez * q_source / vp.mag(r) ** 2) * rhat
            arrowList.append(vp.arrow(pos = r_obs, color = vp.color.blue, axis = sf * Etot, shaftwidth = 1e-1 / 2))
            # Adds an arrow to the arrow list that is directed in the direction of the scaled down electric field.
            theta += dtheta
            # Done to update the theta so the points are measured in a ring.
            Elist = np.append(Elist, vp.mag(Etot))
            # Numpy array with electric field at each observation point
    return Elist


'''
Program done to find the number of particles needed to effectively model a charged rod.
'''

avg_change = 100 #Place holder
intBalls = 6 #Specified for project
E_IntList = plot_electricfield(intBalls) #initial list of electric fields for 6 balls
final_avg_change = .005 #Value of the average change that when reached will stop the simulation.

while avg_change >= final_avg_change:
    intBalls += 1 #Increases the number of particles
    E_FinList = plot_electricfield(intBalls) #Makes final list with new increased number of particles
    E_change = E_FinList - E_IntList #Calculates the change between each component
    E_IntList = E_FinList # Makes the new list the older list so the change can be calculated again
    avg_change = np.average(E_change) #Finds the average of the change array
plot_electricfield(intBalls)
print('The number of particles to cause a %f change in the electric field was: %d particles' % (final_avg_change, intBalls))
