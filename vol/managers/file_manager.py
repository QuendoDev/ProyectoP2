import os
import vol.setup.constants as cte

"""
result_folder function
Creates the folder where the results of the simulations will be saved. As the complete project has two parts, one
mandatory and one voluntary, the results of the simulations are saved in two different folders. This module is only
used in the voluntary part of the project, so it creates the folder for the voluntary part of the project in the
results folder (the common folder for both parts of the project). If the folder already exists, it does nothing.
"""


def result_folder():
    # Path to the results folder of the entire project.
    res_dir = cte.RESULTS_PATH

    # Create the folder of the results of the entire project if it does not exist.
    try:
        os.mkdir(res_dir)
    except FileExistsError:
        pass

    # Path to the main folder of the voluntary part of the project.
    vol_dir = cte.VOL_PATH

    # Create the main folder of the voluntary part of the project if it does not exist.
    try:
        os.mkdir(vol_dir)
    except FileExistsError:
        pass


"""
init_files function
Creates the folders where the results of the simulations and the analysis of those results will be saved. It creates
subfolders for the different parts of the analysis of the results of the simulations. If the folders already exist, it
does nothing.
"""


def init_files():
    # Path to the folder where the results of the simulations will be saved.
    data_dir = cte.DATA_PATH

    # Create the folder where the results of the simulations will be saved if it does not exist.
    try:
        os.mkdir(data_dir)
    except FileExistsError:
        pass

    # Path to the folder where the analysis of the results of the simulations will be saved.
    an_dir = cte.ANALYSIS_PATH

    # Create the folder where the analysis of the results of the simulations will be saved if it does not exist.
    try:
        os.mkdir(an_dir)
    except FileExistsError:
        pass

    # Path to the sub-folder where the comparison between the results of the simulations and the Onsager solution will
    # be saved.
    ons_exp_dir = os.path.join(an_dir, 'Onsager vs Exp')

    # Create the sub-folder where the comparison between the results of the simulations and the Onsager solution will
    # be saved if it does not exist.
    try:
        os.mkdir(ons_exp_dir)
    except FileExistsError:
        pass

        # Path to the sub-folder where the critical temperature and specific heat analysis will be saved.
    temp_dir = os.path.join(an_dir, 'Temperatura critica')

    # Create the sub-folder where the critical temperature and specific heat analysis will be saved if it does not
    # exist.
    try:
        os.mkdir(temp_dir)
    except FileExistsError:
        pass

    # Path to the sub-folder where the exponent of the magnetization calculation and analysis will be saved.
    exp_mag_dir = os.path.join(an_dir, 'Exponente de magnetizacion')

    # Create the sub-folder where the critical exponent of the magnetization calculation and analysis will be saved if
    # it does not exist.
    try:
        os.mkdir(exp_mag_dir)
    except FileExistsError:
        pass

    # Path to the sub-folder where the critical exponent of the correlation and the correlation length calculation and
    # analysis will be saved.
    corr_dir = os.path.join(an_dir, 'Correlacion')

    # Create the sub-folder where the critical exponent of the correlation and the correlation length calculation and
    # will be saved if it does not exist.
    try:
        os.mkdir(corr_dir)
    except FileExistsError:
        pass
