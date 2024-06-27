import os

import matplotlib.pyplot as plt
import numpy as np

import vol.calc.analysis as an
import vol.setup.constants as cte
import vol.managers.results_manager as rm

"""
########################################################################################################################
1. Describe the behavior of the previous magnitudes for the range of temperatures and sizes. Compare with the exact
    result of Onsager. Describe the effect of size on each of the variables.
########################################################################################################################
"""

"""
onsager function
This function compares the results of the simulation with the exact results of Onsager. It plots the energy, specific
heat, and correlation functions for each N and compare the specific heat with the exact result of Onsager. The graphs
are saved in the results folder and the results are saved in a text file.

Parameters:
----------
en: numpy array
    Array with the energy values of the simulation for each N and each temperature.
cv: numpy array
    Array with the specific heat values of the simulation for each N and each temperature.
corr: numpy array
    Array with the correlation function values of the simulation for each N, each temperature, and each i. The shape
    of the array is (len(N), 4, len(T)).
"""


def onsager(en, cv, corr):
    # Copy the temperatures used for the Onsager exact representation.
    T = cte.T_ext.copy()

    # Load the specific heat values of Onsager from the file cv_onsager.npy.
    Cv_inf = np.load(os.path.join(cte.DATA_PATH, 'cv_onsager.npy'))

    # Generate a graph for each magnitude plotting the values of the simulation (for each N) and the values of Onsager.
    # The results of the simulation made for making the document are stored in sim_results.py with an array of arrays,
    # where each array corresponds to an N and each value of that array corresponds to a temperature, but for
    # delivering the code, all the results will be stored in the cte.DATA_PATH folder.
    fig_energy, ax_energy = plt.subplots()
    fig_cv, ax_cv = plt.subplots()
    fig_corr_first, ax_corr_first = plt.subplots()
    fig_corr_second, ax_corr_second = plt.subplots()

    fig_energy.suptitle('Energy', fontsize=20)
    fig_cv.suptitle('Specific heat', fontsize=20)
    fig_corr_first.suptitle('Correlation i = ' + str(cte.i[0]), fontsize=20)
    fig_corr_second.suptitle('Correlation i = ' + str(cte.i[1]), fontsize=20)

    # Plot the values of the simulation for each N.
    for i in range(len(cte.N)):
        ax_energy.plot(cte.T, en[i], 'o-', label='N = ' + str(cte.N[i]), color=cte.COLORS[i],
                       markersize=3)
        ax_cv.plot(cte.T, cv[i], 'o-', label='N = ' + str(cte.N[i]), color=cte.COLORS[i],
                   markersize=3)
        ax_corr_first.plot(cte.T, corr[i, 0], 'o-', label='N = ' + str(cte.N[i]), color=cte.COLORS[i],
                           markersize=3)
        ax_corr_second.plot(cte.T, corr[i, 1], 'o-', label='N = ' + str(cte.N[i]), color=cte.COLORS[i],
                            markersize=3)

    # Plot the values of Onsager for the specific heat.
    ax_cv.plot(T, Cv_inf, '-', label='Onsager', color='y', markersize=3)

    # Add the labels to the graphs.
    ax_energy.set_xlabel('T')
    ax_energy.set_xticks(cte.T)
    ax_energy.set_ylabel('Energy')

    ax_cv.set_xlabel('T')
    ax_cv.set_xticks(cte.T)
    ax_cv.set_ylabel('Specific heat')

    ax_corr_first.set_xlabel('T')
    ax_corr_first.set_xticks(cte.T)
    ax_corr_first.set_ylabel('Correlation i = ' + str(cte.i[0]))

    ax_corr_second.set_xlabel('T')
    ax_corr_second.set_xticks(cte.T)
    ax_corr_second.set_ylabel('Correlation i = ' + str(cte.i[1]))

    # Add the legends to the graphs.
    ax_energy.legend()
    ax_cv.legend()
    ax_corr_first.legend()
    ax_corr_second.legend()

    # Save the graphs in the results folder.
    fig_energy.savefig(os.path.join(os.path.join(cte.ANALYSIS_PATH, 'Onsager vs Exp'),
                                    'energy.jpg'),
                       dpi=300)
    fig_cv.savefig(os.path.join(os.path.join(cte.ANALYSIS_PATH, 'Onsager vs Exp'),
                                'cv.jpg'),
                   dpi=300)
    fig_corr_first.savefig(os.path.join(os.path.join(cte.ANALYSIS_PATH, 'Onsager vs Exp'),
                                        'corr_first.jpg'),
                           dpi=300)
    fig_corr_second.savefig(os.path.join(os.path.join(cte.ANALYSIS_PATH, 'Onsager vs Exp'),
                                         'corr_second.jpg'),
                            dpi=300)

    # Show the graphs.
    plt.show()

    # Save the results in a text file with a custom format defined in the results_manager.py file.
    rm.onsager_results(Cv_inf, os.path.join(cte.ANALYSIS_PATH, 'Onsager vs Exp'))


"""
########################################################################################################################
3. Estimate the value of the critical point: For each value of N, obtain an estimate of the maximum of the specific
    heat, Tc(N), and study its behavior with N extrapolating to N -> inf.
########################################################################################################################
"""

"""
critical_temperature function
This function plots the critical temperature and the maximum specific heat for each N. It compares the results with the
theoretical values of Onsager: one of them is the exact critical temperature defined in the constants.py file and the
other is the maximum specific heat calculated with the Onsager exact representation. The graphs are saved in the results
folder and the results are saved in a text file.

Parameters:
----------
max_T_cv: numpy array
    Array with the critical temperature and the maximum specific heat for each N. The shape of the array is (2, len(N)).
"""


def critical_temperature(max_T_cv):
    # Initialize the figure with two subplots. The first one is for the critical temperature and the second one is for
    # the maximum specific heat.
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    fig.suptitle('Critical temperature and maximum specific heat', fontsize=20)

    # Load the specific heat values of Onsager from the file cv_onsager.npy.
    Cv_inf = np.load(os.path.join(cte.DATA_PATH, 'cv_onsager.npy'))

    # Find the maximum specific heat and the critical temperature for the Onsager exact representation.
    max_Cv = np.max(Cv_inf)
    max_T = cte.T_ext[np.where(Cv_inf == max_Cv)[0][0]]

    # Plot the critical temperature for each N, including the theoretical value of Onsager defined in the constants.py
    # file with a red dashed line, and the critical temperature obtained from the maximum specific heat of the Onsager
    # exact representation with a green dashed line.
    axs[0].plot(cte.N, max_T_cv[0], 'o-', label='Tc')
    axs[0].axhline(y=cte.T_c_onsager, color='r', linestyle='--', label='Tc theoretical')
    axs[0].axhline(y=max_T, color='g', linestyle='--', label='Tc Onsager')
    axs[0].set_title('Critical temperature')
    axs[0].set_xlabel('N')
    axs[0].set_xticks(cte.N)
    axs[0].set_ylabel('Tc')
    axs[0].legend()

    # Calculate the specific heat using the exact critical temperature of Onsager minus a small value to avoid the
    # divergence of the specific heat.
    cv_onsager = an.heat_onsager(cte.T_c_onsager - 0.0015)

    # Plot the maximum specific heat for each N, including the maximum specific heat obtained from the theoretical value
    # of the critical temperature with a red dashed line, and the maximum specific heat calculated with the Onsager
    # exact representation with a green dashed line.
    axs[1].plot(cte.N, max_T_cv[1], 'o-', label='Cv')
    axs[1].axhline(y=cv_onsager, color='r', linestyle='--', label='Cv theoretical - 0.0015')
    axs[1].axhline(y=max_Cv, color='g', linestyle='--', label='Cv Onsager')
    axs[1].set_title('Maximum specific heat')
    axs[1].set_xlabel('N')
    axs[1].set_xticks(cte.N)
    axs[1].set_ylabel('Cv')
    axs[1].legend()

    # Save the graphs in the results folder.
    fig.savefig(os.path.join(os.path.join(cte.ANALYSIS_PATH, 'Temperatura critica'),
                             'critical_temperature_cv.jpg'),
                dpi=300)

    # Show the graphs.
    plt.show()

    # Save the results in a text file with a custom format defined in the results_manager.py file.
    rm.critical_temperature_results(max_T_cv, cv_onsager, max_T, max_Cv,
                                    os.path.join(cte.ANALYSIS_PATH, 'Temperatura critica'))


"""
########################################################################################################################
4. Obtain numerically the critical exponent β of the magnetization and compare with the exact result.
########################################################################################################################
"""

"""
critical_exponent function
This function calculates the critical exponent of the magnetization for each N and plots the results. It compares the
results with the theoretical value of Onsager. The graphs are saved in the results folder and the results are saved in a
text file.

Parameters:
----------
max_T_cv: numpy array
    Array with the critical temperature and the maximum specific heat for each N. The shape of the array is (2, len(N)).
mag: numpy array
    Array with the magnetization values of the simulation for each N and each temperature.
"""


def critical_exponent(mag, max_T_cv):
    # Array to store the critical exponent of the magnetization and its error for each N.
    beta = np.zeros((len(cte.N), 2))

    # Calculate the critical exponent of the magnetization and its error for each N. The critical exponent is calculated
    # using the critical temperature obtained in the vol_main.py file.
    for i in range(len(cte.N)):
        beta[i, 0], beta[i, 1] = an.critical_exponent(mag[i], max_T_cv[0, i])

    # Plot the critical exponent of the magnetization for each N with its error, including the theoretical value of
    # Onsager defined in the constants.py file with a red dashed line.
    fig, ax = plt.subplots()
    fig.suptitle('Critical exponent of magnetization', fontsize=20)

    ax.errorbar(cte.N, beta[:, 0], yerr=beta[:, 1], fmt='o-', label='β')
    ax.axhline(y=cte.beta_t, color='r', linestyle='--', label='β theoretical')
    ax.set_xlabel('N')
    ax.set_xticks(cte.N)
    ax.set_ylabel('β')

    # Save the graph in the results' folder.
    fig.savefig(os.path.join(os.path.join(cte.ANALYSIS_PATH, 'Exponente de magnetizacion'),
                             'critical_exponent.jpg'),
                dpi=300)

    # Show the graph.
    plt.show()

    # Calculate the mean of the critical exponent of the magnetization and its error for each N.
    beta_mean = np.mean(beta[:, 0])
    beta_mean_err = np.mean(beta[:, 1])

    # Save the results in a text file with a custom format defined in the results_manager.py file.
    rm.critical_exponent_results(beta, beta_mean, beta_mean_err, os.path.join(cte.ANALYSIS_PATH,
                                                                              'Exponente de magnetizacion'))


"""
########################################################################################################################
5. Study the function f(i) with temperature and system size. Extract the correlation length and its characteristic
    critical exponent.
########################################################################################################################
"""

"""
correlation function
This function calculates the correlation length and the critical exponent of the correlation function for each N. It
plots the correlation length in function of the temperature for each N and the critical exponent of the correlation
function in function of N. The graphs are saved in the results folder and the results are saved in a text file.

Parameters:
----------
corr: numpy array
    Array with the correlation function values of the simulation for each N, each temperature, and each i. The shape
    of the array is (len(N), 4, len(T)).
max_T_cv: numpy array
    Array with the critical temperature and the maximum specific heat for each N. The shape of the array is (2, len(N)).
"""


def correlation(corr, max_T_cv):
    # Calculate the correlation length and its error for each N and each temperature.
    xi = np.zeros((len(cte.N), len(cte.T), 2))
    for i in range(len(cte.N)):
        for j in range(len(cte.T)):
            xi[i, j, 0], xi[i, j, 1] = an.corr_length(corr[i, :, j])

    # Initialize the figure with four subplots, one for each pair xi-T depending on the N.
    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    fig.suptitle('Correlation length', fontsize=20)

    # Plot the correlation length for each N in function of the temperature. For each subplot, the x-axis is the
    # temperature and the y-axis is the correlation length. The error bars are included in the plot.
    for i in range(len(cte.N)):
        axs[i // 2, i % 2].errorbar(cte.T, xi[i, :, 0], yerr=xi[i, :, 1], fmt='o-', label='N = ' + str(cte.N[i]))
        axs[i // 2, i % 2].set_title('N = ' + str(cte.N[i]))
        axs[i // 2, i % 2].set_xlabel('T')
        axs[i // 2, i % 2].set_ylabel('Correlation length')
        axs[i // 2, i % 2].legend()

    # Save the graph in the results' folder.
    fig.savefig(os.path.join(os.path.join(cte.ANALYSIS_PATH, 'Correlacion'),
                             'correlation_length.jpg'),
                dpi=300)

    # Show the graph.
    plt.show()

    # Array to store the critical exponent of the correlation function and its error for each N.
    eta = np.zeros((len(cte.N), 2))

    # Calculate the critical exponent of the correlation function and its error for each N. The critical exponent,
    # using the formula that has been used, can only be calculated at temperatures close to the critical point, so the
    # critical temperatures obtained previously will be used. For this, in each loop, I must obtain the critical
    # temperature, and see which is the index of that temperature in the array of temperatures, and from there,
    # calculate the critical exponent.
    for i in range(len(cte.N)):
        for j in range(len(cte.T)):
            if cte.T[j] == max_T_cv[0, i]:
                eta[i, 0], eta[i, 1] = an.corr_exp(corr[i, :, j])

    # Plot the critical exponent of the correlation function for each N with its error, including the theoretical value
    # of Onsager defined in the constants.py file with a red dashed line.
    fig, ax = plt.subplots()
    fig.suptitle('Critical exponent of the correlation function', fontsize=20)

    ax.errorbar(cte.N, eta[:, 0], yerr=eta[:, 1], fmt='o-', label='η')
    ax.axhline(y=cte.eta_t, color='r', linestyle='--', label='η theoretical')
    ax.set_xlabel('N')
    ax.set_xticks(cte.N)
    ax.set_ylabel('η')

    # Save the graph in the results' folder.
    fig.savefig(os.path.join(os.path.join(cte.ANALYSIS_PATH, 'Correlacion'),
                             'correlation_exponent.jpg'),
                dpi=300)

    # Show the graph.
    plt.show()

    # Calculate the mean of the critical exponent of the correlation function and its error for each N.
    eta_mean = np.mean(eta[:, 0])
    eta_mean_err = np.mean(eta[:, 1])

    # Save the results in a text file with a custom format defined in the results_manager.py file.
    rm.correlation_results(xi, eta, eta_mean, eta_mean_err, os.path.join(cte.ANALYSIS_PATH, 'Correlacion'))
