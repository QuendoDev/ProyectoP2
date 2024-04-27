import numpy as np


def magnetization(s, N):
    return np.abs(s.sum()) / N ** 2


def energy(s, n):
    E = 0
    for i in range(n):
        for j in range(n):
            E += s[i, j] * (s[i, (j + 1) % n] + s[i, (j - 1) % n] + s[(i + 1) % n, j] + s[(i - 1) % n, j])

    return -E / 2


def sum_correlation(s, i, N):
    s_plus_i = 0
    for n in range(N):
        for m in range(N):
            s_plus_i += s[n, m] * s[(n + i) % N, m]
    return s_plus_i
