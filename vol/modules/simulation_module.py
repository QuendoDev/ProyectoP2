import numpy as np
import os
import time
import matplotlib.pyplot as plt

import vol.setup.constants as cte
import vol.setup.settings as st
import vol.calc.algorithms as alg
import vol.calc.vol_params as param
import math

"""
format_time function
Formats the time in seconds to hours, minutes and seconds.

Parameters
----------
seconds : int
    Time in seconds.
    
Returns
-------
str
    Time formatted in hours, minutes and seconds.
"""


def format_time(seconds):
    # Divide the time in seconds in hours, minutes and seconds.
    hours, remainder = divmod(seconds, 3600)
    # Divide the remainder in minutes and seconds.
    minutes, seconds = divmod(remainder, 60)

    # Return the formatted time.
    return "{:02} horas {:02} minutos {:02} segundos".format(int(hours), int(minutes), int(seconds))


"""
sim function
Simulates the Ising model for a list of N values and a list of T values, calculating the average magnetization, energy,
specific heat and correlation function for each N, T and for all values of i in i = {1, 3, 5, 7}. While doing this, it
prints the percentage of the calculations that have been done and the time that has passed since the beginning of the
calculations. It saves each magnitude in a text file.

Parameters
----------
args : tuple
    Tuple with the values of N and T. Necessary to use the multiprocessing library.
    
Returns
-------
N : int
    Size of the system.
T : float
    Temperature of the system.
mag_t : float
    Average magnetization of the system.
ene_t : float
    Average energy of the system.
cv : float
    Specific heat of the system.
corr_1 : float
    Correlation function for i = 1.
corr_3 : float
    Correlation function for i = 3.
corr_5 : float
    Correlation function for i = 5.
corr_7 : float
    Correlation function for i = 7.
"""


def sim(args):
    N, T = args
    mag = np.zeros(cte.DIV)
    ene = np.zeros(cte.DIV)
    ene_sq = np.zeros(cte.DIV)
    s_plus_i_first = np.zeros(cte.DIV)
    s_plus_i_second = np.zeros(cte.DIV)
    s_plus_i_third = np.zeros(cte.DIV)
    s_plus_i_fourth = np.zeros(cte.DIV)

    # Data path for the results.
    data_path = cte.DATA_PATH

    # Print the N and T to know in which step of the simulation we are.
    print(f'Calculating for {N}x{N} and T = {T}')

    # Generate the initial configuration.
    s = np.ones((N, N))
    s_0 = s.copy()

    # Define the probability vector related to the possible energy variations [-8, -4, 0, 4, 8] that can occur in the
    # system, and that will be used in the metropolis algorithm.
    p = np.zeros(5)
    for i in range(5):
        v = 4 * i - 8
        p[i] = np.exp(-v / T)

    # Start counting the time it takes to do the calculations.
    start_n = time.time()

    # Variables to count when 25%, 50%, 75% and 100% of the calculations have been done to print the percentage.
    time_25 = 0
    time_50 = 0
    time_75 = 0

    # Loop for each cycle of the simulation.
    for i in range(cte.CYCLES):
        # Save the values of the parameters every 100 steps to calculate the average at the end of the loop.
        if i % cte.STEP == 0:
            mag[i // cte.STEP] = param.magnetization(s, N)
            e = param.energy(s, N)
            ene[i // cte.STEP] = e
            ene_sq[i // cte.STEP] = e ** 2
            s_plus_i_first[i // cte.STEP] = param.sum_correlation(s, cte.i[0], N)
            s_plus_i_second[i // cte.STEP] = param.sum_correlation(s, cte.i[1], N)
            s_plus_i_third[i // cte.STEP] = param.sum_correlation(s, cte.i[2], N)
            s_plus_i_fourth[i // cte.STEP] = param.sum_correlation(s, cte.i[3], N)

        # Do a montecarlo step.
        s = alg.montecarlo(s, N, p)

        # Print the percentage of calculations that have been done, including N and T.
        if i == cte.CYCLES // 4:
            time_25 = time.time()
            print(f'{N}x{N}, T = {T}, 25%, {str(time_25 - start_n)} s, {str(time_25 - start_n)} s')
        elif i == cte.CYCLES // 2:
            time_50 = time.time()
            print(f'{N}x{N}, T = {T}, 50%, {str(time_50 - start_n)} s, {str(time_50 - time_25)} s')
        elif i == cte.CYCLES // 4 * 3:
            time_75 = time.time()
            print(f'{N}x{N}, T = {T}, 75%, {str(time_75 - start_n)} s, {str(time_75 - time_50)} s')

    # Print the time it took to do the calculations for this N and T.
    finish_n = time.time()
    print(f'{N}x{N}, T = {T}, 100%, {str(finish_n - start_n)} s, {str(finish_n - time_75)} s')
    print(f'Time for calculations of {N}x{N}, T = {T}: {finish_n - start_n} s')

    # Calculate the final parameters for this N and T.
    mag_t = np.mean(mag)
    ene_t = np.mean(ene) / (2 * N)
    cv = (np.mean(ene_sq) - np.mean(ene) ** 2) / (T * N ** 2)
    corr_1 = np.mean(s_plus_i_first) / N ** 2
    corr_3 = np.mean(s_plus_i_second) / N ** 2
    corr_5 = np.mean(s_plus_i_third) / N ** 2
    corr_7 = np.mean(s_plus_i_fourth) / N ** 2

    # Print the final parameters for this N and T.
    print(f'{N}x{N}, T = {T}, Magnetization: {mag_t}')
    print(f'{N}x{N}, T = {T}, Energy: {ene_t}')
    print(f'{N}x{N}, T = {T}, Specific heat: {cv}')
    print(f'{N}x{N}, T = {T}, Correlation for i = {cte.i[0]}: {corr_1}')
    print(f'{N}x{N}, T = {T}, Correlation for i = {cte.i[1]}: {corr_3}')
    print(f'{N}x{N}, T = {T}, Correlation for i = {cte.i[2]}: {corr_5}')
    print(f'{N}x{N}, T = {T}, Correlation for i = {cte.i[3]}: {corr_7}')

    # Save all the results in one text file with the following format: <parameter>: <value>.
    with open(os.path.join(data_path, f'{N}_{T}.txt'), 'w') as f:
        f.write('Time for calculations: ' + format_time(finish_n - start_n) + '\n')
        f.write('----------------------------------------------------------------\n')
        f.write(f'Magnetization: {mag_t}\n')
        f.write(f'Energy: {ene_t}\n')
        f.write(f'Specific heat: {cv}\n')
        f.write(f'Correlation for i = {cte.i[0]}: {corr_1}\n')
        f.write(f'Correlation for i = {cte.i[1]}: {corr_3}\n')
        f.write(f'Correlation for i = {cte.i[2]}: {corr_5}\n')
        f.write(f'Correlation for i = {cte.i[3]}: {corr_7}\n')

    # Save all the results as an array in a npy file.
    np.save(os.path.join(data_path, f'{N}_{T}.npy'), [mag_t, ene_t, cv, corr_1, corr_3, corr_5, corr_7])

    return N, T, mag_t, ene_t, cv, corr_1, corr_3, corr_5, corr_7


"""
simulation_graphs function
Takes the results of the simulation and generates the graphs for each magnitude, depending on the number of true values
in the configuration parameter.

Parameters
----------
config : numpy array
    Boolean array with the magnitudes that will be generated. The order of the array is the following: [magnetization,
    energy, specific heat, correlation_1, correlation_3, correlation_5, correlation_7].
mag : numpy array
    Array with the magnetization values for each N and T.
en : numpy array
    Array with the energy values for each N and T.
cv : numpy array
    Array with the specific heat values for each N and T.
corr : numpy array
    Array with the correlation values for each N and T and for each i in i = {1, 3, 5, 7}. The shape of the array is
    (len(N), 4, len(T)).
"""


def simulation_graphs(config, mag, en, cv, corr):
    # Calculates how many graphs will be generated, depending on the number of true values in the configuration.
    n_graphs = sum(config)

    # Calculate the shape of the figure where each graph will be done. The number of rows and columns will depend on
    # the number of graphs that will be generated. The size of the figure will also depend on the number of graphs,
    # with a maximum of 4 graphs per row.
    n_cols = st.COLS if n_graphs > st.COLS else n_graphs
    n_rows = math.ceil(n_graphs / st.COLS)

    # For each N value, generate the graphs for each magnitude.
    for N in cte.N:
        # Create the figure where the graphs will be plotted and set the title of the figure.
        fig, axs = plt.subplots(n_rows, n_cols, figsize=(15, 3 * n_rows))
        fig.suptitle(f'{N}x{N}', fontsize=20)

        # For each magnitude, generate the graph if it is true in the configuration.
        count = 0

        # If there are more than 4 graphs to generate, axs will be a 2D array, so we need to access the elements with
        # two indices. If there are less than 4 graphs, axs will be a 1D array, so we need to access the elements with
        # only one index and the else statement will be executed.
        if n_graphs > st.COLS:
            # Generate the magnetization graph.
            if config[0]:
                axs[count // n_cols, count % n_cols].plot(cte.T, mag[np.where(cte.N == N)[0][0]])
                axs[count // n_cols, count % n_cols].set_title('Magnetization')
                axs[count // n_cols, count % n_cols].set_xlabel('T')
                axs[count // n_cols, count % n_cols].set_ylabel('Magnetization')
                count += 1

            # Generate the energy graph.
            if config[1]:
                axs[count // n_cols, count % n_cols].plot(cte.T, en[np.where(cte.N == N)[0][0]])
                axs[count // n_cols, count % n_cols].set_title('Energy')
                axs[count // n_cols, count % n_cols].set_xlabel('T')
                axs[count // n_cols, count % n_cols].set_ylabel('Energy')
                count += 1

            # Generate the specific heat graph.
            if config[2]:
                axs[count // n_cols, count % n_cols].plot(cte.T, cv[np.where(cte.N == N)[0][0]])
                axs[count // n_cols, count % n_cols].set_title('Specific Heat')
                axs[count // n_cols, count % n_cols].set_xlabel('T')
                axs[count // n_cols, count % n_cols].set_ylabel('Specific Heat')
                count += 1

            # Generate the correlation graphs.
            for i in range(4):
                if config[i + 3]:
                    axs[count // n_cols, count % n_cols].plot(cte.T, corr[np.where(cte.N == N)[0][0], i])
                    axs[count // n_cols, count % n_cols].set_title(f'Correlation for i = {cte.i[i]}')
                    axs[count // n_cols, count % n_cols].set_xlabel('T')
                    axs[count // n_cols, count % n_cols].set_ylabel('Correlation')
                    count += 1
        else:
            # Generate the magnetization graph.
            if config[0]:
                axs[count].plot(cte.T, mag[np.where(cte.N == N)[0][0]])
                axs[count].set_title('Magnetization')
                axs[count].set_xlabel('T')
                axs[count].set_ylabel('Magnetization')
                count += 1

            # Generate the energy graph.
            if config[1]:
                axs[count].plot(cte.T, en[np.where(cte.N == N)[0][0]])
                axs[count].set_title('Energy')
                axs[count].set_xlabel('T')
                axs[count].set_ylabel('Energy')
                count += 1

            # Generate the specific heat graph.
            if config[2]:
                axs[count].plot(cte.T, cv[np.where(cte.N == N)[0][0]])
                axs[count].set_title('Specific Heat')
                axs[count].set_xlabel('T')
                axs[count].set_ylabel('Specific Heat')
                count += 1

            # Generate the correlation graphs.
            for i in range(4):
                if config[i + 3]:
                    axs[count].plot(cte.T, corr[np.where(cte.N == N)[0][0], i])
                    axs[count].set_title(f'Correlation for i = {cte.i[i]}')
                    axs[count].set_xlabel('T')
                    axs[count].set_ylabel('Correlation')
                    count += 1

        # After generating all the graphs, check if the number of generated graphs is less than the total number of
        # graphs. total_graphs is the total number of graphs that can be generated in the figure.
        total_graphs = n_rows * n_cols
        if count < total_graphs:
            # If so, generate empty graphs in the remaining spaces.
            for i in range(count, total_graphs):
                if n_graphs > st.COLS:
                    axs[i // n_cols, i % n_cols].axis('off')
                else:
                    axs[i].axis('off')

        # Save the figure with all the graphs.
        plt.savefig(os.path.join(cte.DATA_PATH, f'{N}.png'))

        # Show the figure.
        plt.show()
