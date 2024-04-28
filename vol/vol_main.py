import os
import time

import matplotlib.pyplot as plt
import numpy as np

import vol.algorithms as alg
import vol.constants as cte
import vol.file_manager as fm
import vol.results_manager as rm
import vol.vol_params as param

# Se quieren calcular una lista de parametros para cada N en [16, 32, 64, 128], representando para cada temperatura
# en [1.5, 3.5] con 10 valores. Los parametros que se quieren calcular son:
# - La magnetizacion promedio
# - La energia media
# - El calor especifico
# - La funcion de correlacion

# Para esto, se genera una configuracion inicial de espines todos ordenadors (s[i, j] = 1 para cualquier i, j), y se
# deja evolucionar el sistema 1000000 ciclos, guardando los resultados cada 100 ciclos. Cada resultado se guarda en una
# posicion del array correspondiente al parametro que se esta calculando y al final del bucle, se le hace la media a ese
# array para obtener el valor promedio de ese parametro. Si hay que hacer algun calculo mas usando escalares o ctes
# al final de la formula para obtener el valor final que se pide, se hace al finalizar el bucle para ahorrar calculos.

# Por ultimo, se guardan los resultados en un archivo de texto con el nombre de los parametros que se han calculado y se
# generan las graficas correspondientes.

# Genero las carpetas de resultados.
result_path = fm.init_files()

# Empiezo un bucle para cada N que hay en la lista de constantes.
for N in cte.N:
    # Imprimo el N para saber en que paso del bucle estoy.
    print(f'Calculando para {N}x{N}')

    # Empiezo a contar el tiempo que tarda en hacer los calculos.
    start_n = time.time()

    # Defino para cada N, y parametros los arrays donde se guardaran los resultados de cada 100 pasos de montecarlo.
    mag = np.zeros(cte.DIV)
    ene = np.zeros(cte.DIV)
    ene_sq = np.zeros(cte.DIV)
    s_plus_i_first = np.zeros(cte.DIV)
    s_plus_i_second = np.zeros(cte.DIV)

    # Defino las matrices que contendran los 10 valores de cada parametro, a representar en las graficas.
    mag_all = np.zeros(len(cte.T))
    ene_all = np.zeros(len(cte.T))
    cv_all = np.zeros(len(cte.T))
    corr_all_first = np.zeros(len(cte.T))
    corr_all_second = np.zeros(len(cte.T))

    # Genero la configuracion inicial.
    s = np.ones((N, N))
    s_0 = s.copy()

    # Empiezo un bucle para cada temperatura en la lista de constantes.
    for k in range(len(cte.T)):
        # Imprimo la temperatura para saber en que paso del bucle estoy.
        print(f'Calculando para T = {cte.T[k]}')

        # Empiezo a contar el tiempo que tarda en hacer los calculos para esta temperatura.
        start_t = time.time()

        # Defino las variables para contabilizar cuando llevo 25%, 50&, 75% y 100% de los calculos para ir printeando el
        # porcentaje.
        time_25 = 0
        time_50 = 0
        time_75 = 0

        # Defino la temperatura a la que se va a trabajar.
        T = cte.T[k]

        # Defino el vector probabilidad relacionado con las posibles variaciones de energia [-8, -4, 0, 4, 8] que se
        # pueden dar en el sistema, y que se usara en el algoritmo de metropolis.
        p = np.zeros(5)
        for i in range(5):
            v = 4 * i - 8
            p[i] = np.exp(-v / T)

        for i in range(cte.CYCLES):
            if i % cte.STEP == 0:
                # Sumo los parametros de este ciclo para hacer la media al final del bucle.
                mag[i // cte.STEP] = param.magnetization(s, N)
                e = param.energy(s, N)
                ene[i // cte.STEP] = e
                ene_sq[i // cte.STEP] = e ** 2
                s_plus_i_first[i // cte.STEP] = param.sum_correlation(s, cte.i[0], N)
                s_plus_i_second[i // cte.STEP] = param.sum_correlation(s, cte.i[1], N)

            # Hago un paso de montecarlo.
            s = alg.montecarlo(s, N, p)

            # Imprimo el porcentaje de calculos que llevo.
            if i == cte.CYCLES // 4:
                time_25 = time.time()
                print('25%', '--', str(time_25 - start_t) + ' s', str(time_25 - start_t) + ' s')
            elif i == cte.CYCLES // 2:
                time_50 = time.time()
                print('50%', '--', str(time_50 - start_t) + ' s', str(time_50 - time_25) + ' s')
            elif i == cte.CYCLES // 4 * 3:
                time_75 = time.time()
                print('75%', '--', str(time_75 - start_t) + ' s', str(time_75 - time_50) + ' s')

        # Calculo los parametros finales para esta temperatura.
        mag_all[k] = np.mean(mag) / N ** 2
        ene_all[k] = np.mean(ene) / (2 * N)
        cv_all[k] = (np.mean(ene_sq) - np.mean(ene) ** 2) / (T * N ** 2)
        corr_all_first[k] = np.mean(s_plus_i_first) / N ** 2
        corr_all_second[k] = np.mean(s_plus_i_second) / N ** 2

        # Imprimo el tiempo que ha tardado en hacer los calculos para esta temperatura.
        finish_t = time.time()
        print(f'Tiempo para calculos de T = {T}: {finish_t - start_t} s')

        # Guardo los resultados en un archivo de texto.
        rm.t_results(T, N,
                     s_0, finish_t - start_t,
                     mag_all[k], ene_all[k], cv_all[k],
                     corr_all_first[k], corr_all_second[k],
                     os.path.join(result_path, str(N) + 'x' + str(N)))

    # Imprimo el tiempo que ha tardado en hacer los calculos para este N.
    finish_calc_n = time.time()
    print(f'Tiempo para calculos de {N}x{N}: {finish_calc_n - start_n} s')

    # Genero las graficas y las guardo en la carpeta de resultados usando subplots y axes para poner las 5 graficas
    # en una misma figura para cada bucle de N.
    fig, axs = plt.subplots(3, 2, figsize=(15, 15))
    fig.suptitle(f'{N}x{N}', fontsize=20)

    # Grafica de la magnetizacion.
    axs[0, 0].plot(cte.T, mag_all)
    axs[0, 0].set_title('Magnetizacion')
    axs[0, 0].set_xlabel('T')
    axs[0, 0].set_ylabel('Magnetizacion')

    # Grafica de la energia.
    axs[0, 1].plot(cte.T, ene_all)
    axs[0, 1].set_title('Energia')
    axs[0, 1].set_xlabel('T')
    axs[0, 1].set_ylabel('Energia')

    # Grafica del calor especifico.
    axs[1, 0].plot(cte.T, cv_all)
    axs[1, 0].set_title('Calor especifico')
    axs[1, 0].set_xlabel('T')
    axs[1, 0].set_ylabel('Calor especifico')

    # Grafica de la correlacion.
    axs[1, 1].plot(cte.T, corr_all_first)
    axs[1, 1].set_title('Funcion correlacion para i = ' + str(cte.i[0]))
    axs[1, 1].set_xlabel('T')
    axs[1, 1].set_ylabel('Correlacion')

    # Grafica de la correlacion.
    axs[2, 0].plot(cte.T, corr_all_second)
    axs[2, 0].set_title('Funcion correlacion para i = ' + str(cte.i[1]))
    axs[2, 0].set_xlabel('T')
    axs[2, 0].set_ylabel('Correlacion')

    # Elimino el ultimo subplot que no se va a usar.
    fig.delaxes(axs[2, 1])

    # Guardo la figura en la carpeta de resultados.
    fig.savefig(os.path.join(os.path.join(result_path, str(N) + 'x' + str(N)),
                             'graph.jpg'), dpi=300)

    # Calculo el tiempo que ha tardado en hacer los graficos para este N.
    finish_graph_n = time.time()
    print(f'Tiempo para graficos de {N}x{N}: {finish_graph_n - finish_calc_n} s')

    # Muestro la figura.
    plt.show()

    # Guardo los resultados en un archivo de texto.
    rm.n_results(N, s_0,
                 finish_calc_n - start_n,
                 finish_graph_n - finish_calc_n,
                 mag_all, ene_all, cv_all,
                 corr_all_first, corr_all_second, os.path.join(result_path, str(N) + 'x' + str(N)))
