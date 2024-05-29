import numpy as np

CYCLES = 1000000
STEP = 100
DIV = CYCLES // STEP
N = np.array([16, 32, 64, 128])
T = np.linspace(1.5, 3.5, 10)
T_ext = np.linspace(1.5, 3.5, 100)
i = np.array([1, 3])
COLORS = np.array(['b', 'g', 'r', 'c'])

T_c_onsager = 2 / np.log(1 + np.sqrt(2))
beta_t = 1 / 8
eta_t = 1 / 4
