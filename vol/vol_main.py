import os
from concurrent.futures import ProcessPoolExecutor
from itertools import product
import numpy as np

import vol.setup.constants as cte
import vol.setup.settings as st
import vol.managers.file_manager as fm
import vol.calc.analysis as an
import vol.modules.analisis_module as an_mod
import vol.modules.onsager_module as ons_mod
import vol.modules.simulation_module as sim_mod

"""
We want to calculate a list of parameters for each N in [16, 32, 64, 128], representing for each temperature in 
[1.5, 3.5] with 10 values. The parameters we want to calculate are:
- The average magnetization
- The average energy
- The specific heat
- The correlation function

For this, an initial configuration of all ordered spins (s[i, j] = 1 for any i, j) is generated, and the system is 
allowed to evolve 1000000 cycles, saving the results every 100 cycles. Each result is saved in a position of the array
corresponding to the parameter being calculated and at the end of the loop, the mean of that array is taken to obtain
the average value of that parameter. If any further calculation using scalars or constants is needed at the end of the
formula to obtain the final value that is requested, it is done at the end of the loop to save calculations.

Finally, the results are saved in a text file with the name of the parameters that have been calculated and the
corresponding graphs are generated.

The professor has pointed out that the magnetization does not need to be included since it was included in the
mandatory part, but in the analysis that needs to be done in the second part of the voluntary, it is requested that an
analysis of the critical exponent of this be done, so a module has been created to calculate it by parallelization to
reduce the calculation time, since the simulation as such was started without this last calculation, and due to the
available time, a complete simulation with this calculation included has not been possible, but a separate one has been
done with this method in order to be able to do the analysis of the second part of the voluntary.

In the delivered code, the calculation of the magnetization and correlation function for i = {5, 7} is included, but
in the simulation made for the document, those parameters were calculated in other modules. For making the code more
readable, the calculation of the magnetization and correlation function for i = {5, 7} has been removed from those
modules and included in the simulation module, so that all the calculations are done in the same module and it is only
necessary to call the simulation module to obtain all the results.
"""

"""
########################################################################################################################
INSTRUCTIONS FOR RUNNING THE CODE:
1. Change the path in the constants.py file to the path where the results will be saved.
2. Modify the settings.py file to set the parameters of the simulation and the analysis that will be done.
3. Modify the values of the constants in the constants.py file to change the parameters of the simulation and the
    analysis that will be done, such as the posible sizes of the lattice, the temperatures to simulate, the temperatures
    used in the Onsager exact representation, the values of i for the correlation function, and the colors for the plots
    of the parameters.
4. Run the code.

!!! IMPORTANT !!!
If the simulation is going to be done, the run time of the code is going to be long, since the simulation is done for
each N and T, and the calculation of the parameters is done for each N and T. The simulation is done in parallel to
reduce the calculation time, but it is still going to take a long time. If the simulation is not going to be done, the
results are loaded from the .npy files, so the run time is going to be shorter. Be careful with the number of workers
used in the parallelization, since it can cause the computer to freeze if the number of workers is too high.
########################################################################################################################
"""

"""
########################################################################################################################
Start of the first part of the voluntary exercise, the simulation of the parameters for each N and T.
########################################################################################################################
"""

# Generate the folders for the results.
fm.init_files()

# Variables to store the results of the simulation.
mag = np.zeros((len(cte.N), len(cte.T)))
en = np.zeros((len(cte.N), len(cte.T)))
cv = np.zeros((len(cte.N), len(cte.T)))
corr = np.zeros((len(cte.N), 4, len(cte.T)))

# If the simulation is going to be done, the simulation module is called to calculate the parameters for each N and T,
# and the results are saved in a .npy file. If the simulation is not going to be done, the results are loaded from the
# .npy file.
if st.SIMULATE:
    print('Starting simulation of parameters for each N and T')
    with ProcessPoolExecutor(max_workers=st.MAX_WORKERS) as executor:
        results = executor.map(sim_mod.sim,
                               product(cte.N, cte.T))

    for result in results:
        Nr, Tr, mag_tr, en_tr, cv_tr, corr1_tr, corr3_tr, corr5_tr, corr7_tr = result
        mag[np.where(cte.N == Nr)[0], np.where(cte.T == Tr)[0]] = mag_tr
        en[np.where(cte.N == Nr)[0], np.where(cte.T == Tr)[0]] = en_tr
        cv[np.where(cte.N == Nr)[0], np.where(cte.T == Tr)[0]] = cv_tr
        corr[np.where(cte.N == Nr)[0], 0, np.where(cte.T == Tr)[0]] = corr1_tr
        corr[np.where(cte.N == Nr)[0], 1, np.where(cte.T == Tr)[0]] = corr3_tr
        corr[np.where(cte.N == Nr)[0], 2, np.where(cte.T == Tr)[0]] = corr5_tr
        corr[np.where(cte.N == Nr)[0], 3, np.where(cte.T == Tr)[0]] = corr7_tr

    print('Finished simulation of parameters for each N and T')

else:
    print('Omitting calculation of averages, taking data from .npy file')
    for N in cte.N:
        for T in cte.T:
            data = np.load(os.path.join(cte.DATA_PATH, f'{N}_{T}.npy'))
            mag[np.where(cte.N == N)[0], np.where(cte.T == T)[0]] = data[0]
            en[np.where(cte.N == N)[0], np.where(cte.T == T)[0]] = data[1]
            cv[np.where(cte.N == N)[0], np.where(cte.T == T)[0]] = data[2]
            corr[np.where(cte.N == N)[0], 0, np.where(cte.T == T)[0]] = data[3]
            corr[np.where(cte.N == N)[0], 1, np.where(cte.T == T)[0]] = data[4]
            corr[np.where(cte.N == N)[0], 2, np.where(cte.T == T)[0]] = data[5]
            corr[np.where(cte.N == N)[0], 3, np.where(cte.T == T)[0]] = data[6]

# Generate the graphics for the simulation if there is at least one parameter to be graphed.
if np.any(st.SIMULATION_GRAPHICS):
    print('Starting generation of graphics for the simulation')
    sim_mod.simulation_graphs(st.SIMULATION_GRAPHICS, mag, en, cv, corr)
    print('Finished generation of graphics for the simulation')

"""
########################################################################################################################
# End of the first part of the voluntary exercise, the simulation of the parameters for each N and T.
########################################################################################################################
"""

"""
########################################################################################################################
For the second part of the voluntary exercise, an analysis of the simulation will be made based on 5 parts:
1. Describe the behavior of the previous magnitudes for the range of temperatures and sizes. Compare with the exact
    result of Onsager. Describe the effect of size on each of the variables.
2. Obtain information from the literature on critical exponents and finite size theory.
3. Estimate the value of the critical point: For each value of N, obtain an estimate of the maximum of the specific
    heat, Tc(N), and study its behavior with N extrapolating to N -> inf.
4. Obtain numerically the critical exponent β of the magnetization and compare with the exact result.
5. Study the function f(i) with temperature and system size. Extract the correlation length and its characteristic
    critical exponent.
########################################################################################################################
"""

"""
########################################################################################################################
1. Describe the behavior of the previous magnitudes for the range of temperatures and sizes. Compare with the exact
    result of Onsager. Describe the effect of size on each of the variables.
########################################################################################################################
"""
# Generate the data for the Onsager analysis if it is set to be done.
if st.ONSAGER_DATA:
    print('Generating Onsager data for the analysis')
    ons_mod.data(cte.T_ext.copy())
    print('Finished generating Onsager data for the analysis')

# Make the analysis of the magnitudes and compares them with the exact result of Onsager.
if st.ONSAGER:
    print('Starting analysis of magnitudes and comparison with Onsager')
    an_mod.onsager(en, cv, corr)
    print('Finished analysis of magnitudes and comparison with Onsager')
else:
    print('Omitting analysis of magnitudes and comparison with Onsager')

"""
########################################################################################################################
2. Obtain information from the literature on critical exponents and finite size theory.
########################################################################################################################
"""
# This part is only theoretical, no operations are performed.

"""
########################################################################################################################
3. Estimate the value of the critical point: For each value of N, obtain an estimate of the maximum of the specific
    heat, Tc(N), and study its behavior with N extrapolating to N -> inf.
########################################################################################################################
"""
# Calculate the critical temperature and the maximum specific heat for each N. This is done outside the if because the
# critical temperature is necessary for the calculation of the critical exponent.
max_T_cv = np.zeros((2, len(cte.N)))
for i in range(len(cte.N)):
    max_T_cv[0, i], max_T_cv[1, i] = an.critical_temperature(i)

# Make the analysis of the critical temperature and the maximum specific heat for each N. Remember that it compares
# the critical temperature with the exact value of Onsager, so the Onsager data must be generated before this part.
if st.CRITICAL_TEMPERATURE:
    print('Starting analysis of critical temperature and maximum specific heat')
    an_mod.critical_temperature(max_T_cv)
    print('Finished analysis of critical temperature and maximum specific heat')
else:
    print('Omitting analysis of critical temperature and maximum specific heat')

"""
########################################################################################################################
4. Obtain numerically the critical exponent β of the magnetization and compare with the exact result.
########################################################################################################################
"""
# Make the calculation and analysis of the critical exponent of the magnetization.
if st.CRITICAL_EXPONENT:
    print('Starting analysis of critical exponent of the magnetization')
    an_mod.critical_exponent(mag, max_T_cv)
    print('Finished analysis of critical exponent of the magnetization')
else:
    print('Omitting analysis of critical exponent of the magnetization')

"""
########################################################################################################################
5. Study the function f(i) with temperature and system size. Extract the correlation length and its characteristic
    critical exponent.
########################################################################################################################
"""
# Make the calculation and analysis of the correlation length and its characteristic critical exponent.
if st.CORRELATION:
    print('Starting analysis of correlation length and exponent of the correlation function')
    an_mod.correlation(corr, max_T_cv)
    print('Finished analysis of correlation length and exponent of the correlation function')
else:
    print('Omitting analysis of correlation length and exponent of the correlation function')
