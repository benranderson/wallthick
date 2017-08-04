"""
INPUT CLASSES
"""
import scipy.constants as constants


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
        return self.D_o / t >= 20


class Process:
    """Class compiling process data"""

    def __init__(self, T_d, P_d, h_ref, rho_d, R_reel, T_lay):
        self.T_d = T_d
        self.P_d = P_d
        self.h_ref = h_ref
        self.rho_d = rho_d
        self.R_reel = R_reel
        self.T_lay = T_lay


class Environment:
    """Class compiling environmental data"""

    def __init__(self, d_max, d_min, T_a=4, rho_w=1025, g=constants.g):
        self.d_max = d_max
        self.d_min = d_min
        self.T_a = T_a
        self.rho_w = rho_w
        self.g = g
