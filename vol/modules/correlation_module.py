import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from itertools import product
import os

import vol.constants as cts
import vol.algorithms as alg
import vol.sim_results as sr


def sum_correlation(s, i, N):
    s_plus_i = 0
    for n in range(N):
        for m in range(N):
            s_plus_i += s[n, m] * s[(n + i) % N, m]
    return s_plus_i


def calc_corr(args):
    N, T = args
    s_plus_i_first = np.zeros(cts.DIV)
    s_plus_i_second = np.zeros(cts.DIV)

    s = np.ones((N, N))
    s_0 = s.copy()

    start_t = time.time()

    time_25 = 0
    time_50 = 0
    time_75 = 0

    p = np.zeros(5)
    for i in range(5):
        v = 4 * i - 8
        p[i] = np.exp(-v / T)

    for i in range(cts.CYCLES):
        if i % cts.STEP == 0:
            s_plus_i_first[i // cts.STEP] = sum_correlation(s, 5, N)
            s_plus_i_second[i // cts.STEP] = sum_correlation(s, 7, N)

        s = alg.montecarlo(s, N, p)

        if i == cts.CYCLES // 4:
            time_25 = time.time()
            print('25%', '--', str(time_25 - start_t) + ' s', str(time_25 - start_t) + ' s')
        elif i == cts.CYCLES // 2:
            time_50 = time.time()
            print('50%', '--', str(time_50 - start_t) + ' s', str(time_50 - time_25) + ' s')
        elif i == cts.CYCLES // 4 * 3:
            time_75 = time.time()
            print('75%', '--', str(time_75 - start_t) + ' s', str(time_75 - time_50) + ' s')

    finish_t = time.time()
    print(f'Tiempo para calculos de T = {T}: {finish_t - start_t} s')
    corr1 = np.mean(s_plus_i_first) / N ** 2
    corr2 = np.mean(s_plus_i_second) / N ** 2
    print(N, T, 'f(5):', corr1)
    print(N, T, 'f(7):', corr2)
    np.savetxt(os.path.join('C:/Users/euget/Downloads/Fisica Computacional/P2 - '
                            'Modelo de Ising/Proyecto P2/Resultado/Voluntario/Analisis/Datos',
                            f'corr_{N}_{T}.txt'), [corr1, corr2])
    return N, T, corr1, corr2


def main():
    dat_dir = ('C:/Users/euget/Downloads/Fisica Computacional/P2 - Modelo de Ising/Proyecto P2/Resultado/Voluntario/'
               'Analisis/Datos')

    corr_total = np.zeros((len(cts.N), 4, len(cts.T)))

    corr_total[0, 0] = sr.fcorr0[0]
    corr_total[1, 0] = sr.fcorr0[1]
    corr_total[2, 0] = sr.fcorr0[2]
    corr_total[3, 0] = sr.fcorr0[3]

    corr_total[0, 1] = sr.fcorr1[0]
    corr_total[1, 1] = sr.fcorr1[1]
    corr_total[2, 1] = sr.fcorr1[2]
    corr_total[3, 1] = sr.fcorr1[3]

    # Generar los valores de correlación para N = [16, 32, 64, 128] y para T = np.linspace(1.5, 3.5, 10) con n workers.
    with ProcessPoolExecutor(max_workers=10) as executor:
        results = executor.map(calc_corr,
                               product(cts.N, cts.T))

    # Recoger los resultados y actualizar corr_total.
    for result in results:
        Nr, Tr, corr1r, corr2r = result
        corr_total[np.where(cts.N == Nr)[0], 2, np.where(cts.T == Tr)[0]] = corr1r
        corr_total[np.where(cts.N == Nr)[0], 3, np.where(cts.T == Tr)[0]] = corr2r

    # Guardar los valores de correlación en un archivo .npy en la carpeta Resultado/Voluntario/Analisis/Datos
    np.save(os.path.join(dat_dir, 'corr.npy'), corr_total)

    # Guardar los valores de correlación en un archivo .txt en la carpeta Resultado/Voluntario/Analisis/Datos
    np.savetxt(os.path.join(dat_dir, 'corr.txt'), corr_total)


if __name__ == '__main__':
    main()
