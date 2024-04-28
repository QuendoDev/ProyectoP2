import vol.constants as cte

import os
import numpy as np


def t_results(T, N, s_0, time, mag, ene, cv, corr_first, corr_second, path):
    name = str(T) + ".txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nInformación sobre la simulación:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTamaño de la red:\n')
        f.write(str(N) + 'x' + str(N) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nConfiguración inicial:\n')
        np.savetxt(f, s_0, fmt='%d')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTemperatura:\n')
        f.write(str(T) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nMagnetización promedio:\n')
        f.write(str(mag) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nEnergia media:\n')
        f.write(str(ene) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nCalor especifico:\n')
        f.write(str(cv) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nFuncion de correlacion para i = ' + str(cte.i[0]) + ':\n')
        f.write(str(corr_first) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nFuncion de correlacion para i = ' + str(cte.i[1]) + ':\n')
        f.write(str(corr_second) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTiempo empleado:\n')
        f.write(format_time(time)+ '\n')
        f.write('\n----------------------------------------------------------------\n')


def n_results(N, s_0, calc_time, graph_time, mag, ene, cv, corr_first, corr_second, path):
    name = "result.txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nInformación sobre la simulación a varias temperaturas:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTamaño de la red:\n')
        f.write(str(N) + 'x' + str(N) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nConfiguración inicial:\n')
        np.savetxt(f, s_0, fmt='%d')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTemperaturas utilizadas:\n')
        np.savetxt(f, cte.T, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nMagnetizaciónes calculadas:\n')
        np.savetxt(f, mag, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nEnergias calculadas:\n')
        np.savetxt(f, ene, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nCalores especificos calculadas:\n')
        np.savetxt(f, cv, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nFunciones de correlacion para i = ' + str(cte.i[0]) + ':\n')
        np.savetxt(f, corr_first, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nFunciones de correlacion para i = ' + str(cte.i[1]) + ':\n')
        np.savetxt(f, corr_second, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTiempo necesario para los calculos:\n')
        f.write(format_time(calc_time) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTiempo necesario para las gráficas:\n')
        f.write(format_time(graph_time) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTiempo total empleado:\n')
        f.write(format_time(calc_time + graph_time) + '\n')
        f.write('\n----------------------------------------------------------------\n')


def format_time(seconds):
    # Dividir los segundos en horas y el resto
    hours, remainder = divmod(seconds, 3600)
    # Dividir el resto en minutos y segundos
    minutes, seconds = divmod(remainder, 60)
    # Devolver el tiempo formateado
    return "{:02} horas {:02} minutos {:02} segundos".format(int(hours), int(minutes), int(seconds))
