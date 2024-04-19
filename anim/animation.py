import matplotlib.colors as mcolors
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Patch


def make_anim(all_s, steps, n, t, path):
    name = "ising_" + str(t) + "_" + str(n) + "x" + str(n)
    file_out = path + "/" + name  # Nombre del fichero de salida (sin extensión)
    interval = 200  # Tiempo entre fotogramas en milisegundos

    # False: muestra la animación por pantalla
    # True: la guarda en un fichero
    save_to_file = True

    dpi = 150  # Calidad del vídeo de salida (dots per inch)

    # Inicializa la lista con los datos de cada fotograma.
    # frames_data[j] contiene los datos del fotograma j-ésimo
    frames_data = list()

    for i in range(steps + 1):
        frames_data.append(all_s[i].reshape(n, n).copy())

    # Crea los objetos figure y axis
    fig, ax = plt.subplots()

    # Define el rango de los ejes
    ax.axis("off")

    # Agrega una línea de borde alrededor del cuadrado grande
    # ax.plot([-0.5, n - 0.5, n - 0.5, -0.5, -0.5],
    #         [-0.5, -0.5, n - 0.5, n - 0.5, -0.5],
    #         color='black')

    # Crear un mapa de colores personalizado
    cmap = mcolors.ListedColormap(['grey', 'black'])
    bounds = [-1, 0, 1]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # Crear los objetos Patch para la leyenda
    legend_elements = [Patch(facecolor='grey', edgecolor='k', label='-1'),
                       Patch(facecolor='black', edgecolor='k', label='1')]

    # Añadir la leyenda a los ejes
    ax.legend(handles=legend_elements, loc='upper right')

    # Representa el primer fotograma
    im = ax.imshow(frames_data[0], cmap=cmap, vmin=-1, vmax=+1)

    # Calcula el nº de frtogramas o instantes de tiempo
    nframes = len(frames_data)

    # Si hay más de un instante de tiempo, genera la animación
    if nframes > 1:
        animation = FuncAnimation(
            fig, update,
            fargs=(frames_data, im), frames=nframes, blit=True, interval=interval)

        # Muestra por pantalla o guarda según parámetros
        if save_to_file:
            animation.save("{}.mp4".format(file_out), dpi=dpi)
        else:
            plt.show()
    # En caso contrario, muestra o guarda una imagen
    else:
        # Muestra por pantalla o guarda según parámetros
        if save_to_file:
            fig.savefig("{}.pdf".format(file_out))
        else:
            plt.show()


# Función que actualiza la configuración del sistema en la animación
def update(j_frame, frames_data1, im1):
    # Actualiza el gráfico con la configuración del sistema
    im1.set_data(frames_data1[j_frame])

    return im1,
