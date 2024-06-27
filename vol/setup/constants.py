import numpy as np
import os

# Number of cycles of Monte Carlo for the simulation.
CYCLES = 1000000
# Number of cycles to save the parameters.
STEP = 100
# Number of saved parameters.
DIV = CYCLES // STEP
# Sizes of the lattice.
N = np.array([16, 32, 64, 128])
# Temperatures to simulate.
T = np.linspace(1.5, 3.5, 10)
# Temperatures used in the Onsager exact representation.
T_ext = np.linspace(1.5, 3.5, 100)
# Values of i for the correlation function.
i = np.array([1, 3, 5, 7])
# Colors for the plots of the parameters, one for each N.
COLORS = np.array(['b', 'g', 'r', 'c'])

# Critical temperature of the Ising model by Onsager.
T_c_onsager = 2 / np.log(1 + np.sqrt(2))
# Theoretical value of the critical exponent of the magnetization.
beta_t = 1 / 8
# Theoretical value of the critical exponent of the correlation function.
eta_t = 1 / 4

# Paths to the results of the simulation. RESULTS_PATH, VOL_PATH, ANALISIS_PATH, and DATA_PATH are created if they do
# not exist. The DIR path must be changed to the user's path.
DIR = os.path.normpath('C:/Users/euget/OneDrive/Escritorio/Fisica Computacional/P2 - Modelo de Ising/Proyecto P2')
RESULTS_PATH = os.path.join(DIR, 'Resultado')
VOL_PATH = os.path.join(RESULTS_PATH, 'Voluntario')
DATA_PATH = os.path.join(VOL_PATH, 'Datos')
ANALYSIS_PATH = os.path.join(VOL_PATH, 'Analisis')
