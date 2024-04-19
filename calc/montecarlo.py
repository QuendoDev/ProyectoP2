import numpy as np


def step(T, s, N):
    matrix = s.reshape(N, N)
    for i in range(N ** 2):
        matrix = alg(T, matrix, N)
    return matrix.flatten()


def alg(T, s, N):
    # Algoritmo de metropolis para generar configuraciones tipicas con probabilidad de equilibrio
    # T: Temperatura
    # s: Configuracion inicial
    # Devuelve: Configuracion final

    # Inicializacion

    # Se elige un punto aleatorio (n,m) de la red
    n = np.random.randint(0, N)
    m = np.random.randint(0, N)

    # Se evalua p = min(1, exp-[var(E)]/T))
    # donde var(E) = 2s(n,m)[s(n+1,m)+s(n-1,m)+s(n,m+1)+s(n,m-1)]
    # y s(n,m) es el valor de la red en el punto (n,m).
    # Usar las condiciones de contorno periodicas:
    # s(0, j) = s(N, j), s(i, 0) = s(i, N), s(N+1, j) = s(1, j), s(i, N+1) = s(i, 1).

    var_E = 2 * s[n, m] * (s[(n + 1) % N, m] + s[(n - 1) % N, m] + s[n, (m + 1) % N] + s[n, (m - 1) % N])
    p = min(1, np.exp(-var_E / T))

    # Se genera un numero aleatorio uniforme r entre 0 y 1
    r = np.random.rand()

    # Si r < p, se cambia el valor de s(n,m) a -s(n,m)
    if r < p:
        s[n, m] = -s[n, m]

    return s
