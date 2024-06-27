import numpy as np

########################################################################################################################
# Settings for the simulation. Here we can choose what parts of the simulation and of the analysis we want to run.
########################################################################################################################
# If we want to simulate the parameters for each N and T or load them from a .npy file.
SIMULATE = False

# Maximum number of workers for the parallelization of the simulation.
MAX_WORKERS = 10

# If we want to generate the graphics for the simulation. Here we have a lot of possibilities, and it follows the
# following format: each position of the array corresponds to a parameter, and if it is True, the graph of that
# parameter is generated.
# The order of the parameters is the following: magnetization, energy, specific heat, correlation for i = 1, 3, 5, 7.
# If they are all False, the graphing part of the simulation will be omitted.
# Recommended configurations are two of the following:
# - SIMULATION_GRAPHICS = np.array([False, True, True, True, True, False, False]) to generate the graphics just for the
#   parameters that are going to be analyzed in the second part of the voluntary exercise. RECOMMENDED.
# - SIMULATION_GRAPHICS = np.array([True, True, True, True, True, True, True]) to generate the graphics for all the
#   parameters, even those that are only used in intermediate calculations.
SIMULATION_GRAPHICS = np.array([False, True, True, True, True, False, False])

# Maximum number of graphics per row (number of columns).
COLS = 2

# If we want to generate the Onsager analytical function data.
ONSAGER_DATA = False

# If we want to analyze the behavior of the magnitudes and compare them with the exact result of Onsager.
ONSAGER = True

# If we want to analyze the critical temperature and the maximum specific heat for each N.
CRITICAL_TEMPERATURE = True

# If we want to calculate and analyze the critical exponent of the magnetization.
CRITICAL_EXPONENT = True

# If we want to analyze the correlation length and its characteristic critical exponent.
CORRELATION = True
