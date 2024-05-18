import os
import time

import matplotlib.pyplot as plt
import numpy as np

import vol.algorithms as alg
import vol.constants as cte
import vol.file_manager as fm
import vol.results_manager as rm
import vol.vol_params as param
import vol.sim_results as sr
import vol.analysis as an

########################################################################################################################
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

# El profesor ha puntualizado que la magnetizacion no hay que ponerla ya que estaba incluida en el obligatorio, pero en
# el analisis que hay que hacer en la segunda parte del voluntario, se pide que se haga un analisis del exponente
# critico de esta, por lo que se ha creado un modulo para calcularla mediante paralelizacion para reducir el tiempo
# de calculo, ya que la simulacion como tal se empezo sin este ultimo calculo, y debido al tiempo disponible
# no se ha podido hacer una simulacion completa con este calculo incluido, sino que se ha hecho aparte con este
# metodo para poder hacer el analisis de la segunda parte del voluntario.
########################################################################################################################

########################################################################################################################
# Principio de la primera parte del ejercicio voluntario, la simulacion de los parametros para cada N y T.
########################################################################################################################

# Genero las carpetas de resultados.
result_path = fm.init_files()

# Defino si se quieren hacer los calculos de las medias de los parametros.
PROMS = False

if PROMS:
    # Empiezo un bucle para cada N que hay en la lista de constantes.
    for N in cte.N:
        # Imprimo el N para saber en que paso del bucle estoy.
        print(f'Calculando para {N}x{N}')

        # Empiezo a contar el tiempo que tarda en hacer los calculos.
        start_n = time.time()

        # Defino para cada N, y parametros los arrays donde se guardaran los resultados de cada 100 pasos de montecarlo.
        # mag = np.zeros(cte.DIV)
        ene = np.zeros(cte.DIV)
        ene_sq = np.zeros(cte.DIV)
        s_plus_i_first = np.zeros(cte.DIV)
        s_plus_i_second = np.zeros(cte.DIV)

        # Defino las matrices que contendran los 10 valores de cada parametro, a representar en las graficas.
        # mag_all = np.zeros(len(cte.T))
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

            # Defino las variables para contabilizar cuando llevo 25%, 50&, 75% y 100% de los calculos para ir
            # printeando el porcentaje.
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
                    # mag[i // cte.STEP] = param.magnetization(s, N)
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
            # mag_all[k] = np.mean(mag) / N ** 2
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
                         # mag_all[k],
                         ene_all[k], cv_all[k],
                         corr_all_first[k], corr_all_second[k],
                         os.path.join(result_path, str(N) + 'x' + str(N)))

        # Imprimo el tiempo que ha tardado en hacer los calculos para este N.
        finish_calc_n = time.time()
        print(f'Tiempo para calculos de {N}x{N}: {finish_calc_n - start_n} s')

        # Genero las graficas y las guardo en la carpeta de resultados usando subplots y axes para poner las 5 graficas
        # en una misma figura para cada bucle de N.
        fig, axs = plt.subplots(2, 2, figsize=(15, 15))
        fig.suptitle(f'{N}x{N}', fontsize=20)

        # Grafica de la magnetizacion.
        # axs[0, 0].plot(cte.T, mag_all)
        # axs[0, 0].set_title('Magnetizacion')
        # axs[0, 0].set_xlabel('T')
        # axs[0, 0].set_ylabel('Magnetizacion')

        # Grafica de la energia.
        axs[0, 0].plot(cte.T, ene_all)
        axs[0, 0].set_title('Energia')
        axs[0, 0].set_xlabel('T')
        axs[0, 0].set_ylabel('Energia')

        # Grafica del calor especifico.
        axs[0, 1].plot(cte.T, cv_all)
        axs[0, 1].set_title('Calor especifico')
        axs[0, 1].set_xlabel('T')
        axs[0, 1].set_ylabel('Calor especifico')

        # Grafica de la correlacion 1.
        axs[1, 0].plot(cte.T, corr_all_first)
        axs[1, 0].set_title('Funcion correlacion para i = ' + str(cte.i[0]))
        axs[1, 0].set_xlabel('T')
        axs[1, 0].set_ylabel('Correlacion')

        # Grafica de la correlacion 2.
        axs[1, 1].plot(cte.T, corr_all_second)
        axs[1, 1].set_title('Funcion correlacion para i = ' + str(cte.i[1]))
        axs[1, 1].set_xlabel('T')
        axs[1, 1].set_ylabel('Correlacion')

        # Guardo la figura en la carpeta de resultados.
        fig.savefig(os.path.join(os.path.join(result_path, str(N) + 'x' + str(N)),
                                 'graph.jpg'),
                    dpi=300)

        # Calculo el tiempo que ha tardado en hacer los graficos para este N.
        finish_graph_n = time.time()
        print(f'Tiempo para graficos de {N}x{N}: {finish_graph_n - finish_calc_n} s')

        # Muestro la figura.
        plt.show()

        # Guardo los resultados en un archivo de texto.
        rm.n_results(N, s_0,
                     finish_calc_n - start_n,
                     finish_graph_n - finish_calc_n,
                     # mag_all,
                     ene_all, cv_all,
                     corr_all_first, corr_all_second, os.path.join(result_path, str(N) + 'x' + str(N)))

else:
    print('Omitiendo calculo de promedios')

########################################################################################################################
# Fin de la primera parte del ejercicio voluntario.
########################################################################################################################


########################################################################################################################
# Para la segunda parte del ejercicio voluntario, se hará un análisis de la simulación basada en 5 partes:
# 1. Describir el comportamiento de las anteriores magnitudes para el rango de temperaturas y tamaños. Comparar
#    con el resultado exácto de Onsager. Describir el efecto del tamaño en cada una de las variables.
# 2. Obtener de la literatura información sobre exponentes críticos y teoría de tamaño finito.
# 3. Estimar el valor del punto crítico: Para cada valor de N obtener una estimación del máximo del calor específico,
#    Tc(N), y estudiar su comportamiento con N extrapolando para N -> inf.
# 4. Obtener numéricamente el exponente crítico β de la magnetización y comparar con el resultado exacto.
# 5. Estudiar de la función f(i) con la temperatura y el tamaño del sistema. Extraer la longitud de correlación y su
#    exponente crítico característico.
########################################################################################################################

# Defino que pasos se quieren realizar.
ONSAGER = True
CRITICAL_TEMPERATURE = True
CRITICAL_EXPONENT = True
CORRELATION = True

########################################################################################################################
# 1. Describir el comportamiento de las anteriores magnitudes para el rango de temperaturas y tamaños. Comparar
# con el resultado exácto de Onsager. Describir el efecto del tamaño en cada una de las variables.
########################################################################################################################
if ONSAGER:
    # Obtengo los resultados de Onsager del archivo Resultados/Voluntario/Analisis/Onsager/magnitud_onsager.npy.
    E_inf = np.load(os.path.join(os.path.join(result_path, 'Analisis', 'Onsager'), 'e_onsager.npy'))
    Cv_inf = np.load(os.path.join(os.path.join(result_path, 'Analisis', 'Onsager'), 'cv_onsager.npy'))
    corr_first_inf = np.load(os.path.join(os.path.join(result_path, 'Analisis', 'Onsager'), 'corr_first_onsager.npy'))
    corr_second_inf = np.load(os.path.join(os.path.join(result_path, 'Analisis', 'Onsager'), 'corr_second_onsager.npy'))

    # Genero un grafico para cada magnitud ploteando los valores de la simulacion (para cada N) y los valores de
    # Onsager. Los resultados de la simulacion estan almacenados en sim_results.py con un formato de array de arrays
    # donde cada array corresponde a un N y cada valor de ese array corresponde a una temperatura.
    fig_energy, ax_energy = plt.subplots()
    fig_cv, ax_cv = plt.subplots()
    fig_corr_first, ax_corr_first = plt.subplots()
    fig_corr_second, ax_corr_second = plt.subplots()

    fig_energy.suptitle('Energia', fontsize=20)
    fig_cv.suptitle('Calor especifico', fontsize=20)
    fig_corr_first.suptitle('Correlacion i = ' + str(cte.i[0]), fontsize=20)
    fig_corr_second.suptitle('Correlacion i = ' + str(cte.i[1]), fontsize=20)

    for i in range(len(cte.N)):
        # Ploteo los valores de la simulacion.
        ax_energy.plot(cte.T, sr.E[i], 'o-', label='N = ' + str(cte.N[i]), color=cte.COLORS[i])
        ax_cv.plot(cte.T, sr.c[i], 'o-', label='N = ' + str(cte.N[i]), color=cte.COLORS[i])
        ax_corr_first.plot(cte.T, sr.fcorr0[i], 'o-', label='N = ' + str(cte.N[i]), color=cte.COLORS[i])
        ax_corr_second.plot(cte.T, sr.fcorr1[i], 'o-', label='N = ' + str(cte.N[i]), color=cte.COLORS[i])

    # Ploteo los valores de Onsager.
    ax_energy.plot(cte.T, E_inf, 'o-', label='Onsager', color='y')
    ax_cv.plot(cte.T, Cv_inf, 'o-', label='Onsager', color='y')
    ax_corr_first.plot(cte.T, corr_first_inf, 'o-', label='Onsager', color='y')
    ax_corr_second.plot(cte.T, corr_second_inf, 'o-', label='Onsager', color='y')

    # Pongo los ejes de cada grafico.
    ax_energy.set_xlabel('T')
    ax_energy.set_ylabel('Energia')

    ax_cv.set_xlabel('T')
    ax_cv.set_ylabel('Calor especifico')

    ax_corr_first.set_xlabel('T')
    ax_corr_first.set_ylabel('Correlacion')

    ax_corr_second.set_xlabel('T')
    ax_corr_second.set_ylabel('Correlacion')

    # Añado las leyendas a los graficos.
    ax_energy.legend()
    ax_cv.legend()
    ax_corr_first.legend()
    ax_corr_second.legend()

    # Guardo las figuras en la carpeta de resultados.
    fig_energy.savefig(os.path.join(os.path.join(result_path, 'Analisis'),
                                    'energy.jpg'),
                       dpi=300)
    fig_cv.savefig(os.path.join(os.path.join(result_path, 'Analisis'),
                                'cv.jpg'),
                   dpi=300)
    fig_corr_first.savefig(os.path.join(os.path.join(result_path, 'Analisis'),
                                        'corr_first.jpg'),
                           dpi=300)
    fig_corr_second.savefig(os.path.join(os.path.join(result_path, 'Analisis'),
                                         'corr_second.jpg'),
                            dpi=300)

    # Muestro las figuras.
    plt.show()

    # Guardo los resultados de Onsager en un archivo de texto.
    rm.onsager_results(E_inf, Cv_inf, corr_first_inf, corr_second_inf, os.path.join(result_path, 'Analisis'))
else:
    print('Omitiendo analisis de magnitudes y comparacion con Onsager')

########################################################################################################################
# 2. Obtener de la literatura información sobre exponentes críticos y teoría de tamaño finito.
########################################################################################################################
# Apartado unicamente teorico, no se realiza ninguna operacion.


########################################################################################################################
# 3. Estimar el valor del punto crítico: Para cada valor de N obtener una estimación del máximo del calor específico,
# Tc(N), y estudiar su comportamiento con N extrapolando para N -> inf:
########################################################################################################################
# Calculo la temperatura crítica y el calor específico máximo para cada N. Hago esto fuera del if porque la temperatura
# crítica es necesaria para el cálculo del exponente crítico.
max_T_cv = np.zeros((2, len(cte.N)))
for i in range(len(cte.N)):
    max_T_cv[0, i], max_T_cv[1, i] = an.critical_temperature(i)

if CRITICAL_TEMPERATURE:

    # Ploteo las temperaturas y los calores especificos en funcion de N.
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    fig.suptitle('Temperatura crítica y calor específico máximo', fontsize=20)

    axs[0].plot(cte.N, max_T_cv[0], 'o-', label='Tc')
    axs[0].axhline(y=cte.T_c_onsager, color='r', linestyle='--', label='Tc teórico')
    axs[0].set_title('Temperatura crítica')
    axs[0].set_xlabel('N')
    axs[0].set_ylabel('Tc')

    axs[1].plot(cte.N, max_T_cv[1], 'o-', label='Cv')
    axs[1].set_title('Calor específico máximo')
    axs[1].set_xlabel('N')
    axs[1].set_ylabel('Cv')

    # Guardo la figura en la carpeta de resultados.
    fig.savefig(os.path.join(os.path.join(result_path, 'Analisis'),
                             'critical_temperature_cv.jpg'),
                dpi=300)

    # Muestro la figura.
    plt.show()

    # Guardo los resultados en un archivo de texto.
    rm.critical_temperature_results(max_T_cv, os.path.join(result_path, 'Analisis'))
else:
    print('Omitiendo analisis de temperatura crítica y calor específico máximo')

########################################################################################################################
# 4. Obtener numéricamente el exponente crítico β de la magnetización y comparar con el resultado exacto.
########################################################################################################################
if CRITICAL_EXPONENT:
    # Cargo los valores de la magnetización de la simulación desde el archivo guardado con el mag_module.py con ruta
    # Resultado/Voluntario/Analisis/Datos/mag.npy
    m = np.load(os.path.join(os.path.join(result_path, 'Analisis', 'Datos'), 'mag.npy'))

    # Calculo el exponente crítico de la magnetización para cada N.
    beta = np.zeros((len(cte.N), 2))
    for i in range(len(cte.N)):
        beta[i, 0], beta[i, 1] = an.critical_exponent(m[i], max_T_cv[0, i])

    # Ploteo el exponente crítico de la magnetización en función de N.
    fig, ax = plt.subplots()
    fig.suptitle('Exponente crítico de la magnetización', fontsize=20)

    ax.errorbar(cte.N, beta[:, 0], yerr=beta[:, 1], fmt='o-', label='β')
    ax.axhline(y=cte.beta_t, color='r', linestyle='--', label='β teórico')
    ax.set_xlabel('N')
    ax.set_ylabel('β')

    # Guardo la figura en la carpeta de resultados.
    fig.savefig(os.path.join(os.path.join(result_path, 'Analisis'),
                             'critical_exponent.jpg'),
                dpi=300)

    # Muestro la figura.
    plt.show()

    # Hago la media de los valores de beta para cada N.
    beta_mean = np.mean(beta[:, 0])
    beta_mean_err = np.mean(beta[:, 1])

    # Guardo los resultados en un archivo de texto.
    rm.critical_exponent_results(beta, beta_mean, beta_mean_err, os.path.join(result_path, 'Analisis'))
else:
    print('Omitiendo analisis de exponente crítico de la magnetización')

########################################################################################################################
# 5. Estudiar de la función f(i) con la temperatura y el tamaño del sistema. Extraer la longitud de correlación y su
# exponente crítico característico.
########################################################################################################################
if CORRELATION:
    # Cargo los valores de las funciones de correlación de la simulación desde el archivo guardado con el
    # correlation_module.py con ruta Resultado/Voluntario/Analisis/Datos/corr.npy
    corr = np.load(os.path.join(os.path.join(result_path, 'Analisis', 'Datos'), 'corr.npy'))

    # Calculo la longitud de correlación para cada N y para cada T.
    xi = np.zeros((len(cte.N), len(cte.T), 2))
    for i in range(len(cte.N)):
        for j in range(len(cte.T)):
            xi[i, j, 0], xi[i, j, 1] = an.corr_length(corr[i, :, j])

    # Para cada N, ploteo la longitud de correlación en función de la temperatura.
    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    fig.suptitle('Longitud de correlación', fontsize=20)

    for i in range(len(cte.N)):
        axs[i // 2, i % 2].errorbar(cte.T, xi[i, :, 0], y_err=xi[i, :, 1], fmt='o-', label='N = ' + str(cte.N[i]))
        axs[i // 2, i % 2].set_title('N = ' + str(cte.N[i]))
        axs[i // 2, i % 2].set_xlabel('T')
        axs[i // 2, i % 2].set_ylabel('Longitud de correlación')
        axs[i // 2, i % 2].legend()

    # Guardo la figura en la carpeta de resultados.
    fig.savefig(os.path.join(os.path.join(result_path, 'Analisis'),
                            'correlation_length.jpg'),
                dpi=300)

    # Muestro la figura.
    plt.show()

    # Calculo el exponente critico de la funcion de correlacion para cada N. Este valor, mediante la formula que se ha
    # utilizado, solo se puede calcular a temperaturas cercanas al punto critico, por lo que se usarán los valores de
    # Tc obtenidos anteriormente. Para ello en cada bucle debo obtener la temperatura critica, y ver cual es el indice
    # de esa temperatura en el array de temperaturas, y a partir de ahi, calcular el exponente critico.
    eta = np.zeros((len(cte.N), 2))
    for i in range(len(cte.N)):
        for j in range(len(cte.T)):
            if cte.T[j] == max_T_cv[0, i]:
                eta[i, 0], eta[i, 1] = an.corr_exp(corr[i, :, j])

    # Ploteo el exponente crítico de la función de correlación en función de N.
    fig, ax = plt.subplots()
    fig.suptitle('Exponente crítico de la función de correlación', fontsize=20)

    ax.errorbar(cte.N, eta[:, 0], yerr=eta[:, 1], fmt='o-', label='η')
    ax.axhline(y=cte.eta_t, color='r', linestyle='--', label='η teórico')
    ax.set_xlabel('N')
    ax.set_ylabel('η')

    # Guardo la figura en la carpeta de resultados.
    fig.savefig(os.path.join(os.path.join(result_path, 'Analisis'),
                            'correlation_exponent.jpg'),
                dpi=300)

    # Muestro la figura.
    plt.show()

    # Guardo los resultados en un archivo de texto.
    rm.correlation_results(xi, eta, os.path.join(result_path, 'Analisis'))
else:
    print('Omitiendo analisis de longitud de correlación y exponente crítico de la función de correlación')
