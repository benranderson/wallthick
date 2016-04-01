"""

Module containing functions to collect and return input data

"""

from wallthick.input_classes import InputData, Pipe, Environment, Process
from wallthick.input_data_files.db_materials import materials


def collect_inputs(data):
    """ Function to collect data from input file and construct the InputData
    class """

    pipe = Pipe(data.t_sel,
                data.D_o,
                data.t_corr,
                data.f_tol,
                data.f_0,
                materials[data.mat_p])

    environment = Environment(data.d,
                              data.T_a,
                              data.rho_w,
                              data.g)

    process = Process(data.T_d,
                      data.P_d,
                      data.T_t)

    input_data = InputData(data.name,
                           pipe, process, environment)

    return input_data
