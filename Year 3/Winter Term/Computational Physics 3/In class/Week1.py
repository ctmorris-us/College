import numpy as np
import matplotlib.pyplot as plt

K = 9.0e9

def potential(x, y, q, xq, yq):
    phi = 0

    q = q.T

    #xq, yq must be 1-D array so that the proper concatenation works
    dx = -xq.T + x
    dy = -yq.T + y

    r = np.concatenate((dx, dy), axis = 1)
    dr = np.linalg.norm(r, axis = 1, keepdims = True)

    phi = np.sum(K*q/dr)

    return phi

def Efield(x, y, q, xq, yq):
    E = -1

    #Need to reshape everything from 1-D to D-1 arrays

    q = q.T

    dx = -xq.T + x
    dy = -yq.T + y

    r = np.concatenate((dx, dy), axis = 1)
    dr = np.linalg.norm(r, axis = 1, keepdims = True)


    E = np.sum(K*q*r/(dr**3), axis = 0)

    return E


R_MAX = 50.0 # limit the radius
PHI_0 = 1e6 # limit the potential
DS = 0.01 # target step size
D_PHI = 1e2 # limit the step


def compute_field_line(xi, yi,		# starting point
                       q, xq, yq,	# charges
                       direction):

    x = [xi]
    y = [yi]

    # Loop until the line is too far from the origin
    # or too close to a charge.

    while abs(potential(xi, yi, q, xq, yq)) < PHI_0 \
        and xi*xi+yi*yi < R_MAX*R_MAX:

        # Compute the field.
        Ex,Ey = Efield(xi, yi, q, xq, yq)
        E = np.sqrt(Ex*Ex + Ey*Ey)

        # Choose the step length and limit the change in potential.

        ds = DS
        if ds > D_PHI/E: ds = D_PHI/E

        # Take a step in the direction (or opposite) of the field.

        xi += direction*ds*Ex/E
        yi += direction*ds*Ey/E

        x.append(xi)
        y.append(yi)

    return x, y


def plotfullfieldlines(q, xq, yq, ntheta):

    number_of_charges = np.size(q)

    for i in range(number_of_charges):
        charge = q[0,i] #Have to use two indices because q is a 1xn array
        r = 1.1 * K * charge / PHI_0

        for n in range(ntheta):
            theta = 2 * np.pi * n / ntheta

            xi = xq[0,i] + r * np.cos(theta)
            yi = yq[0,i] + r * np.sin(theta)

            xfieldline, yfieldline = compute_field_line(xi, yi, q, xq, yq, 1)
            plt.plot(xfieldline, yfieldline, 'k-')

            xfieldline, yfieldline = compute_field_line(xi, yi, q, xq, yq, -1)
            plt.plot(xfieldline, yfieldline, 'k-')

            print('Did theta')

    plt.show()

# q  = np.array([[1.e-6, -1.e-6]])
# xq = np.array([[-1,1]])
# yq = np.array([[0,0]])

q  = np.array([[1.e-6]])
xq = np.array([[0]])
yq = np.array([[0]])

# pot = potential(0, 0, q, xq, yq)
# field = Efield(0, 0 , q, xq, yq)
# xfieldline, yfieldline = compute_field_line(2, 1, q, xq, yq, 1)

plotfullfieldlines(q, xq, yq, 2)
