"""
INPUT CLASSES
"""


class InputData:
    """Class compiling input data to be passed into analysis"""
    def __init__(self, name, pipe, process, environment):
        self.name = name
        self.pipe = pipe
        self.process = process
        self.environment = environment


class Pipe:
    """Class compiling pipe data"""
    def __init__(self, t_sel, D_o, t_corr, f_tol, f_0, material):
        self.t_sel = t_sel
        self.D_o = D_o
        self.t_corr = t_corr
        self.f_tol = f_tol
        self.f_0 = f_0
        self.material = material

    def thin_wall_check(self, t):
        """Number [m] -> Bool
        Returns True if thin wall and False if thick wall"""
        return self.D_o/t >= 20


class Environment:
    """Class compiling environmental data"""
    def __init__(self, d, T_a=4, rho_w=1025, g=9.81):
        self.d = d
        self.T_a = T_a
        self.rho_w = rho_w
        self.g = g

    def hydro_pressure(self):
        '''-> Number [Pa]
        Calculate the hydrostatic external pressure at water depth'''
        return self.rho_w*self.g*self.d


class Process:
    """Class compiling process data"""
    def __init__(self, T_d, P_d, T_t):
        self.T_d = T_d
        self.P_d = P_d
        self.T_t = T_t


if __name__ == "__main__":  #pragma: no cover
    pass
