import os

import matplotlib.pyplot as plt
import numpy as np

import vol.analysis as an
import vol.constants as cts

# Generar los valores de Onsager para T_ext = np.linspace(1.5, 3.5, 100) y guardarlos en un archivo en
# Resultados/Voluntario/Analisis/Onsager/magnitud_onsager.txt o en
# Resultados/Voluntario/Analisis/Onsager/magnitud_onsager.npy.

# En las graficas, se ploteara una linea para los valores de T_ext y luego otra para los valores de T, pero como solo
# se van a hacer los calculos con la dimension de T_ext, para plotear la de T se tomaran datos de 10 pasos en 10
# pasos de T_ext.

ons_dir = ('C:/Users/euget/OneDrive/Escritorio/Fisica Computacional/P2 - Modelo de Ising/Proyecto P2/Resultado/Voluntario/'
           'Analisis/Onsager')

T = cts.T_ext.copy()

Cv_inf = np.zeros(len(T))

for i in range(len(T)):
    Cv_inf[i] = an.heat_onsager(T[i])

np.savetxt(os.path.join(ons_dir, 'cv_onsager.txt'), Cv_inf)

np.save(os.path.join(ons_dir, 'cv_onsager.npy'), Cv_inf)

# Ploteo los valores de Onsager para T = np.linspace(1.5, 3.5, 10) para cada magnitud en subplots.
fig, ax = plt.subplots()
ax.plot(T, Cv_inf)
ax.set_title('Capacidad calorífica')
ax.set_xlabel('T')
ax.set_ylabel('Cv')
plt.tight_layout()
plt.show()