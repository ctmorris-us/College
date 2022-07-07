
"""
Computational Physics 3 HW 2
Problem 1
Christopher Morris

The code differs from what was provided in class, however when used with the inclass examples it results in the same values.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

Nlist = [int(1e2), int(1e4), int(1e6)]
seed = 42
np.random.seed(seed)

def density(x,y,z):
    return np.exp(-x*y*z)

def volume_per_point(x,y,z):
    return x / x

for N in Nlist:
    m_accum = 0
    msq_accum = 0

    vol_accum = 0
    volsq_accum = 0

    Volume = 8 #The shape is defined inside a square block from -1 to 1 (look at x = np.random.uniform(-1,1))

    x = np.random.uniform(-1,1,int(N))
    y = np.random.uniform(-1,1,int(N))
    z = np.random.uniform(-1,1,int(N))

    xgood = x[(x**2 + y**2 + z**2 < 1) & (x + y + z < .5) & (x + y + 2*z > 0)]
    ygood = y[(x**2 + y**2 + z**2 < 1) & (x + y + z < .5) & (x + y + 2*z > 0)]
    zgood = z[(x**2 + y**2 + z**2 < 1) & (x + y + z < .5) & (x + y + 2*z > 0)]

    m_accum     = density(xgood, ygood, zgood)
    msq_accum   = density(xgood, ygood, zgood)**2
    vol_accum   = volume_per_point(xgood, ygood, zgood)
    volsq_accum = volume_per_point(xgood, ygood, zgood)**2

    mavg     = np.sum(m_accum)/N
    msqavg   = np.sum(msq_accum)/N
    volavg   = np.sum(vol_accum)/N
    volsqavg = np.sum(volsq_accum)/N

    m       = mavg * Volume
    m_std   = np.sqrt((msqavg - mavg**2)/N) * Volume
    vol     = volavg * Volume
    vol_std = np.sqrt((volsqavg - volavg**2)/N) * Volume

    print('For N = {:E} Mass: {:.7f} and Mass Error: {:.7f}'.format(N,m, m_std))
    print('For N = {:E} Volume: {:.7f} and Volume Error: {:.7f}\n'.format(N,vol, vol_std))

fig = plt.figure(figsize = (24,8))
# ax = plt.axes(projection='3d')
# ax.scatter3D(xgood, ygood, zgood);
plt.subplot(1,3,1)
plt.plot(xgood, ygood, 'b.', markersize=0.5)
plt.xlabel('x')
plt.ylabel('y')
plt.subplot(1,3,2)
plt.plot(ygood, zgood, 'b.', markersize=0.5)
plt.xlabel('y')
plt.ylabel('z')
plt.subplot(1,3,3)
plt.plot(xgood, zgood, 'b.', markersize=0.5)
plt.xlabel('x')
plt.ylabel('z')

plt.show()
