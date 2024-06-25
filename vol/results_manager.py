import vol.constants as cte

import os
import numpy as np


def correlation_results(xi, eta, path):
    name = "correlation.txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nInformación sobre la longitud de correlación:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nLongitudes utilizadas:\n')
        np.savetxt(f, cte.N, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nEta teorica:\n')
        f.write(str(cte.eta_t) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        np.savetxt(f, eta, fmt='%s +- %s', delimiter=', ', newline='\n',
                   header='\nEtas:\n', comments='',
                   footer='\n----------------------------------------------------------------\n')
        f.write('\nXi:\n')
        for i in range(xi.shape[0]):
            for j in range(xi.shape[1]):
                valor_error = 'N = {}, T = {}: {} +- {}\n'.format(cte.N[i], cte.T[j], xi[i, j, 0], xi[i, j, 1])
                f.write(valor_error)
        f.write('\n----------------------------------------------------------------\n')


def critical_exponent_results(beta, beta_mean, beta_mean_err, path):
    name = "critical_exponent.txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nInformación sobre el exponente crítico:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTamaños utilizados:\n')
        np.savetxt(f, cte.N, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nBeta teorica:\n')
        f.write(str(cte.beta_t) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        np.savetxt(f, beta, fmt='%s +- %s', delimiter=', ', newline='\n',
                   header='\nBetas:\n', comments='',
                   footer='\n----------------------------------------------------------------\n')
        f.write('\nBeta promedio:\n')
        f.write(str(beta_mean) + '+-' + str(beta_mean_err) + '\n')
        f.write('\n----------------------------------------------------------------\n')


def critical_temperature_results(max_T_cv, path):
    name = "critical_temperature.txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nInformación sobre la temperatura crítica:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTamaños utilizados:\n')
        np.savetxt(f, cte.N, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTemperatura de Onsager (teorica):\n')
        f.write(str(cte.T_c_onsager) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTemperaturas críticas:\n')
        np.savetxt(f, max_T_cv[0], fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nCalores especificos maximos:\n')
        np.savetxt(f, max_T_cv[1], fmt='%f')
        f.write('\n----------------------------------------------------------------\n')


def onsager_results(Cv_inf, path):
    name = "onsager.txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nInformación sobre los resultados de Onsager:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTemperaturas utilizadas:\n')
        np.savetxt(f, cte.T, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nCalor especifico de Onsager:\n')
        np.savetxt(f, Cv_inf, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')


def t_results(T, N, s_0, time,
              # mag,
              ene, cv, corr_first, corr_second, path):
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
        # f.write('\n----------------------------------------------------------------\n')
        # f.write('\nMagnetización promedio:\n')
        # f.write(str(mag) + '\n')
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
        f.write(format_time(time) + '\n')
        f.write('\n----------------------------------------------------------------\n')


def n_results(N, s_0, calc_time, graph_time,
              # mag,
              ene, cv, corr_first, corr_second, path):
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
        # f.write('\n----------------------------------------------------------------\n')
        # f.write('\nMagnetizaciónes calculadas:\n')
        # np.savetxt(f, mag, fmt='%f')
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
