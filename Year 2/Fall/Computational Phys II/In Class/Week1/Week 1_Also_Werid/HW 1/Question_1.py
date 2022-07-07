import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')

import math
import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return np.cos(x)

def fp(x):
    return -math.sin(x)

x = 3.0
dx = 0.1

dx_list = []
error1_list = []
error2_list = []

for n in range(1, 50):

    dx = 2**(-n)

    deriv1 = (f(x+dx)-f(x))/dx
    deriv2 = (f(x+dx)-f(x-dx))/(2*dx)

    error1 = abs(deriv1 - fp(x))
    error2 = abs(deriv2 - fp(x))

    dx_list.append(dx)
    error1_list.append(error1)
    error2_list.append(error2)


plt.loglog(dx_list, error1_list, 'r-', label = 'e1')
plt.loglog(dx_list, error2_list, 'b--',label = 'e2')
plt.title('Question 1A')
plt.xlabel('log(dx)')
plt.ylabel('log(error)')
plt.legend()
plt.show()


# print(x, deriv, fp(x), abs(deriv-fp(x)))

dx = np.array([.1, .05, .025])
deriv = (f(x+dx)-f(x-dx))/(2*dx)

p = np.polyfit(dx, deriv, 2)
print('\nQ1 part b)')
print('\np1:', p[0], 'p2:', p[1], 'p3:', p[2])
print('True derivative at dx = 0:', fp(x))
print('Extrapolated derivative from polynomial fitting:', p[2], 'with an error of:', abs(fp(x) - p[2]))
print('The error of dx = .025:', abs(fp(x) - deriv[-1]))


dx = np.array([.1, .05, .025, .0125])
deriv = (f(x+dx)-f(x-dx))/(2*dx)

p = np.polyfit(dx, deriv, 3)
print('\nQ1 part c)')
print('\np1:', p[0], 'p2:', p[1], 'p3:', p[2],'p4:', p[3], '\n')
print('True derivative at dx = 0:', fp(x))
print('Extrapolated derivative from polynomial fitting:', p[3], 'with an error of:', abs(fp(x) - p[3]))
