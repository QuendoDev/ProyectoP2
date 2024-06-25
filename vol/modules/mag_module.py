import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from itertools import product
import os

import vol.constants as cts
import vol.algorithms as alg


def magnetization(s, N):
    return np.abs(s.sum()) / N ** 2


def calc_mag(args):
    N, t = args
    mag = np.zeros(cts.CYCLES // cts.STEP)

    time1 = time.time()
    time2 = 0
    time3 = 0
    time4 = 0

    s_0 = np.ones((N, N))
    s = s_0.copy()

    p = np.zeros(5)
    for i in range(5):
        v = 4 * i - 8
        p[i] = np.exp(-v / t)

    for i in range(cts.CYCLES):
        if i % cts.STEP == 0:
            mag[i // cts.STEP] = magnetization(s, N)

        s = alg.montecarlo(s, N, p)

        if i == cts.CYCLES // 4:
            time2 = time.time()
            print(N, t, '25%', str(time2 - time1) + ' s', str(time2 - time1) + ' s')
        elif i == cts.CYCLES // 2:
            time3 = time.time()
            print(N, t, '50%', str(time3 - time1) + ' s', str(time3 - time2) + ' s')
        elif i == cts.CYCLES // 4 * 3:
            time4 = time.time()
            print(N, t, '75%', str(time4 - time1) + ' s', str(time4 - time3) + ' s')

    final_time = time.time() - time1
    print(N, t, '100%', str(final_time) + ' s', str(time.time() - time4) + ' s')
    mag_t = np.mean(mag)
    print(N, t, 'Magnetization:', mag_t)
    np.savetxt(os.path.join('C:/Users/euget/Downloads/Fisica Computacional/P2 - '
                            'Modelo de Ising/Proyecto P2/Resultado/Voluntario/Analisis/Datos',
                            f'mag_{N}_{t}.txt'), mag_t)
    return N, t, mag_t


def main():
    dat_dir = ('C:/Users/euget/Downloads/Fisica Computacional/P2 - Modelo de Ising/Proyecto P2/Resultado/Voluntario/'
               'Analisis/Datos')

    mag_total = np.zeros((len(cts.N), len(cts.T)))

    # Generar los valores de magnetización para N = [16, 32, 64, 128] y para T = np.linspace(1.5, 3.5, 10) con n
    # workers.
    with ProcessPoolExecutor(max_workers=5) as executor:
        results = executor.map(calc_mag,
                               product(cts.N, cts.T))

    # Recoger los resultados y actualizar mag_total.
    for result in results:
        Nr, Tr, mag_tr = result
        mag_total[np.where(cts.N == Nr)[0], np.where(cts.T == Tr)[0]] = mag_tr

    # Guardar los valores de magnetización en un archivo .npy en la carpeta Resultado/Voluntario/Analisis/Datos
    np.save(os.path.join(dat_dir, 'mag.npy'), mag_total)

    # Guardar los valores de magnetización en un archivo .txt en la carpeta Resultado/Voluntario/Analisis/Datos
    np.savetxt(os.path.join(dat_dir, 'mag.txt'), mag_total)


if __name__ == '__main__':
    main()
