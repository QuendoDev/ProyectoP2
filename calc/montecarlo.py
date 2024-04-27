import numpy as np


def step_matrix(s, N, p):
    matrix = s
    for i in range(N ** 2):
        matrix = alg(matrix, N, p)
    return matrix


def step(s, N, p):
    matrix = s.reshape(N, N)
    for i in range(N ** 2):
        matrix = alg(matrix, N, p)
    return matrix.flatten()


def alg(s, N, prob):
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

    # Para sacar la probabilidad p, en vez de calcularla con la formula de arriba, se usa el vector p que se pasa
    # como argumento. Este solo tiene 5 valores, por lo que solo hay que calcular la posicion de i sabiendo que
    # var_E = 4*i - 8.
    i = (var_E + 8) // 4
    p = prob[i]

    # Se genera un numero aleatorio uniforme r entre 0 y 1
    r = np.random.rand()

    # Si r < p, se cambia el valor de s(n,m) a -s(n,m)
    if r < p:
        s[n, m] = -s[n, m]

    return s
