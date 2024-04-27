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

            # Se calcula el vector de probabilidades sabiendo que la variacion de energía solo puede tomar
            # los valores -8, -4, 0, 4, 8.
            p = np.zeros(5)
            for i in range(5):
                v = 4 * i - 8
                p[i] = np.exp(-v / t)

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

                s = mc.step(s.copy(), n, p)
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
    time0 = time.time()
    mag_proms = np.zeros(len(ic.T_2))
    s_0 = np.random.choice([-1, 1], (ic.N_CALC, ic.N_CALC))
    mag = np.zeros(ic.CYCLES // ic.STEP)
    for k in range(len(ic.T_2)):

        time1 = time.time()
        time2 = 0
        time3 = 0
        time4 = 0

        t = ic.T_2[k]
        Z = 0
        mag_prom = 0
        beta = 1 / t

        s = s_0.copy()

        p = np.zeros(5)
        for i in range(5):
            v = 4 * i - 8
            p[i] = np.exp(-v / t)

        for i in range(ic.CYCLES):
            if i % ic.STEP == 0:
                mag[i // ic.STEP] = cp.magnetization(s)

            s = mc.step_matrix(s, ic.N_CALC, p)

            if i == ic.CYCLES // 4:
                time2 = time.time()
                print(t, '25%', str(time2 - time1) + ' s', str(time2 - time1) + ' s')
            elif i == ic.CYCLES // 2:
                time3 = time.time()
                print(t, '50%', str(time3 - time1) + ' s', str(time3 - time2) + ' s')
            elif i == ic.CYCLES // 4 * 3:
                time4 = time.time()
                print(t, '75%', str(time4 - time1) + ' s', str(time4 - time3) + ' s')

        final_time = time.time() - time1
        print(t, '100%', str(final_time) + ' s', str(time.time() - time4) + ' s')
        mag_t = np.mean(mag)
        mag_proms[k] = mag_t
        rs.ising_results(t, beta, ic.N_CALC, mag_t, Z, s_0, final_time, path)

    print('Total time: ', time.time() - time0)

    if st.separate_process:
        np.save(os.path.join(path, 'mag'), mag)

        # Limpia la memoria
        del mag
        gc.collect()

    if st.graph:
        if st.separate_process:
            # Se obtiene la magnetizacion promedio del archivo .npy guardado
            mag = np.load(os.path.join(path, 'mag.npy'))

        # Se grafica la magnetizacion promedio vs T
        fig, ax = plt.subplots()

        ax.plot(ic.T_2, mag_proms,
                color='red',
                marker='o', markersize=2,
                label='Magnetizacion promedio')

        ax.set_xlabel('T')
        ax.set_ylabel('<m>')

        ax.set_title('Magnetizacion promedio vs T')
        ax.legend(loc='lower left')

        plt.savefig(os.path.join(path, 'graph_' + str(ic.N_CALC) + 'x' + str(ic.N_CALC) + '.jpg'), dpi=300)
        plt.show()
