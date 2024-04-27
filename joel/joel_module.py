# Modulo para ejecutar en el supercomputador de la UGR para calcular los datos de magnetizacion promedio
# y poder cargarlos posteriormente en el programa para plotearlos.
import numpy as np
import time

# from numba import njit, prange

T_2 = np.linspace(0.5, 5, 10)
N_CALC = 8
CYCLES = 1000000
STEP = 100


def magnetization(sp):
    return np.abs(sp.sum()) / N_CALC ** 2


def energy(sp, n):
    E = 0
    for v in range(n):
        for j in range(n):
            E += sp[v, j] * (sp[v, (j + 1) % n] + sp[v, (j - 1) % n] + sp[(v + 1) % n, j] + sp[(v - 1) % n, j])

    return -E / 2


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


# @njit(parallel=True)
def func():
    time0 = time.time()
    mag = np.zeros(len(T_2))
    s_0 = np.random.choice([-1, 1], (N_CALC, N_CALC))
    for k in range(len(T_2)):

        time1 = time.time()
        time2 = 0
        time3 = 0
        time4 = 0

        t = T_2[k]
        Z = 0
        mag_prom = 0
        beta = 1 / t

        s = s_0.copy()

        p = np.zeros(5)
        for i in range(5):
            v = 4 * i - 8
            p[i] = np.exp(-v / t)

        for i in range(CYCLES):
            if i % STEP == 0:
                magnetization1 = magnetization(s)
                energy1 = energy(s, N_CALC)
                param = np.exp(-beta * energy1)
                Z += param
                mag_prom += param * magnetization1

            s = step(s.flatten().copy(), N_CALC, p).reshape(N_CALC, N_CALC)

            if i == CYCLES // 4:
                time2 = time.time()
                print(t, '25%', str(time2 - time1) + ' s', str(time2 - time1) + ' s')
            elif i == CYCLES // 2:
                time3 = time.time()
                print(t, '50%', str(time3 - time1) + ' s', str(time3 - time2) + ' s')
            elif i == CYCLES // 4 * 3:
                time4 = time.time()
                print(t, '75%', str(time4 - time1) + ' s', str(time4 - time3) + ' s')

        final_time = time.time() - time1
        print(t, '100%', str(final_time) + ' s', str(time.time() - time4) + ' s')
        mag_t = mag_prom / Z
        mag[k] = mag_t

    print('Total time: ', time.time() - time0)
    np.save('mag', mag)


func()
