import numpy as np
import matplotlib.pyplot as plt
import os

import vol.results_manager as rm
import vol.constants as cte
import vol.analysis as an
import vol.sim_results as sr


########################################################################################################################
# 1. Describir el comportamiento de las anteriores magnitudes para el rango de temperaturas y tamaños. Comparar
# con el resultado exácto de Onsager. Describir el efecto del tamaño en cada una de las variables.
########################################################################################################################
def onsager(result_path):
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
    fig_energy.savefig(os.path.join(os.path.join(result_path, 'Analisis/Onsager vs Exp'),
                                    'energy.jpg'),
                       dpi=300)
    fig_cv.savefig(os.path.join(os.path.join(result_path, 'Analisis/Onsager vs Exp'),
                                'cv.jpg'),
                   dpi=300)
    fig_corr_first.savefig(os.path.join(os.path.join(result_path, 'Analisis/Onsager vs Exp'),
                                        'corr_first.jpg'),
                           dpi=300)
    fig_corr_second.savefig(os.path.join(os.path.join(result_path, 'Analisis/Onsager vs Exp'),
                                         'corr_second.jpg'),
                            dpi=300)

    # Muestro las figuras.
    plt.show()

    # Guardo los resultados de Onsager en un archivo de texto.
    rm.onsager_results(E_inf, Cv_inf, corr_first_inf, corr_second_inf, os.path.join(result_path,
                                                                                    'Analisis/Onsager vs Exp'))


########################################################################################################################
# 3. Estimar el valor del punto crítico: Para cada valor de N obtener una estimación del máximo del calor específico,
# Tc(N), y estudiar su comportamiento con N extrapolando para N -> inf:
########################################################################################################################
def critical_temperature(result_path, max_T_cv):
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
    fig.savefig(os.path.join(os.path.join(result_path, 'Analisis/Temperatura critica'),
                             'critical_temperature_cv.jpg'),
                dpi=300)

    # Muestro la figura.
    plt.show()

    # Guardo los resultados en un archivo de texto.
    rm.critical_temperature_results(max_T_cv, os.path.join(result_path, 'Analisis/Temperatura critica'))


########################################################################################################################
# 4. Obtener numéricamente el exponente crítico β de la magnetización y comparar con el resultado exacto.
########################################################################################################################
def critical_exponent(result_path, max_T_cv):
    # Cargo los valores de la magnetización de la simulación desde el archivo guardado con el mag_module.py con ruta
    # Resultado/Voluntario/Analisis/Datos/mag.npy
    m = np.load(os.path.join(os.path.join(result_path, 'Analisis', 'Datos'), 'mag.npy'))

    # Para cada valor de magnetizacion, debo dividirlo entre N ** 2 ya que a la hora de realizar la simulacion no fue
    # dividido por N ** 2, y para poder comparar con el valor teorico, debo dividirlo.
    for i in range(len(cte.N)):
        m[i] /= cte.N[i] ** 2

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
    fig.savefig(os.path.join(os.path.join(result_path, 'Analisis/Exponente de magnetizacion'),
                             'critical_exponent.jpg'),
                dpi=300)

    # Muestro la figura.
    plt.show()

    # Hago la media de los valores de beta para cada N.
    beta_mean = np.mean(beta[:, 0])
    beta_mean_err = np.mean(beta[:, 1])

    # Guardo los resultados en un archivo de texto.
    rm.critical_exponent_results(beta, beta_mean, beta_mean_err, os.path.join(result_path,
                                                                              'Analisis/Exponente de magnetizacion'))


########################################################################################################################
# 5. Estudiar de la función f(i) con la temperatura y el tamaño del sistema. Extraer la longitud de correlación y su
# exponente crítico característico.
########################################################################################################################
def correlation(result_path, max_T_cv):
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
    fig.savefig(os.path.join(os.path.join(result_path, 'Analisis/Correlacion'),
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
    fig.savefig(os.path.join(os.path.join(result_path, 'Analisis/Correlacion'),
                             'correlation_exponent.jpg'),
                dpi=300)

    # Muestro la figura.
    plt.show()

    # Guardo los resultados en un archivo de texto.
    rm.correlation_results(xi, eta, os.path.join(result_path, 'Analisis/Correlacion'))
