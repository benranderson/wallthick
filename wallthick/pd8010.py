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
    """Returns internal pressure [Pa] due to combined design pressure and
    pressure head.

    :param P_d: Design pressure [Pa]
    :param P_h: Pressure head [Pa]
    """
    return P_d + P_h


def water_depths(h, H_t, H):
    """Returns minimum and maximum water depths [m] as a tuple.

    :param h: Water depth [m]
    :param H_t: Tide [m]
    :param H: Wave height [m]
    """
    d_min = h - (H/2)
    d_max = h + H_t + (H/2)
    return d_min, d_max


def external_pressure(rho, g, d):
    """Returns external pressure [Pa] at water depth.

    :param rho: Water density [kg/m^2]
    :param g: Acceleration of gravity [m/s^2]
    :param d: Water depth [m]
    """
    return rho * g * d


def hoop_pressure_thin(t, D_o, P_o, sig):
    """Returns the internal pressure [Pa] that induces a stress, sig, in a thin
    wall pipe of thickness t.

    PD 8010-2 Equation (3)

    :param t: Wall thickness [m]
    :param D_o: Outside diameter [m]
    :param P_o: External pressure [Pa]
    :param sig: Minimum yield strength [Pa]
    """
    return ((sig * 2 * t) / D_o) + P_o


def hoop_pressure_thick(t, D_o, P_o, sig):
    """Returns the internal pressure [Pa] that induces a stress, sig, in a thick
    walled pipe of thickness t.

    PD 8010-2 Equation (5)

    :param t: Wall thickness [m]
    :param D_o: Outside diameter [m]
    :param P_o: External pressure [Pa]
    :param sig: Minimum yield strength [Pa]
    """
    return ((sig * (D_o**2 - (D_o - 2 * t)**2)) / (D_o**2 + (D_o - 2 * t)**2)) + P_o


def hoop_thickness_thin(P_i, P_o, D_o, sig_y_d):
    """Returns the minimum wall thickness [m] for internal pressure containment
    for a thin walled pipe.

    PD 8010-2 Equation (3)

    :param P_i: Internal pressure [Pa]
    :param P_o: External pressure [Pa]
    :param D_o: Outside diameter [m]
    :param sig_y_d: Minimum yield strength [Pa]
    """
    return abs(P_i - P_o) * D_o / (2 * n_s * sig_y_d)


def hoop_thickness_thick(P_i, P_o, D_o, sig_y_d):
    """Returns the minimum wall thickness [m] for internal pressure containment
    for a thick walled pipe.

    PD 8010-2 Equation (5)

    :param P_i: Internal pressure [Pa]
    :param P_o: External pressure [Pa]
    :param D_o: Outside diameter [m]
    :param sig_y_d: Minimum yield strength [Pa]
    """
    eq = math.sqrt((((n_s*sig_y_d - abs(P_i - P_o))) * D_o**2) /
                   (n_s*sig_y_d + abs(P_i - P_o)))
    return 0.5 * (D_o - eq)


def hoop_thickness(P_i, P_o, D_o, sig_y_d):
    """Returns the minimum (note not nominal) wall thickness [m] for internal
    pressure containment.

    Considers:
    - Allowable hoop stress
    - Worst case maximum pressure difference
    - Appropriate wall thickness theory, i.e. thick or thin

    :param P_i: Internal pressure [Pa]
    :param P_o: External pressure [Pa]
    :param D_o: Outside diameter [m]
    :param sig_y_d: Minimum yield strength [Pa]
    """
    t_min_thin = hoop_thickness_thin(P_i, P_o, D_o, sig_y_d)

    # Select appropriate wall theory based on minimum thin wall thickness
    if D_o / t_min_thin > 20:
        t_min = t_min_thin
    else:
        t_min = hoop_thickness_thick(P_i, P_o, D_o, sig_y_d)

    return t_min


def req_thickness(t_min, t_corr, f_tol):
    """Returns the required wall thickness [m] based on the following mechanical
    allowances:
    - Corrosion allowance
    - Fabrication tolerance

    Extrapolated from Equation (4)

    :param t_min: Minimum wall thickness [m]
    :param t_corr: Corrosion allowance [m]
    :param f_tol: Fabrication tolerance [m]
    """
    try:
        return (t_min + t_corr) / (1 - f_tol)
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "Divide by zero. Check fabrication tolerance.")


# G.1.2 External Pressure - Hydrostatic Collapse
# ==============================================


def collapse_thickness(P_o, sig_y_d, E, v, D_o, f_0):
    """Returns the nominal wall thickness [m] for local buckling due to external
    pressure.

    Considers the worst case maximum external over pressure, i.e.:
    - Minimum internal pressure (zero)
    - Maximum external pressure (at water depth, d)

    PD 8010-2 Clause G.1.2

    :param P_o: External pressure [Pa]
    :param sig_y_d: Minimum yield strength [Pa]
    :param E: Young's modulus [Pa]
    :param v: Poisson's ratio [-]
    :param D_o: Outside diameter [m]
    :param f_0: Initial ovalisation [%]
    """

    def P_e(t):
        """Returns the critical pressure [Pa] for an elastic critical tube.

        PD 8010-2 Section G.2

        :param t: Wall thickness [m]
        """
        return 2 * E / (1 - v**2) * (t / D_o)**3

    def P_y(t):
        """Returns the yield pressure [Pa].

        PD 8010-2 Equation (G.3)

        :param t: Wall thickness [m]
        """
        return 2 * sig_y_d * (t / D_o)

    def char_resist(t):
        """Returns the characteristic resistance [m] for external pressure.

        PD 8010-2 Equation (G.1)

        :param t: Wall thickness [m]
        """
        term_1 = ((P_o / P_e(t)) - 1)
        term_2 = ((P_o / P_y(t))**2 - 1)
        return term_1 * term_2 - (P_o / P_y(t)) * f_0 * (D_o / t)

    return scipy.optimize.newton(char_resist, 1e-3)


# G.2 Propagation Buckling
# ========================


def buckle_thickness(D_o, P_p, sig_y):
    """Returns the nominal buckle thickness [m] based on the propagation
    pressure. Considers the worst case maximum external pressure and ignores
    internal pressure.

    PD 8010-2 Equation (G.21)

    :param D_o: Outside diameter [m]
    :param P_p: Propagation pressure [Pa]
    :param sig_y: Minimum yield strength [Pa]
    """
    return D_o * (P_p / (10.7 * sig_y))**(4 / 9)


# 11 Construction - Testing
# =========================


def strength_test_pressure(t_sel, f_tol, sig_y, D_o, P_d, P_o, P_h):
    """Returns the strength test pressure, i.e. the minimum of:
    - 1.5 * design pressure:
        Note that hydrostatic head is not multiplied by 1.5 (interpreted by
        last paragraph of Section 11.5.2)
    - the pressure that induces a hoop stress of 90 percent SMYS at nominal
        wall thickness.

    PD 8010-2 Section 11.5.1, Ref.1

    :param t_sel: Selected wall thickness [m]
    :param f_tol: fabrication tolerance [m]
    :param sig_y: Minimum yield strength [Pa]
    :param D_o: Outside diameter [m]
    :param P_d: Design pressure [Pa]
    :param P_h: Pressure head [Pa]
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


class Pd8010:
    """PD8010-2 Wall thickness analysis class.

    :param data: Input data dictionary
    """

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
        """Nominal wall thickness [m] to satisfy the internal pressure (hoop)
        criterion.
        """
        P_i = internal_pressure(self.P_d, self.P_h)
        # min water depth
        d, _ = water_depths(self.h, self.H_t, self.H)
        P_o = external_pressure(self.rho_w, self.g, d)
        # minimum wall thickness
        t_h_min = hoop_thickness(P_i, P_o, self.D_o, self.sig_y_d)
        # nominal wall thickness
        return req_thickness(t_h_min, self.t_corr, self.f_tol)

    @property
    def t_c(self):
        """Nominal wall thickness [m] to satisfy the hydrostatic collapse
        criterion.
        """
        # max water depth
        _, d = water_depths(self.h, self.H_t, self.H)
        # include safety factor
        P_o = self.f_s * external_pressure(self.rho_w, self.g, d)
        return collapse_thickness(
            P_o, self.sig_y_d, self.E, self.v, self.D_o, self.f_0)

    @property
    def t_b(self):
        """Nominal wall thickness [m] to satisfy the local buckle propagation
        criterion.
        """
        # max water depth
        _, d = water_depths(self.h, self.H_t, self.H)
        # propagation pressure equal to max external pressure
        P_p = external_pressure(self.rho_w, self.g, d)
        return buckle_thickness(self.D_o, P_p, self.sig_y_d)

    @property
    def P_st(self):
        """Strength test pressure [Pa].

        PD 8010-2 Section 11.5.2
        """
        # min water depth
        d, _ = water_depths(self.h, self.H_t, self.H)
        P_o = external_pressure(self.rho_w, self.g, d)
        return strength_test_pressure(self.t_sel, self.f_tol, self.sig_y,
                                      self.D_o, self.P_d, P_o, self.P_h)

    @property
    def P_lt(self):
        """Leak test pressure [Pa] at LAT.

        PD 8010-2 Section 11.5.3
        """
        return 1.1 * self.P_d
