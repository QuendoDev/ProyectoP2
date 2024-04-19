import numpy as np

import results.exercises as ex
import setup.settings as st
import setup.files as files

# Ejercicio 1: Para cada N, calcular las configuraciones para tres temperaturas, una baja, una media y una alta.
# Para cada temperatura, hacer un video con las configuraciones generadas para 10^6 pasos de Montecarlo (mc.step).
# Ejercicio 2: Dividir en 10 intervalos la temperatura entre 0.5 y 5. Para cada intervalo, calcular la magnetización
# promedio y la energía promedio de las configuraciones generadas para 10^6 pasos de Montecarlo (mc.step), usando
# solamente las medidas obtenidas cada 100 pasos de montecarlo, teniendo así 10^4 medidas por intervalo.

# Inicializacion de archivos
paths = files.init_files()

# Ejercicio 1:
if st.ex1:
    ex.ex1(paths[0])


# Modulo de calculo

