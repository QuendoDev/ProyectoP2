import os
import setup.initial_conditions as ic


def init_files():
    direction = 'C:/Users/euget/Downloads/Fisica Computacional/P2 - Modelo de Ising/Proyecto P2'
    result_name = 'Resultado'
    ex1_name = 'Ejercicio 1'
    ex2_name = 'Ejercicio 2'

    try:
        os.mkdir(os.path.join(direction, result_name))
    except FileExistsError:
        pass

    res_dir = os.path.join(direction, result_name)

    try:
        os.mkdir(os.path.join(res_dir, ex1_name))
    except FileExistsError:
        pass

    ex1_dir = os.path.join(res_dir, ex1_name)

    try:
        os.mkdir(os.path.join(res_dir, ex2_name))
    except FileExistsError:
        pass

    ex2_dir = os.path.join(res_dir, ex2_name)

    try:
        for n in ic.N:
            os.mkdir(os.path.join(ex1_dir, str(n) + 'x' + str(n)))
    except FileExistsError:
        pass

    return ex1_dir, ex2_dir
