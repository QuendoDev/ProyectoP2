import os
import numpy as np

import vol.setup.constants as cte

"""
correlation_results function
This function writes the correlation results in a file, with the correlation values, the xi values and the eta values
with their mean and error.

Parameters:
----------
xi: numpy array
    The xi values for each size and temperature.
eta: numpy array
    The eta values for each size and temperature.
eta_mean: float
    The mean of the eta values.
eta_mean_err: float
    The error of the mean of the eta values.
path: string
    The path where the file will be saved.
"""


def correlation_results(xi, eta, eta_mean, eta_mean_err, path):
    name = "correlation.txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nCorrelation information:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nUsed lengths:\n')
        np.savetxt(f, cte.i, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nUsed sizes:\n')
        np.savetxt(f, cte.N, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTheoretical eta:\n')
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
        f.write('\nMean eta:\n')
        f.write(str(eta_mean) + '+-' + str(eta_mean_err) + '\n')
        f.write('\n----------------------------------------------------------------\n')


"""
critical_exponent_results function
This function writes the critical exponent results in a file, with the beta values, the mean of the beta values and
the error of the mean.

Parameters:
----------
beta: numpy array
    The beta values for each size.
beta_mean: float
    The mean of the beta values.
beta_mean_err: float
    The error of the mean of the beta values.
path: string
    The path where the file will be saved.
"""


def critical_exponent_results(beta, beta_mean, beta_mean_err, path):
    name = "critical_exponent.txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nCritical exponent of magnetization information:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nUsed sizes:\n')
        np.savetxt(f, cte.N, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nTheoretical beta:\n')
        f.write(str(cte.beta_t) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        np.savetxt(f, beta, fmt='%s +- %s', delimiter=', ', newline='\n',
                   header='\nBetas:\n', comments='',
                   footer='\n----------------------------------------------------------------\n')
        f.write('\nMean beta:\n')
        f.write(str(beta_mean) + '+-' + str(beta_mean_err) + '\n')
        f.write('\n----------------------------------------------------------------\n')


"""
critical_temperature_results function
This function writes the critical temperature results in a file, with the critical temperatures, the maximum Cv values,
the theoretical Onsager temperature and Cv, and the analytical representation of the critical temperature and Cv.

Parameters:
----------
max_T_cv: numpy array
    The critical temperatures and the maximum Cv values.
cv_onsager: float
    The theoretical Cv value at the Onsager temperature.
max_T: float
    The analytical representation of the critical temperature.
max_Cv: float
    The analytical representation of the maximum Cv value.
path: string
    The path where the file will be saved.
"""


def critical_temperature_results(max_T_cv, cv_onsager, max_T, max_Cv, path):
    name = "critical_temperature.txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nCritical temperature information:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nUsed sizes:\n')
        np.savetxt(f, cte.N, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nOnsager temperature (theoretical):\n')
        f.write(str(cte.T_c_onsager) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nHeat capacity at Onsager temperature (theoretical):\n')
        f.write(str(cv_onsager) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nCritical temperatures:\n')
        np.savetxt(f, max_T_cv[0], fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nMaximum specific heats:\n')
        np.savetxt(f, max_T_cv[1], fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nCritical temperature of the analytic representation:\n')
        f.write(str(max_T) + '\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nMaximum specific heat of the analytic representation:\n')
        f.write(str(max_Cv) + '\n')
        f.write('\n----------------------------------------------------------------\n')


"""
onsager_results function
This function writes the Onsager results in a file, with the Onsager Cv values.

Parameters:
----------
Cv_inf: numpy array
    The Onsager Cv values.
path: string
    The path where the file will be saved.
"""


def onsager_results(Cv_inf, path):
    name = "onsager.txt"

    with open(os.path.join(path, name), 'w') as f:
        f.write('----------------------------------------------------------------\n')
        f.write('\nOnsager results information:\n')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nUsed temperatures:\n')
        np.savetxt(f, cte.T_ext, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
        f.write('\nOnsager specific heat:\n')
        np.savetxt(f, Cv_inf, fmt='%f')
        f.write('\n----------------------------------------------------------------\n')
