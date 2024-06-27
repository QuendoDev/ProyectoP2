import numpy as np

"""
magnetization function
This function calculates the magnetization of the system, given the spin configuration and the size of the system.

Parameters
-----------
s: numpy array
    The spin configuration of the system.
N: int
    The size of the system.
    
Returns
--------
float
    The magnetization of the system.
"""


def magnetization(s, N):
    return np.abs(s.sum()) / N ** 2


"""
energy function
This function calculates the energy of the system, given the spin configuration and the size of the system. It is 
calculated with this formula: E(s) = -1/2 * sum(s_i,j * (s_i+1,j + s_i-1,j + s_i,j+1 + s_i,j-1)) applying periodic
boundary conditions.

Parameters
-----------
s: numpy array
    The spin configuration of the system.
N: int
    The size of the system.
    
Returns
--------
float
    The energy of the system.
"""


def energy(s, n):
    E = 0
    for i in range(n):
        for j in range(n):
            E += s[i, j] * (s[i, (j + 1) % n] + s[i, (j - 1) % n] + s[(i + 1) % n, j] + s[(i - 1) % n, j])

    return -E / 2


"""
sum_correlation function
This function calculates the sum of the correlation between spins separated by a distance i, given the spin
configuration and the size of the system. This is calculated with the formula: sum(s_n,m * s_n+i,m) applying periodic
boundary conditions. This sum will be used to calculate the correlation function.

Parameters
-----------
s: numpy array
    The spin configuration of the system.
i: int
    The distance between the spins.
N: int
    The size of the system.
    
Returns
--------
float
    The sum of the correlation between spins separated by a distance i.
"""


def sum_correlation(s, i, N):
    s_plus_i = 0
    for n in range(N):
        for m in range(N):
            s_plus_i += s[n, m] * s[(n + i) % N, m]
    return s_plus_i
