import numpy as np
from scipy.optimize import curve_fit

import vol.setup.constants as cts
import vol.old.sim_results as sr

"""
corr_exp_func function
Function that models the correlation function as a power law with an exponential correction term.

Parameters
----------
long : float
    The distance between two spins.
A : float
    The amplitude of the power law term.
eta : float
    The exponent of the power law term.
C : float
    The amplitude of the exponential correction term.
    
Returns
-------
float
    The value of the correlation function at the given distance.
"""


def corr_exp_func(long, A, eta, C):
    return A * long ** (-eta) + C


"""
corr_exp function
Function that fits the correlation function to the corr_exp_func function. Used to extract from the data the critical
exponent of the correlation function.

Parameters
----------
corr : numpy array
    The correlation function at different distances.
    
Returns
-------
float
    The critical exponent of the correlation function.
float
    The error of the critical exponent of the correlation function.
"""


def corr_exp(corr):
    lengths = cts.i.copy()
    popt, p_cov = curve_fit(corr_exp_func, lengths, corr)
    p_err = np.sqrt(np.diag(p_cov))
    return popt[1], p_err[1]


"""
corr_long_exp function
Function that models the correlation function as an exponential decay.

Parameters
----------
long : float
    The distance between two spins.
A : float
    The amplitude of the exponential decay term.
xi : float
    The correlation length.
    
Returns
-------
float
    The value of the correlation function at the given distance.
"""


def corr_long_exp(long, A, xi):
    return A * np.exp(-long / xi)


"""
corr_length function
Function that fits the correlation function to the corr_long_exp function. Used to extract from the data the correlation
length of the system for a given temperature and lattice size.

Parameters
----------
corr : numpy array
    The correlation function at different distances.
    
Returns
-------
float
    The correlation length of the system.
float
    The error of the correlation length of the system.
"""


def corr_length(corr):
    lengths = cts.i.copy()
    popt, pcov = curve_fit(corr_long_exp, lengths, corr)
    perr = np.sqrt(np.diag(pcov))
    return popt[1], perr[1]


"""
mag_exp function
Function that models the magnetization as a power law with an exponential correction term. It is linearized to fit the
data.

Parameters
----------
reduced_T : float
    The reduced temperature.
beta : float
    The critical exponent of the magnetization.
    
Returns
-------
float
    The value of the magnetization at the given reduced temperature.
"""


def mag_exp(reduced_T, beta):
    return beta * np.log(reduced_T)


"""
critical_exponent function
Function that fits the magnetization to the mag_exp function. Used to extract from the data the critical exponent of the
magnetization. It only fits the data for temperatures below the critical temperature for avoiding the divergence of the
magnetization. The reduced temperature is calculated as the difference between the critical temperature and the 
temperature of the data.

Parameters
----------
m : numpy array
    The magnetization of the system.
Tc : float
    The critical temperature of the system for the given lattice size.
    
Returns
-------
float
    The critical exponent of the magnetization.
float
    The error of the critical exponent of the magnetization.
"""


def critical_exponent(m, Tc):
    # Mask to filter the data for temperatures below the critical temperature.
    mask = cts.T < Tc
    filtered_temperatures = cts.T[mask]
    filtered_magnetization = m[mask]

    # Calculate the reduced temperature.
    reduced_T = Tc - filtered_temperatures

    # Linearize the data.
    mag = np.log(filtered_magnetization)

    # Fit the data.
    popt, p_cov = curve_fit(mag_exp, reduced_T, mag)
    p_err = np.sqrt(np.diag(p_cov))

    return popt[0], p_err[0]


"""
heat_onsager function
Function that calculates the heat capacity of the system using the Onsager solution for the 2D Ising model. For values
of the temperature above the critical temperature, the heat capacity is zero. The heat capacity is calculated using
the following formula: C = (2k / pi) * (2J / kTc) ** 2 * (-ln(1 - T / Tc) + ln(kTc / 2J) - 1 - pi / 4), where k is the
Boltzmann constant, J is the coupling constant, and Tc is the critical temperature. In this case, we rescale the
k to 1 and we set J = 1.

Parameters
----------
T : float
    The temperature of the system.
    
Returns
-------
float
    The heat capacity of the system at the given temperature.
"""


def heat_onsager(T):
    T_c = 2 / np.log(1 + np.sqrt(2))
    if T >= T_c:
        return 0

    t1 = (2 / np.pi) * ((2 / T_c) ** 2)
    t2 = -np.log(1 - (T / T_c))
    t3 = np.log(T_c / 2)
    t4 = 1 + np.pi / 4

    return t1 * (t2 + t3 - t4)


"""
critical_temperature function
Function that gets the critical temperature and the heat capacity at the critical temperature for a given lattice size
from the simulation results.

Parameters
----------
N : int
    The lattice size.
    
Returns
-------
float
    The critical temperature of the system.
float
    The heat capacity at the critical temperature of the system.
"""


def critical_temperature(N):
    max_index = np.argmax(sr.c[N])
    return cts.T[max_index], sr.c[N][max_index]
