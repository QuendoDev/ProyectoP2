import numpy as np

"""
montecarlo function
This function is used to generate a configuration of the Ising model using the Monte Carlo method.

Parameters
----------
s : numpy array
    Initial configuration of the system.
N : int
    Size of the system.
p : numpy array
    Probability vector used in the Metropolis algorithm.
    
Returns
-------
numpy array
    Final configuration of the system.
"""


def montecarlo(s, N, p):
    matrix = s

    # Iterate over all the spins in the system.
    for i in range(N ** 2):
        matrix = metropolis(matrix, N, p)

    return matrix


"""
metropolis function
This function generates typical configurations of the Ising model using the Metropolis algorithm. It has a little 
optimization, as it uses a probability vector p that is passed as an argument, instead of calculating the probability
using the formula, so it makes less calculations.

Parameters
----------
s : numpy array
    Initial configuration of the system.
N : int
    Size of the system.
prob : numpy array
    Probability vector used in the Metropolis algorithm.
    
Returns
-------
numpy array
    Final configuration of the system.
"""


def metropolis(s, N, prob):
    # Se elige un punto aleatorio (n,m) de la red
    n = np.random.randint(0, N)
    m = np.random.randint(0, N)

    # Calculates var(E) = 2s(n,m)[s(n+1,m)+s(n-1,m)+s(n,m+1)+s(n,m-1)] using periodic boundary conditions:
    # s(0, j) = s(N, j), s(i, 0) = s(i, N), s(N+1, j) = s(1, j), s(i, N+1) = s(i, 1) with s(n,m) being the value of
    # the system at point (n,m).
    var_E = 2 * s[n, m] * (s[(n + 1) % N, m] + s[(n - 1) % N, m] + s[n, (m + 1) % N] + s[n, (m - 1) % N])

    # For getting the probability p, instead of calculating it with the usual formula, the probability vector p is
    # used. This vector only has 5 values, so it is only necessary to calculate the position of i knowing that
    # var_E = 4*i - 8.
    i = (var_E + 8) // 4
    p = prob[int(i)]

    # Generates a random number between 0 and 1.
    r = np.random.rand()

    # If the random number is less than the probability p, the spin is flipped.
    if r < p:
        s[n, m] = -s[n, m]

    return s
