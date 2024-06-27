import os
import numpy as np

import vol.calc.analysis as an
import vol.setup.constants as cts

"""
data function
It generates the values for the heat capacity of the Ising model using the Onsager exact representation. It saves the
values in a .txt file and a .npy file in the 'data' directory.

Parameters
----------
T : numpy array
    Temperatures to calculate the heat capacity.
"""


def data(T):
    # Path for the directory to save the data.
    ons_dir = cts.DATA_PATH

    # Array to save the values of the heat capacity.
    Cv_inf = np.zeros(len(T))

    # Calculation of the heat capacity for each temperature.
    for i in range(len(T)):
        Cv_inf[i] = an.heat_onsager(T[i])

    # Save the values of the heat capacity in a .txt file and a .npy file.
    np.savetxt(os.path.join(ons_dir, 'cv_onsager.txt'), Cv_inf)
    np.save(os.path.join(ons_dir, 'cv_onsager.npy'), Cv_inf)

