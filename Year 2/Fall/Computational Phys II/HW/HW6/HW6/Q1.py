'''
Phys 305
HW 6
Christopher Morris
Q1

'''
# Ignore, needed in order to import scipy on my machine
# import sys
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')

import numpy as np
from scipy.linalg import eig, solve, det, inv
import matplotlib.pyplot as plt



plt.figure(figsize = (6,6))

def g(x):
    return -x**2

a = -6.0
b = 6.0
N = 3500

x = np.linspace(a, b, N+1)
h = (b-a)/N

# Difference matrix A (dimension N-1).

xx = x[1:-1]		# interior points only
A = np.zeros((N-1,N-1))
for n in range(N-1):
    A[n,n] = -2.0 + h**2*g(xx[n])
    if n > 0:
        A[n,n-1] = 1.0
    if n < N-2:
        A[n,n+1] = 1.0

eigenvalues,eigenfunctions = eig(A)
iarr = np.argsort(-eigenvalues)		# list in ascending order

n = 0
print('\n Question 1a Matrix Method')
for i in iarr[:10]:
    psi = np.array([0.])
    psi = np.append(psi, eigenfunctions[:,i])
    psi = np.append(psi, 0.)
    norm = (h*(psi**2).sum())**0.5
    psi /= norm
    if psi.max() <= 0: psi = -psi
    eigi = -np.real(eigenvalues[i])/h**2
    print('Eigenvalue = {} with Error = {}'.format(eigi, 2*n+1 - eigi))
    plt.plot(x, psi, label='E = {:.3f}'.format(eigi))
    n += 1

plt.xlim(a, b)
plt.xlabel('x')
plt.ylabel(r'$\psi$')
plt.legend(loc='right')
plt.title('Question 1a N = '+str(N))
plt.show()

plt.figure(figsize = (6,6))

def g(x):
    return -x**2

def s(x):
    return 0

a = -6.0
b = 6.0
ya = 0.0
yb = 0.0
N = 400

x = np.linspace(a, b, N+1)
h = (b-a)/N

xx = x[1:-1]		# N-1 interior points only: indices n = 0 to N-2

# Difference matrix A (dimension N-1).

A = np.zeros((N-1,N-1))
B = np.zeros((N-1,N-1))

# Right-hand side r.

r = np.zeros(N-1)
r[0] = -ya*(1+h**2*g(a)/12)
r[-1] = -yb*(1+h**2*g(b)/12)

for n in range(N-1):
    A[n,n] = -2.0*(1 - 5*h**2*g(xx[n])/12)
    B[n,n] = 10.0
    if n > 0:
        A[n,n-1] = 1.0 + h**2*g(xx[n-1])/12
        B[n,n-1] = 1.0
    if n < N-2:
        A[n,n+1] = 1.0 + h**2*g(xx[n+1])/12
        B[n,n+1] = 1.0
    r[n] += h**2*(s(x[n+2])+10*s(x[n+1])+s(x[n]))/12	# note use of x here

eigenvalues,eigenfunctions = eig(np.matmul(inv(B),A))
iarr = np.argsort(-eigenvalues)		# list in ascending order

n = 0

print('\n\nQuestion 1b Numerov Method')
for i in iarr[:10]:
    psi = np.array([0.])
    psi = np.append(psi, eigenfunctions[:,i])
    psi = np.append(psi, 0.)
    norm = (h*(psi**2).sum())**0.5
    psi /= norm
    if psi.max() <= 0: psi = -psi
    eigi = -np.real(eigenvalues[i])/h**2 * 12
    print('Eigenvalue = {} with Error = {}'.format(eigi, 2*n+1 - eigi))
    plt.plot(x, psi, label='E = {:.3f}'.format(eigi))
    n += 1

plt.xlim(a, b)
plt.xlabel('x')
plt.ylabel(r'$\psi$')
plt.legend(loc='right')
plt.title('Q1b, Numerov Method N = '+str(N))
plt.show()
