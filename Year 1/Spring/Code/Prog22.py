# coding: utf-8

# In[ ]:


from vpython import *
from math import *
from random import *
import numpy as np

#1 setup buttons
#2 place atoms and assign quantities to those atoms
#3 place springs
#4 give some ground state energy (i.e. momentum)
#  even before add quanta, will vibrate b/c momentum will
#  cause pos to change and thus there to be a force.
#5 now link in the quanta information to update momentum
#6 finally, determine the entropy and make some plots

# Constants
N_A = 6.022e23	# [mol^-1] Avagadro's number
hbar = 1.05e-34 	# [kg m^2 /s] Planck's reduced constant
kb = 1.38e-23	# [J/K] Boltzmann constant
l = 5e-10	# length of spring [m]  (separation of atoms)
dt = 1e-14		# [s] Time step
t = 0			# [s] Initial time
N = 3			# number of oscillators in each atom

Al = sphere(color=color.blue, radius=143e-12, pos=vec(-l,0,0), vel = vec(0,0,0))
Pb = sphere(color=color.red, radius=202e-12, pos=vec(l,0,0), vel = vec(0,0,0))

##########################################################################################

# Button 1 - Add one quanta to each atom in a random direction
def click1(evt):
    global Al_dq, Pb_dq
    i = randint(0,2)
    Al_dq[i] = 1
    Pb_dq[i] = 1

# Button 2 - Add 5 Al quanta to each atom in a random direction
def click2(evt):
    global Al_dE, Pb_dE, Al_dq, Pb_dq
    i = randint(0,2)
    Al_dq[i] = 5
    Pb_dq[i] = 3 # This should be the lowest integer energy for Pb above 5Al quanta

##########################################################################################

Al_k = 2*16.	# [N/m] Al effective spring constant
Pb_k = 2*5.	# [N/m] Pb effective spring constant

# Define energy of one quantum and mass of each atom
#  Note that I have assigned the mass as a property of the atom
#  rather than a separate variable (Al.m vs Al_m).  That is a matter
#  of taste/style.  Ideally you'd do one or the other and stick with it
#  instead of mixing.
Al_m = 26.98/(N_A*1000.) #Mass of one Al atom
Al.m = Al_m
Al_dE = hbar * sqrt(Al_k/Al_m)
Pb_m = 207.2/(N_A*1000.)
Pb.m = Pb_m
Pb_dE = hbar * sqrt(Pb_k/Al_m)#Energy of one Pb quantum

spring_radius = .5e-10
Al_spring = []
#e-10
#  y spring at -l in x, start spring distance l from mass
#  N.B.  That is an "ell" and not a "one"
Al_spring.append(helix(pos=vec(-2*l,0,0), axis=vec(l,0,0), radius=spring_radius))
Al_spring.append(helix(pos=vec(0,0,0), axis=vec(-l,0,0), radius=spring_radius))
Al_spring.append(helix(pos=vec(-l,-l,0), axis=vec(0,l,0), radius=spring_radius))
Al_spring.append(helix(pos=vec(-l,l,0), axis=vec(0,-l,0), radius=spring_radius))
Al_spring.append(helix(pos=vec(-l,0,-l), axis=vec(0,0,l), radius=spring_radius))
Al_spring.append(helix(pos=vec(-l,0,l), axis=vec(0,0,-l), radius=spring_radius))

#3 And for the other 5 springs

#3 And for Pb
Pb_spring = []

Pb_spring.append(helix(pos=vec(2*l,0,0), axis=vec(-l,0,0), radius=spring_radius))
Pb_spring.append(helix(pos=vec(0,0,0), axis=vec(l,0,0), radius=spring_radius))
Pb_spring.append(helix(pos=vec(l,l,0), axis=vec(0,-l,0), radius=spring_radius))
Pb_spring.append(helix(pos=vec(l,-l,0), axis=vec(0,l,0), radius=spring_radius))
Pb_spring.append(helix(pos=vec(l,0,l), axis=vec(0,0,-l), radius=spring_radius))
Pb_spring.append(helix(pos=vec(l,0,-l), axis=vec(0,0,l), radius=spring_radius))

Box = []
Box.append(box(pos=vec(-l,0,0), size = vec(2*l,2*l,2*l), opacity = .1, color = color.blue))
Box.append(box(pos=vec(l,0,0), size = vec(2*l,2*l,2*l), opacity = .1, color = color.red))

scene.autoscale = False

# Make buttons
b1 = button(pos=scene.caption_anchor, text='Single Quanta', bind=click1)
b2 = button(pos=scene.caption_anchor, text='5 Al Quanta', bind=click2)  # Button for energy of 5 (Al) quanta

# Initial quanta
Al_quanta = vector(0,0,0) #none in each direction
Al_dq = [0,0,0] #how many to add for this click

Pb_quanta = vector(0,0,0)
Pb_dq = [0,0,0]
# Labels
Al_label = label(pos=vec(-l,1.2*l,0), text='Quanta in Al: '+str(Al_quanta), border=1)
Pb_label = label(pos= vec(l,1.2*l,0), text='Quanta in Pb: '+str(Pb_quanta), border=1)

# Initial energies (ground state)
Al_energy = vec(.5 * Al_dE, .5 * Al_dE, .5 * Al_dE)   #One half of the ground state energy (for each oscillator)
Pb_energy = vec(.5 * Pb_dE, .5 * Pb_dE, .5 * Pb_dE)

Al_dp = Al.m * sqrt(2 * Al_dE / Al.m)
Pb_dp = Pb.m * sqrt(2 * Pb_dE / Pb.m)
# Initial momenta
Al.p = vec(.5 * Al_dp, .5 * Al_dp, .5 * Al_dp)
Pb.p = vec(.5 * Pb_dp, .5 * Pb_dp, .5 * Pb_dp)
#4 and for Pb

# Initialize plot
g1 = graph(width=1000, xmin=1e-21, xmax=.5e-18, ymin=0, ymax=.2e-21, title='Entropy vs. Energy', xtitle='Energy (J)', ytitle='Entropy (J/K)')  #think about what good values for xmin, xmax, ymin, ymax would be
Al_plot = gcurve(graph=g1, color=color.blue)
Pb_plot = gcurve(graph=g1, color=color.red)

while True:
    rate(30)

    # Reset forces to 0
    Al.F = vector(0,0,0)
    Pb.F = vector(0,0,0)

    # Calculate new force on each atom
        #  Determine force from -kx where x is diff b/w new and old position
        #  Remeber that the tethered end of the spring is the side away from the atom
    #  and that there is no force for the spring at its "rest" lenth (l)
    #  You want the total vector force due to all the springs.
    #  This is probably the trickiest step
    for i in range(6):
        if i<2:
            Al.F.x += -1 * Al_k * (Al.pos.x - (-l))
            Pb.F.x += -1 * Pb_k * (Pb.pos.x - l)
        elif i<4:
            Al.F.y += -1 * Al_k * (Al.pos.y)
            Pb.F.y += -1 * Pb_k * (Pb.pos.y)
        elif i<6:
            Al.F.z += -1 * Al_k * (Al.pos.z)
            Pb.F.z += -1 * Pb_k * (Pb.pos.z)

        #4 and for Pb

    # Update momentum of atoms
    Al.p += Al.F * dt
    Pb.p += Pb.F * dt

    # Update position of atoms
    Al.pos += Al.p * dt / Al.m
    Pb.pos += Pb.p * dt / Pb.m

    # Update spring axes (length of springs)
    #   Careful to move the correct end of each spring.n
    for i in range(6):
        Al_spring[i].axis = Al.pos - Al_spring[i].pos
        Pb_spring[i].axis = Pb.pos - Pb_spring[i].pos

    # Check to see if button has been pressed
    if Al_dq != [0,0,0]:
        # Update quanta
        Al_quanta += vec(Al_dq[0],Al_dq[1],Al_dq[2])
        Pb_quanta += vec(Pb_dq[0],Pb_dq[1],Pb_dq[2])

        # To see if step 1 is working.  Can take this out in Step 2
        # Note that this isn't a tally of the total quanta, just
        # an indication of what oscillator the last one was placed

        # Update energy
        Al_energy = Al_dE * Al_quanta
        Pb_energy = Pb_dE * Pb_quanta
        #5 and for Pb

        # Update momentum
        Al.p = Al_dp * Al_quanta
        Pb.p = Pb_dp * Pb_quanta
        #Pb.p = vec(Pb_p, Pb_p, Pb_p)        #5 and for Pb

        # Update labels
        Al_label.text = 'Quanta in Al: '+str(Al_quanta)
        Pb_label.text = 'Quanta in Pb: '+str(Pb_quanta)

        # Calculate number of microstates in each atom
        Al_energy_sum = Al_energy.x + Al_energy.y + Al_energy.z
        Pb_energy_sum = Pb_energy.x + Pb_energy.y + Pb_energy.z

        Al_Omega = combin((3 + Al_energy_sum/Al_dE - 1), (Al_energy_sum/Al_dE)) #think about what "n" and "r" should be.  See Section 12.7
        Pb_Omega = combin((3 + Pb_energy_sum/Pb_dE - 1), (Pb_energy_sum/Pb_dE))

        # Calculate entropy
        Al_S = kb * log(Al_Omega)
        Pb_S = kb * log(Pb_Omega) # For both Al and Pb


        Al_plot.plot(pos=(Al_energy_sum, Al_S))
        Pb_plot.plot(pos=(Pb_energy_sum, Pb_S)) #Now plot entropy vs energy (Note that you can't sum vector components)

        #6 and for Pb

        # Reset dq
        Al_dq = [0,0,0]
        Pb_dq = [0,0,0]
