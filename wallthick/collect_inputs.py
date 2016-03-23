"""

Module containing functions to collect and return input data

"""

from wallthick.input_classes import InputData, Pipe, Environment, Process
from wallthick.input_data_files.db_materials import materials


def collect_inputs(input_data_file):
    """ Function to collect data from input file and construct the InputData
    class """

    pipe = Pipe(input_data_file.t_sel,
                input_data_file.D_o,
                input_data_file.t_corr,
                input_data_file.f_tol,
                input_data_file.f_0,
                materials[input_data_file.mat_p])

    environment = Environment(input_data_file.d,
                              input_data_file.T_a,
                              input_data_file.rho_w,
                              input_data_file.g)

    process = Process(input_data_file.T_d,
                      input_data_file.P_d,
                      input_data_file.T_t)

    input_data = InputData(input_data_file.name,
                           pipe, process, environment)

    return input_data
