import numpy as np
import time
import results.result_printer as rs
import setup.initial_conditions as ic
import calc.montecarlo as mc
import setup.settings as st
import anim.animation as an
import calc.parameters as cp
import matplotlib.pyplot as plt
import gc
import os


def ex1(path):
    for n in ic.N:
        for t in ic.T_1:
            # Variable para calcular el tiempo de ejecucion
            te_start = time.time()

            # Se inicializa la configuracion inicial
            #s = np.random.choice([-1, 1], (n, n))
            s = np.random.choice([-1, 1], (n ** 2))
            s_0 = s.copy()

            # Se inicializa la matriz que contendrá todas las configuraciones generadas
            #s_all = np.empty((ic.CYCLES, n, n))
            s_all = np.empty((ic.CYCLES, n ** 2))
            s_all[0] = s.copy()

            # Se declara la condicion de equilibrio, si todos los espines son iguales,
            # se considera que la configuracion ya esta en equilibrio.
            eq = False
            steps = 0

            # Se realiza el algoritmo de metropolis y se guardan todas las configuraciones
            for i in range(ic.CYCLES):
                if i == 0:
                    continue
                if eq:
                    break

                s = mc.step(t, s.copy(), n)
                s_all[i] = s.copy()

                # Se verifica si la configuracion ya esta en equilibrio viendo si la matriz s_all en la posicion i
                # solo tiene elementos 1 o -1
                if cp.converged(s_all[i], s_all[i - 1], n):
                    steps = i
                    eq = True

            # Se calcula el tiempo de ejecucion
            te_end = time.time()
            te = te_end - te_start

            # Variable para pasar a la funcion como el tiempo de animacion
            ta = 0

            # Modulo de la animacion
            if st.anim:
                # Variable para calcular el tiempo de animacion
                ta_start = time.time()
                # Se realiza la animacion
                an.make_anim(s_all, steps, n, t, os.path.join(path, str(n) + 'x' + str(n)))

                # Se calcula el tiempo de animacion
                ta_end = time.time()
                ta = ta_end - ta_start

            # Se guardan los datos de la simulacion
            rs.ising_info(n, t, steps, te, ta, s_0, os.path.join(path, str(n) + 'x' + str(n)))

            print(n, t, steps, te, ta)

            # Limpia la memoria
            del s_all
            gc.collect()


def ex2(path):
    mag = np.zeros(len(ic.T_2))
    i = 0
    for t in ic.T_2:
        Z = 0
        mag_prom = 0
        beta = 1 / t
        s = np.random.choice([-1, 1], (ic.N_CALC, ic.N_CALC))
        s_0 = s.copy()
        for i in range(ic.CYCLES):
            if i % 100 == 0:
                magnetization = cp.magnetization(s)
                energy = cp.energy(s, ic.N_CALC)
                param = np.exp(-beta * energy)
                Z += param
                mag_prom += param * magnetization

            s = mc.step(t, s.copy(), ic.N_CALC)

        mag_t = mag_prom / Z
        mag[i] = mag_t
        rs.ising_results(t, beta, ic.N_CALC, mag_t, Z, s_0, path)

    if st.graph:
        fig, ax = plt.subplots()
        # TODO

# if st.calc:
#     # Se calcula la magnetizacion y la energia promedio
#     Z = 0
#     mag_prom = 0
#     for i in range(ic.CYCLES):
#         if i % 100 == 0:
#             magnetization = cp.magnetization(s_all[i])
#             energy = cp.energy(s_all[i])
#             param = np.exp(-ic.beta * energy)
#             Z += param
#             mag_prom += param * magnetization
#
#             # print('i: ', i)
#             # print('s_all[i]: ', s_all[i])
#             # print('magnetization: ', magnetization)
#             # print('energy: ', energy)
#             # print('ic.beta: ', ic.beta * energy)
#             # print('Z: ', Z)
#             # print('mag_prom: ', mag_prom)
#
#     print('Magnetizacion promedio: ', mag_prom / Z)
