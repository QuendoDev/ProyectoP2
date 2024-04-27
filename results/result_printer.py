import os
import numpy as np


def ising_results(t, beta, N, mag_prom, Z, s_0, time, path):
    name = "ising_" + str(t) + "_" + str(N) + "x" + str(N) + ".txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nInformación sobre la simulación:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTamaño de la red:\n')
        f.write(str(N) + 'x' + str(N) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTemperatura:\n')
        f.write(str(t) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nConfiguración inicial:\n')
        np.savetxt(f, s_0, fmt='%d')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nBeta utilizada (1/T):\n')
        f.write(str(beta) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nZ calculada:\n')
        f.write(str(Z) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTiempo para calcular el promedio:\n')
        f.write(str(time) + ' s\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nMagnetización promedio:\n')
        f.write(str(mag_prom) + '\n')
        f.write('\n----------------------------------------------------------------\n')


def ising_info(n, t, steps, time, anim_time, s_0, path):
    name = "ising_" + str(t) + "_" + str(n) + "x" + str(n) + ".txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nInformación sobre la simulación:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTamaño de la red:\n')
        f.write(str(n) + 'x' + str(n) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTemperatura:\n')
        f.write(str(t) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nConfiguración inicial:\n')
        np.savetxt(f, s_0.reshape(n, n), fmt='%d')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nNúmero de pasos para llegar al equilibrio:\n')
        f.write(str(steps) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTiempo necesario para llegar al equilibrio:\n')
        f.write(str(time) + ' segundos\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTiempo de animación:\n')
        f.write(str(anim_time) + ' segundos\n')
        f.write('\n----------------------------------------------------------------\n')
