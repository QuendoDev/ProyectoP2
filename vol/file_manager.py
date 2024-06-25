import os
import vol.constants as cte

direction = 'C:/Users/euget/OneDrive/Escritorio/Fisica Computacional/P2 - Modelo de Ising/Proyecto P2'
result_name = 'Resultado'
vol_name = 'Voluntario'


def result_folder():
    res_dir = os.path.join(direction, result_name)

    try:
        os.mkdir(res_dir)
    except FileExistsError:
        pass

    vol_dir = os.path.join(res_dir, vol_name)

    try:
        os.mkdir(vol_dir)
    except FileExistsError:
        pass

    return vol_dir


def init_files():
    result_path = result_folder()
    for n in cte.N:
        n_dir = os.path.join(result_path, str(n) + 'x' + str(n))

        try:
            os.mkdir(n_dir)
        except FileExistsError:
            pass

    an_dir = os.path.join(result_path, 'Analisis')
    try:
        os.mkdir(an_dir)
    except FileExistsError:
        pass

    an_extra_data_dir = os.path.join(an_dir, 'Datos')
    try:
        os.mkdir(an_extra_data_dir)
    except FileExistsError:
        pass

    onsager_dir = os.path.join(an_dir, 'Onsager')
    try:
        os.mkdir(onsager_dir)
    except FileExistsError:
        pass

    ons_exp_dir = os.path.join(an_dir, 'Onsager vs Exp')
    try:
        os.mkdir(ons_exp_dir)
    except FileExistsError:
        pass

    temp_dir = os.path.join(an_dir, 'Temperatura critica')
    try:
        os.mkdir(temp_dir)
    except FileExistsError:
        pass

    exp_mag_dir = os.path.join(an_dir, 'Exponente de magnetizacion')
    try:
        os.mkdir(exp_mag_dir)
    except FileExistsError:
        pass

    corr_dir = os.path.join(an_dir, 'Correlacion')
    try:
        os.mkdir(corr_dir)
    except FileExistsError:
        pass

    return result_path
