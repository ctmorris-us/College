'''
Name: prog7.py
Made by: Christopher Morris

The program is a simulation of a general 3-body problem with fictional masses.

Date created: Nov. 12, 2018

The simulation works by taking the three masses and calculating the netforce for each mass.
Each mass is then updated in it's position and velocity. The kinetic energy and potential energy
for each mass is then plotted on two seperate graphs. The program runs for till t=30.

The program was made with Vpython with the purpose to understand the conservation of energy.

The program was set up with the general force equation in mind. Meaning it is assumed all units
are setup and standardized so there's no need for conversions or G.

One major problem with the simulation is that the traditional method for trails was significantly slower
than what it should have been. The commented out areas are what is traditionally done and did not work.
The solution was to set trail_make = True for each sphere. The only problem is that there is a little
spike in one of the trails at the start of the simulation.
'''
from vpython import *

'''
Initializing the scene
'''
scene.range=12
scene.autoscale=0
scene.width=1000
scene.height=1000

'''
Creating star objects with positions, radi, colors, velocities, masses, forces, and potential energy.
'''

star1 = sphere(pos=vec(0,0,0), radius = .1, color = color.red, velocity = vec(-.75,-.5,0),
mass = 1.5,force = vec(0,0,0), u = 0, make_trail=True)
star2 = sphere(pos=vec(1,0,0), radius = .2, color = color.blue, velocity = vec(-.5,.5,0),
mass = .8,force = vec(0,0,0), u = 0, make_trail=True)
star3 = sphere(pos=vec(-10,0,0), radius = .1, color = color.yellow, velocity = vec(3,.1,0),
mass = 1.4,force = vec(0,0,0), u = 0, make_trail=True)

starlist = [star1, star2, star3]

# d = []
# for i in range(len(starlist)):
#     d.append(curve(color = starlist[i].color, pos = starlist[i].pos))
'''
Setting variables for time management and to hold total kinetic and potential energies in.
'''
t = 0
dt = .0001
tmax = 30
length = len(starlist)
K = []
U = []

'''
Creating 2 graphs. One for kinetic energy and one for potential energy.
'''

g1 = graph(xmin=0,xmax=tmax,ymin=-20,ymax=20, title = '<b> Energy vs Time</b>',
xtitle = 'Time', ytitle = 'Energy')
kinetic_graph = gcurve(graph=g1,color=color.red)
potential_graph = gcurve(graph=g1,color=color.blue)
totalenergy_graph = gcurve(graph=g1,color=color.green)



# g2 = graph(xmin=0,xmax=tmax,ymin=-3,ymax=3, title = '<b>Total Potential Energy vs Time</b>',
# xtitle = 'Time', ytitle = 'Potential energy' )
# potential_graph = gcurve(graph=g2,color=color.blue)

'''
Main body of the simulation
'''

while t < tmax:
    K = 0
    U = 0
    #Sets total kinetic and potential energy for zero for the graph

    rate = (500)
    #Sets the rate

    for i in range(length):
        starlist[i].force = vec(0,0,0)
        starlist[i].u = 0
        #Sets the forces and indivual potential energy so each star has it's own.
        for j in range(length):
            if i != j:
                radius = starlist[j].pos-starlist[i].pos
                C = starlist[i].mass * starlist[j].mass / mag(radius)
                starlist[i].force += C * norm(radius) / mag(radius)
                starlist[i].u += -1 * C
        #Finds the netforce and potential energy for each star.
    for i in range(length):
        starlist[i].pos += starlist[i].velocity * dt
        starlist[i].velocity += starlist[i].force * dt / starlist[i].mass
        #updates the position and velocity of each star.
        ###d[i].append(starlist[i].pos) Section of code saved for future testing.

        K += .5 * starlist[i].mass * mag(starlist[i].velocity)**2
        U += .5*starlist[i].u
        #Adds each individual kinetic and potential energy to the total kinetic and potential energy.

    kinetic_graph.plot(pos=(t,K))
    potential_graph.plot(pos=(t,U))
    totalenergy_graph.plot(pos=(t,(K+U)))
    #Adds points to the kinetic and potential energy graphs.

    t += dt
    #Updates time

print('done')

#To indicate when the simulation is done.
