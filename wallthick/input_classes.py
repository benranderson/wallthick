"""
INPUT CLASSES
"""
import scipy.constants
from input_data_files import db_materials


class InputData:
    """Class compiling input data to be passed into analysis"""

    def __init__(self, name, pipe, process, environment):
        self.name = name
        self.pipe = pipe
        self.process = process
        self.environment = environment


class Pipe:
    """Class compiling pipe data"""

    def __init__(self, t_sel, D_o, t_corr, f_tol, f_0, B, material, t_coat):
        self.t_sel = t_sel
        self.D_o = D_o
        self.t_corr = t_corr
        self.f_tol = f_tol
        self.f_0 = f_0
        self.B = B
        self.material = material
        self.t_coat = t_coat

    def thin_wall_check(self, t):
        """Number [m] -> Bool
        Returns True if thin wall and False if thick wall"""
        return self.D_o/t >= 20


class Environment:
    """Class compiling environmental data"""

    def __init__(self, d_max, d_min, T_a=4, rho_w=1025, g=scipy.constants.g):
        self.d_max = d_max
        self.d_min = d_min
        self.T_a = T_a
        self.rho_w = rho_w
        self.g = g

    def hydro_pressure(self, d):
        """-> Number [Pa]
        Calculate the hydrostatic external pressure at water depth"""
        return self.rho_w*self.g*d


class Process:
    """Class compiling process data"""

    def __init__(self, T_d, P_d, h_ref, rho_d, R_reel, T_lay):
        self.T_d = T_d
        self.P_d = P_d
        self.h_ref = h_ref
        self.rho_d = rho_d
        self.R_reel = R_reel
        self.T_lay = T_lay


def read_input_data(case):
    """ Module -> InputData
    Function to initialise input classes from input case and return InputData
    object
    """

    try:
        # Retrieve database of materials
        materials = db_materials.materials

        # Initailise input objects
        pipe = Pipe(case.t_sel,
                    case.D_o,
                    case.t_corr,
                    case.f_tol,
                    case.f_0,
                    case.B,
                    materials[case.mat_p],
                    case.t_coat)

        environment = Environment(case.d_max,
                                  case.d_min,
                                  case.T_a,
                                  case.rho_w,
                                  case.g)

        process = Process(case.T_d,
                          case.P_d,
                          case.h_ref,
                          case.rho_d,
                          case.R_reel,
                          case.T_lay)

        data = InputData(case.name, pipe, process, environment)

        return data

    except TypeError:
        print("Provided input case parameter not a module")
        raise

if __name__ == "__main__":  # pragma: no cover
    pass
