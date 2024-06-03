import numpy as np
import os
import matplotlib.pyplot as plt

import vol.analysis as an
import vol.constants as cts

# Generar los valores de Onsager para T_ext = np.linspace(1.5, 3.5, 100) y guardarlos en un archivo en
# Resultados/Voluntario/Analisis/Onsager/magnitud_onsager.txt o en
# Resultados/Voluntario/Analisis/Onsager/magnitud_onsager.npy.

# En las graficas, se ploteara una linea para los valores de T_ext y luego otra para los valores de T, pero como solo
# se van a hacer los calculos con la dimension de T_ext, para plotear la de T se tomaran datos de 10 pasos en 10
# pasos de T_ext.

ons_dir = ('C:/Users/euget/Downloads/Fisica Computacional/P2 - Modelo de Ising/Proyecto P2/Resultado/Voluntario/'
           'Analisis/Onsager')

E_inf = np.zeros(len(cts.T))
Cv_inf = np.zeros(len(cts.T))
corr_first_inf = np.zeros(len(cts.T))
corr_second_inf = np.zeros(len(cts.T))

for i in range(len(cts.T)):
    E_inf[i] = an.energy_onsager(cts.T[i])
    Cv_inf[i] = an.heat_onsager(cts.T[i])
    corr_first_inf[i] = an.corr_onsager(cts.T[i], cts.i[0])
    corr_second_inf[i] = an.corr_onsager(cts.T[i], cts.i[1])

np.savetxt(os.path.join(ons_dir, 'e_onsager.txt'), E_inf)
np.savetxt(os.path.join(ons_dir,'cv_onsager.txt'), Cv_inf)
np.savetxt(os.path.join(ons_dir,'corr_first_onsager.txt'), corr_first_inf)
np.savetxt(os.path.join(ons_dir,'corr_second_onsager.txt'), corr_second_inf)

np.save(os.path.join(ons_dir,'e_onsager.npy'), E_inf)
np.save(os.path.join(ons_dir,'cv_onsager.npy'), Cv_inf)
np.save(os.path.join(ons_dir,'corr_first_onsager.npy'), corr_first_inf)
np.save(os.path.join(ons_dir,'corr_second_onsager.npy'), corr_second_inf)

# Ploteo los valores de Onsager para T = np.linspace(1.5, 3.5, 10) para cada magnitud en subplots.
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
axs[0, 0].plot(cts.T, E_inf)
axs[0, 0].set_title('Energía')
axs[0, 0].set_xlabel('T')
axs[0, 0].set_ylabel('Energía')
axs[0, 1].plot(cts.T, Cv_inf)
axs[0, 1].set_title('Capacidad calorífica')
axs[0, 1].set_xlabel('T')
axs[0, 1].set_ylabel('Cv')
axs[1, 0].plot(cts.T, corr_first_inf)
axs[1, 0].set_title('Correlación 1')
axs[1, 0].set_xlabel('T')
axs[1, 0].set_ylabel('Correlación 1')
axs[1, 1].plot(cts.T, corr_second_inf)
axs[1, 1].set_title('Correlación 3')
axs[1, 1].set_xlabel('T')
axs[1, 1].set_ylabel('Correlación 3')
plt.tight_layout()
plt.show()


