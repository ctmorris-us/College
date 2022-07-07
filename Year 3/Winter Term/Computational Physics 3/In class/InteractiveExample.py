#!/usr/bin/env python

import sys
from math import sqrt
import matplotlib.pyplot as plt

K = 9.0e9
PHI_0 = 1.e6
D_PHI = 1.e2
DS = 0.01
R_MAX = 50

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

def compute_field_line(xi, yi, q, xq, yq, direction):

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

import numpy as np

def setup_charges():

    # Use numpy arrays so we can use xq[(q>=0)] syntax below.
    q  = np.array([[1.e-6, -1.e-6]])
    xq = np.array([[-1,1]])
    yq = np.array([[0,0]])

    return q, xq, yq

def plot_field_line(xi, yi, q, xq, yq):

    xplot,yplot = compute_field_line(xi, yi, q, xq, yq, +1)
    plt.plot(xplot, yplot, 'm-', label='$+$', zorder=1)

    xplot,yplot = compute_field_line(xi, yi, q, xq, yq, -1)
    plt.plot(xplot, yplot, 'c-', label='$-$', zorder=1)

class click_to_call:
    def __init__(self, fig, q, xq, yq, func):
        self.fig = fig
        self.q = q
        self.xq = xq
        self.yq = yq
        self.func = func
        self.cid = fig.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes is not None:
            print('start:', event.xdata, event.ydata)
            self.func(event.xdata, event.ydata, self.q, self.xq, self.yq)
            self.fig.canvas.draw()

if __name__ == "__main__" :

    q, xq, yq = setup_charges()

    # Set up the graphics.

    fig = plt.figure()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('field lines')
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.axes().set_aspect('equal')

    # Show the charges and the starting point.

    plt.scatter(xq[(q>=0)], yq[(q>=0)], c='r', s=10, zorder=2)
    plt.scatter(xq[(q<0)], yq[(q<0)], c='b', s=10, zorder=2)

    # Plot field lines selected by mouse click.

    click_to_call(fig, q, xq, yq, plot_field_line)

    plt.show()
