import matplotlib.pyplot as plt
import math

def real_func(x):
    return math.log(math.factorial(x), math.e)

def sterling_approx(x):
    return x*math.log(x, math.e) - x

def head_tails(N, N1):
    return math.factorial(N) / (math.factorial(N1)*math.factorial(N-N1))

error_plot = []
n_plot = []

min_error = .02
n = 10

error = 1

while True:

    error = abs(real_func(n) - sterling_approx(n))/real_func(n)
    error_plot.append(error)
    n_plot.append(n)

    if error < min_error:
        break

    n += 1

plt.plot(n_plot, error_plot)
plt.xlabel('n')
plt.ylabel('Percentage Error')
plt.title('Sterling error as a function of n')
