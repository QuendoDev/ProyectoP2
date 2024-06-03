import numpy as np

import vol.analysis as an
import vol.constants as cte
import vol.file_manager as fm
import vol.modules.analisis_module as an_mod
import vol.modules.simulation_module as sim_mod

########################################################################################################################
# Se quieren calcular una lista de parametros para cada N en [16, 32, 64, 128], representando para cada temperatura
# en [1.5, 3.5] con 10 valores. Los parametros que se quieren calcular son:
# - La magnetizacion promedio
# - La energia media
# - El calor especifico
# - La funcion de correlacion

# Para esto, se genera una configuracion inicial de espines todos ordenadors (s[i, j] = 1 para cualquier i, j), y se
# deja evolucionar el sistema 1000000 ciclos, guardando los resultados cada 100 ciclos. Cada resultado se guarda en una
# posicion del array correspondiente al parametro que se esta calculando y al final del bucle, se le hace la media a ese
# array para obtener el valor promedio de ese parametro. Si hay que hacer algun calculo mas usando escalares o ctes
# al final de la formula para obtener el valor final que se pide, se hace al finalizar el bucle para ahorrar calculos.

# Por ultimo, se guardan los resultados en un archivo de texto con el nombre de los parametros que se han calculado y se
# generan las graficas correspondientes.

# El profesor ha puntualizado que la magnetizacion no hay que ponerla ya que estaba incluida en el obligatorio, pero en
# el analisis que hay que hacer en la segunda parte del voluntario, se pide que se haga un analisis del exponente
# critico de esta, por lo que se ha creado un modulo para calcularla mediante paralelizacion para reducir el tiempo
# de calculo, ya que la simulacion como tal se empezo sin este ultimo calculo, y debido al tiempo disponible
# no se ha podido hacer una simulacion completa con este calculo incluido, sino que se ha hecho aparte con este
# metodo para poder hacer el analisis de la segunda parte del voluntario.
########################################################################################################################

########################################################################################################################
# Principio de la primera parte del ejercicio voluntario, la simulacion de los parametros para cada N y T.
########################################################################################################################

# Genero las carpetas de resultados.
result_path = fm.init_files()

# Defino si se quieren hacer los calculos de las medias de los parametros.
PROMS = False

if PROMS:
    sim_mod.sim(result_path)
else:
    print('Omitiendo calculo de promedios')

########################################################################################################################
# Fin de la primera parte del ejercicio voluntario.
########################################################################################################################


########################################################################################################################
# Para la segunda parte del ejercicio voluntario, se hará un análisis de la simulación basada en 5 partes:
# 1. Describir el comportamiento de las anteriores magnitudes para el rango de temperaturas y tamaños. Comparar
#    con el resultado exácto de Onsager. Describir el efecto del tamaño en cada una de las variables.
# 2. Obtener de la literatura información sobre exponentes críticos y teoría de tamaño finito.
# 3. Estimar el valor del punto crítico: Para cada valor de N obtener una estimación del máximo del calor específico,
#    Tc(N), y estudiar su comportamiento con N extrapolando para N -> inf.
# 4. Obtener numéricamente el exponente crítico β de la magnetización y comparar con el resultado exacto.
# 5. Estudiar de la función f(i) con la temperatura y el tamaño del sistema. Extraer la longitud de correlación y su
#    exponente crítico característico.
########################################################################################################################

# Defino que pasos se quieren realizar.
ONSAGER = True
CRITICAL_TEMPERATURE = True
CRITICAL_EXPONENT = True
CORRELATION = False

########################################################################################################################
# 1. Describir el comportamiento de las anteriores magnitudes para el rango de temperaturas y tamaños. Comparar
# con el resultado exácto de Onsager. Describir el efecto del tamaño en cada una de las variables.
########################################################################################################################
if ONSAGER:
    print('Empezando analisis de magnitudes y comparacion con Onsager')
    an_mod.onsager(result_path)
    print('Finalizado analisis de magnitudes y comparacion con Onsager')
else:
    print('Omitiendo analisis de magnitudes y comparacion con Onsager')

########################################################################################################################
# 2. Obtener de la literatura información sobre exponentes críticos y teoría de tamaño finito.
########################################################################################################################
# Apartado unicamente teorico, no se realiza ninguna operacion.


########################################################################################################################
# 3. Estimar el valor del punto crítico: Para cada valor de N obtener una estimación del máximo del calor específico,
# Tc(N), y estudiar su comportamiento con N extrapolando para N -> inf:
########################################################################################################################
# Calculo la temperatura crítica y el calor específico máximo para cada N. Hago esto fuera del if porque la temperatura
# crítica es necesaria para el cálculo del exponente crítico.
max_T_cv = np.zeros((2, len(cte.N)))
for i in range(len(cte.N)):
    max_T_cv[0, i], max_T_cv[1, i] = an.critical_temperature(i)

if CRITICAL_TEMPERATURE:
    print('Empezando analisis de temperatura crítica y calor específico máximo')
    an_mod.critical_temperature(result_path, max_T_cv)
    print('Finalizado analisis de temperatura crítica y calor específico máximo')
else:
    print('Omitiendo analisis de temperatura crítica y calor específico máximo')

########################################################################################################################
# 4. Obtener numéricamente el exponente crítico β de la magnetización y comparar con el resultado exacto.
########################################################################################################################
if CRITICAL_EXPONENT:
    print('Empezando analisis de exponente crítico de la magnetización')
    an_mod.critical_exponent(result_path, max_T_cv)
    print('Finalizado analisis de exponente crítico de la magnetización')
else:
    print('Omitiendo analisis de exponente crítico de la magnetización')

########################################################################################################################
# 5. Estudiar de la función f(i) con la temperatura y el tamaño del sistema. Extraer la longitud de correlación y su
# exponente crítico característico.
########################################################################################################################
if CORRELATION:
    print('Empezando analisis de longitud de correlación y exponente crítico de la función de correlación')
    an_mod.correlation(result_path, max_T_cv)
    print('Finalizado analisis de longitud de correlación y exponente crítico de la función de correlación')
else:
    print('Omitiendo analisis de longitud de correlación y exponente crítico de la función de correlación')
