#Physics Hw Due Feb 1
'''
P.61:

B)  For the 60-40 quanta distribution, the max number of microstates is about 6.8e114.
By taking half that value the distribution is about 50-50 with a value of aout 3.4e114.

C)  As the ratio of oscillators becomes less even, for example 450-50, the distribution curve becomes more squashed together and the overall
max value of the microstates increases.

P.62: The max value of the total entropy is about 3.2e-21 with a q1 value of about 60. This max value indicates the most likely
distribution of quanta throughout the system.

P.63: The values of q1 and q2 where the intersection occur is again 60 and 40 respectively with a temperature of 160K.
The significance is the fact that thetemperature at the interesection is the equilibrium temperature of the system which
also happens to be the value that maximizes the entropy of the system.

P.64: The value of the springs constants that had the best fit were found to be 4 * 16 = 64 N/m for Al and 5 * 4 = 20 N/m for Pb.

Remarks: Problem 61 did not give a spring constant so I initially chose 16 * 4 based on the spring constant given as 16 and the fact
that you need to multiply by 4.

For the program itself, there is an initialization section. Just make the section noted by the problem number True and the others False,
and the graphs should appear.




'''
from math import *
from matplotlib import *
import matplotlib.pyplot as plt

macros = 2
oscillators = [300,200]
quanta = 100
graph_values = []
quanta_bin = []

'''
Initialize
'''
micro_states = True #P.61
entropy = False #P.62
temp = False #P.63
specific_heat = False #P.64
points = False #P.64 (this is to turn on or off the the points given in the book to match the graphs to.)

hbar = 1.05e-34	# [kg m^2 /s] Planck's reduced constant
kb = 1.38e-23
kAl = 4*16
N_A = 6.022e23	# [mol^-1] Avagadro's number
massAl = (26.98/(N_A*1000.))
delta_E = hbar * sqrt(kAl / massAl)


def microstates(input_quanta, input_oscillators):
    r = input_quanta
    N = input_oscillators + r - 1
    combination = factorial(N) / (factorial(r) * factorial (N-r))
    return combination


if micro_states == True:
    for i in range(quanta+1):
        quanta_bin.append(i)
        micros = []
        for j in oscillators:
            micros.append(microstates(i, j))
            i = quanta - i
        graph_values.append(micros[0] * micros[1])
        #graph_values.append(microstates(i) * microstates(4-i))

    plt.bar(quanta_bin, graph_values)
    plt.show()

elif entropy == True:
    entropys = []
    for i in range(quanta+1):
        quanta_bin.append(i)
        temp_entropy = []
        for j in oscillators:
            temp_entropy.append(kb*log(microstates(i, j)))
            i = quanta - i
        entropys.append(temp_entropy)
    plt.plot(quanta_bin, [x[0] for x in entropys])
    plt.plot(quanta_bin, [x[1] for x in entropys])
    total_entropys = [x[0] + x[1] for x in entropys]
    plt.plot(quanta_bin, total_entropys)
    maxTot_entropy = max(total_entropys)
    plt.plot(total_entropys.index(maxTot_entropy), maxTot_entropy, 'ro')
    plt.axvline(x=total_entropys.index(maxTot_entropy), color = 'r', linestyle = '--')
    plt.show()

elif temp == True:
    entropys = [[],[]]
    for i in range(quanta+1):
        for index, j in enumerate(oscillators):
            entropys[index].append(kb*log(microstates(i, j)))
            i = quanta - i
    temp = [[],[]]
    for i in range(quanta-1):
        quanta_bin.append(i+1)
        temp[0].append(2*delta_E/(entropys[0][i+2] - entropys[0][i]))
        temp[1].append(2*delta_E/(entropys[1][i] - entropys[1][i+2]))
    plt.plot(quanta_bin, [x for x in temp[0]],'r')
    plt.plot(quanta_bin, [x for x in temp[1]],'b')
    plt.show()

elif specific_heat == True:
    atoms = 35
    oscillators = 105
    quanta = 300
    kAl = 16 * 4
    kPb = 5 * 4
    massAl = (26.98/(N_A*1000.))
    massPb = (207.2/(N_A*1000.))
    delta_E_Al = hbar * sqrt(kAl / massAl)
    delta_E_Pb = hbar * sqrt(kPb / massPb)
    entropys = []

    for i in range(quanta+1):
        entropys.append(kb*log(microstates(i, oscillators)))

    temp = [[],[]]
    for i in range(quanta-1):
        temp[0].append(2*delta_E_Al/(entropys[i+2] - entropys[i]))
        temp[1].append(2*delta_E_Pb/(entropys[i+2] - entropys[i]))
    c=[[],[]]
    for t in range(len(temp[0])-2):
        c[0].append(2*delta_E_Al / (35*(temp[0][t+2]-temp[0][t])))
        c[1].append(2*delta_E_Pb / (35*(temp[1][t+2]-temp[1][t])))
    del temp[0][0], temp[0][-1], temp[1][0], temp[1][-1]

    if points == True:
        temp_text = [20, 40, 60, 80, 100, 150, 200, 250, 300, 400]
        cAl_text = [.23, 2.09, 5.77, 9.65, 13.04, 18.52, 21.58, 23.25, 24.32, 25.61]
        cPb_text = [11.01, 19.57, 22.45, 23.69, 24.43, 25.27, 25.87, 26.36, 26.82, 27.45]
        for i in range(len(cAl_text)):
            cAl_text[i] /= N_A
            cPb_text[i] /= N_A
        plt.plot(temp_text, cAl_text,'go')
        plt.plot(temp_text, cPb_text, 'yo')

    plt.plot(temp[0], c[0], 'r')
    plt.plot(temp[1], c[1], 'b')
    plt.axhline(y = 3*kb, color = 'b', linestyle = '--')
    plt.show()
