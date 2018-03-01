# -*- coding: utf-8 -*-

"""
Main module for wallthick.

PD 8010-2:2015

Pipeline Systems - Part 2: Subsea pipelines – Code of practice - 2015
"""

import math
import scipy.optimize
import json

n_s = 0.72


def internal_pressure(P_d, P_h):
    return P_d + P_h


def water_depths(h, H_t, H):
    d_min = h - (H/2)
    d_max = h + H_t + (H/2)
    return d_min, d_max


def external_pressure(rho, g, d):
    return rho * g * d


def hoop_pressure_thin(t, D_o, P_o, sig):
    """
    Number [Pa], Number [Pa], Number [m], Number [Pa] -> Number [m]

    Returns the internal pressure that induces a stress, sig, in a thin
    wall pipe of thickness t.

    Equation (3)
    """
    return ((sig * 2 * t) / D_o) + P_o


def hoop_pressure_thick(t, D_o, P_o, sig):
    """
    Number [Pa], Number [Pa], Number [m], Number [Pa] -> Number [m]

    Returns the internal pressure that induces a stress, sig, in a thick
    walled pipe of thickness t.

    Equation (5)
    """
    return ((sig * (D_o**2 - (D_o - 2 * t)**2)) / (D_o**2 + (D_o - 2 * t)**2)) + P_o


def hoop_thickness_thin(P_i, P_o, D_o, sig_y_d):
    """
    Number [Pa], Number [Pa], Number [m], Number [Pa] -> Number [m]

    Returns the minimum wall thickness for internal pressure containment for a
    thin walled pipe.

    Equation (3)
    """
    return abs(P_i - P_o) * D_o / (2 * n_s * sig_y_d)


def hoop_thickness_thick(P_i, P_o, D_o, sig_y_d):
    """
    Number [Pa], Number [Pa], Number [m], Number [Pa] -> Number [m]

    Returns the minimum wall thickness for internal pressure containment for a
    thick walled pipe.

    Equation (5)
    """
    eq = math.sqrt((((n_s*sig_y_d - abs(P_i - P_o))) * D_o**2) /
                   (n_s*sig_y_d + abs(P_i - P_o)))
    return 0.5 * (D_o - eq)


def hoop_thickness(P_i, P_o_min, D_o, sig_y_d):
    """
    Number [Pa], Number [Pa], Number [m], Number [Pa] -> Number [m]

    Returns the minimum (note not nominal) wall thickness for internal pressure
    containment.

    Considers:
    - Allowable hoop stress
    - Worst case maximum pressure difference
    - Appropriate wall thickness theory, i.e. thick or thin
    """
    t_min_thin = hoop_thickness_thin(P_i, P_o_min, D_o, sig_y_d)

    # Select appropriate wall theory based on minimum thin wall thickness
    if D_o / t_min_thin > 20:
        t_min = t_min_thin
    else:
        t_min = hoop_thickness_thick(P_i, P_o_min, D_o, sig_y_d)

    return t_min


def req_thickness(t_min, t_corr, f_tol):
    '''
    Number [m], Number [m], Number [-] -> Number [m]

    Returns the required wall thickness based on the following mechanical
    allowances:
    - Corrosion allowance
    - Fabrication tolerance

    Exrapolated from Equation (4)
    '''
    try:
        return (t_min + t_corr) / (1 - f_tol)
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "Divide by zero. Check fabrication tolerance.")


# G.1.2 External Pressure - Hydrostatic Collapse
# ==============================================


def collapse_thickness(P_o, sig_y_d, E, v, D_o, f_0):
    """
    Number [Pa], Number [Pa], Number [Pa], Number [-], Number [m], Number [-]
    -> Number [m]

    Returns the nominal wall thickness for local buckling due to external
    pressure.

    Considers the worst case maximum external over pressure, i.e.:
    - Minimum internal pressure (zero)
    - Maximum external pressure (at water depth, d)

    (Clause G.1.2)
    """

    def P_e(t):
        """
        Number [m] -> Number [Pa]

        Returns the critical pressure for an elastic critical tube.

        Equation (G.2)
        """
        return 2 * E / (1 - v**2) * (t / D_o)**3

    def P_y(t):
        """
        Number [m] -> Number [Pa]

        Returns the yield pressure.

        Equation (G.3)
        """
        return 2 * sig_y_d * (t / D_o)

    def char_resist(t):
        """
        Number [m] -> Number [Pa]

        Returns the characteristic resistance for external pressure

        Equation (G.1)
        """
        term_1 = ((P_o / P_e(t)) - 1)
        term_2 = ((P_o / P_y(t))**2 - 1)
        return term_1 * term_2 - (P_o / P_y(t)) * f_0 * (D_o / t)

    return scipy.optimize.newton(char_resist, 1e-3)


# G.2 Propagation Buckling
# ========================


def buckle_thickness(D_o, P_p, sig_y):
    """
    Number [m], Number [Pa], Number [Pa] -> Number [m]

    Returns the nominal buckle thickness based on the propagation pressure.

    Considers the worst case maximum external pressure and ignores internal
    pressure.

    Equation (G.21)
    """
    return D_o * (P_p / (10.7 * sig_y))**(4 / 9)


# 11 Construction - Testing
# =========================


def strength_test_pressure(t_sel, f_tol, sig_y, D_o, P_d, P_o, P_h):
    """
    InputData -> Number [Pa]

    Returns the strength test pressure, i.e. the minimum of:
    - 1.5 * design pressure:
        Note that hydrostatic head is not multiplied by 1.5 (interpreted by
        last paragraph of Section 11.5.2)
    - the pressure that induces a hoop stress of 90 percent SMYS at nominal
        wall thickness.

    (Section 11.5.1, Ref.1)
    """

    # Determine nominal wall thickness (no corrosion)
    t_min = t_sel * (1 - f_tol)

    # Determine pressure that induces 90 percent SMYS using correct wall
    # theory (i.e. thick or thin)
    if D_o / t_min > 20:
        # Thin wall equation
        P_hoop = hoop_pressure_thin(t_min, D_o, P_o, 0.9 * sig_y)
    else:
        # Thick wall equation
        P_hoop = hoop_pressure_thick(t_min, D_o, P_o, 0.9 * sig_y)

    # Determine 1.5 * Design Pressure (note pressure head not multiplied by
    # 1.5)
    P_test = 1.5 * P_d + P_h

    return min(P_hoop, P_test)


class Pd8010(object):

    def __init__(self, data):
        self.t_sel = data['t_sel']
        self.f_tol = data['f_tol']
        self.B = data['B']
        self.t_corr = data['t_corr']
        self.D_o = data['D_o']
        self.sig_y = data['sig_y']
        self.sig_y_d = data['sig_y_d']
        self.v = data['v']
        self.E = data['E']
        self.f_0 = data['f_0']
        self.rho_w = data['rho_w']
        self.h = data['h']
        self.H_t = data['H_t']
        self.H = data['H']
        self.P_d = data['P_d']
        self.P_h = data['P_h']
        self.g = data['g']
        self.f_s = data['f_s']

    @property
    def t_h(self):
        P_i = internal_pressure(self.P_d, self.P_h)
        # min water depth
        d, _ = water_depths(self.h, self.H_t, self.H)
        P_o = external_pressure(self.rho_w, self.g, d)
        t_h_min = hoop_thickness(P_i, P_o, self.D_o, self.sig_y_d)
        return req_thickness(t_h_min, self.t_corr, self.f_tol)

    @property
    def t_c(self):
        P_i = internal_pressure(self.P_d, self.P_h)
        # max water depth
        _, d = water_depths(self.h, self.H_t, self.H)
        # include safety factor
        P_o = self.f_s * external_pressure(self.rho_w, self.g, d)
        return collapse_thickness(
            P_o, self.sig_y_d, self.E, self.v, self.D_o, self.f_0)

    @property
    def t_b(self):
        # max water depth
        _, d = water_depths(self.h, self.H_t, self.H)
        # propagation pressure equal to max external pressure
        P_p = external_pressure(self.rho_w, self.g, d)
        return buckle_thickness(self.D_o, P_p, self.sig_y_d)

    @property
    def P_st(self):
        ''' Strength test pressure '''
        # min water depth
        d, _ = water_depths(self.h, self.H_t, self.H)
        P_o = external_pressure(self.rho_w, self.g, d)
        return strength_test_pressure(self.t_sel, self.f_tol, self.sig_y,
                                      self.D_o, self.P_d, P_o, self.P_h)

    @property
    def P_lt(self):
        """
        Return leak test pressure: 1.1 * MAOP (design pressure) at LAT

        Section 11.5.3
        """
        return 1.1 * self.P_d
