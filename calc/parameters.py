import numpy as np

import setup.initial_conditions as ic


def magnetization(s):
    return s.sum() / ic.N_CALC ** 2


def energy(s, n):
    E = 0
    for i in range(n):
        for j in range(n):
            E += s[i, j] * (s[i, (j + 1) % n] + s[i, (j - 1) % n] + s[(i + 1) % n, j] + s[(i - 1) % n, j])

    return -E / 2


def converged(s, s_old, n):
    matrix = s.reshape(n, n)
    matrix_old = s_old.reshape(n, n)
    var_e = energy(matrix, n) - energy(matrix_old, n)
    return np.abs(var_e) < ic.PRECISION


def matrix_to_vector_pos(i, j, n):
    return i * n + j


def vector_to_matrix_pos(k, n):
    i = k // n
    j = k % n
    return i, j
