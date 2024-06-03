import numpy as np
from mpmath import ellipk, ellipe
from scipy.optimize import curve_fit

import vol.sim_results as sr
import vol.constants as cts


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


def mag_exp(reduced_T, alpha, beta, gamma):
    return alpha * reduced_T ** (-beta) + gamma


def critical_exponent(m, Tc):
    reduced_T = np.zeros(len(cts.T))
    for i in range(len(cts.T)):
        if cts.T[i] == Tc:
            reduced_T[i] = 0.0001
        else:
            reduced_T[i] = np.abs((cts.T[i] - Tc) / Tc)
    popt, pcov = curve_fit(mag_exp, reduced_T, m)
    perr = np.sqrt(np.diag(pcov))
    return popt[1], perr[1]


def critical_temperature(i):
    max_index = get_max_index(sr.c[i])
    return cts.T[max_index], sr.c[i][max_index]


def energy_onsager(T):
    ch = 1 / np.tanh(2 / T)
    sh = np.sinh(2 / T)
    K = float(ellipk((4 * sh) / (2 * sh + 1) ** 2))
    return -ch * (1 + (2 / np.pi) * (2 * sh) ** (-1 / 2) * K)


def heat_onsager(T):
    T_c = 2 / np.log(1 + np.sqrt(2))
    if T >= T_c:
        return 0

    t1 = (2 / np.pi) * ((2 / T) ** 2)
    t2 = -np.log(1 - (T / T_c))
    t3 = np.log(T_c / 2)
    t4 = 1 + np.pi / 4
    # sh = np.sinh(2 / T)
    # E = float(ellipe((4 * sh) / (2 * sh + 1) ** 2))
    # return (2 / np.pi) * ((2 / T) ** 2) * ((2 * sh) ** (-1 / 2)) * E
    return t1 * (t2 + t3 - t4)


def corr_onsager(T, i):
    sh = np.sinh(2 / T)
    return ((2 * sh) / (2 * sh + 1)) ** (i / 2)


def get_max_index(vector):
    # Obtener el índice del valor máximo en el vector
    max_index = np.argmax(vector)
    return max_index
