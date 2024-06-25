import numpy as np
from scipy.optimize import curve_fit

import vol.constants as cts
import vol.sim_results as sr


def corr_exp_func(long, A, eta):
    return A * long ** (-eta)


def corr_exp(corr):
    lengths = np.array([1, 3, 5, 7])
    popt, pcov = curve_fit(corr_exp_func, lengths, corr)
    perr = np.sqrt(np.diag(pcov))
    return popt[1], perr[1]


def corr_long_exp(long, A, xi):
    return A * np.exp(-long / xi)


def corr_length(corr):
    lengths = np.array([1, 3, 5, 7])
    popt, pcov = curve_fit(corr_long_exp, lengths, corr)
    perr = np.sqrt(np.diag(pcov))
    return popt[1], perr[1]


def mag_exp(reduced_T, beta):
    return beta * np.log(reduced_T)


def critical_exponent(m, Tc):
    mask = cts.T < Tc
    filtered_temperatures = cts.T[mask]
    filtered_magnetizations = m[mask]

    reduced_T = Tc - filtered_temperatures

    mag = np.log(filtered_magnetizations)
    popt, pcov = curve_fit(mag_exp, reduced_T, mag)
    perr = np.sqrt(np.diag(pcov))

    return popt[0], perr[0]


def critical_temperature(i):
    max_index = get_max_index(sr.c[i])
    return cts.T[max_index], sr.c[i][max_index]


def heat_onsager(T):
    T_c = 2 / np.log(1 + np.sqrt(2))
    if T >= T_c:
        return 0

    t1 = (2 / np.pi) * ((2 / T) ** 2)
    t2 = -np.log(1 - (T / T_c))
    t3 = np.log(T_c / 2)
    t4 = 1 + np.pi / 4

    return t1 * (t2 + t3 - t4)


def get_max_index(vector):
    # Obtener el índice del valor máximo en el vector
    max_index = np.argmax(vector)
    return max_index
