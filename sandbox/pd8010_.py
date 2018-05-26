# -*- coding: utf-8 -*-

"""
Main module for wallthick.

PD 8010-2:2015

Pipeline Systems - Part 2: Subsea pipelines – Code of practice - 2015
"""
import math
import scipy.optimize
import datetime
from wallthick import dnvf101
from wallthick import api5l
from wallthick.inputs import material_dict


# General Code Information
# ========================

title = "PD 8010-2"
year = 2015


# General Calcuations
# ===================


def pressure_head(rho, g, d, h_ref):
    """
    Number [kg/m^3], Number [m/s/s], Number [m], Number [m] -> Number [Pa]

    Returns the pressure head considering the reference height relative to LAT.
    """
    return rho * g * (d + h_ref)


# 6.4.2.1 Allowable Stress
# ========================


def allowable_hoop_stress(sig_y):
    """
    Number [Pa], Number [m], Number [Pa] -> Number [m]

    Returns the allowable hoop stress.

    Equation (2)
    """
    # Hoop stress design factor from Table 2
    df_h = 0.72
    return df_h * sig_y


# 6.4.2.2 Hoop
# ============


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


def hoop_thickness_thin(P_i, P_o, D_o, sig_A):
    """
    Number [Pa], Number [Pa], Number [m], Number [Pa] -> Number [m]

    Returns the minimum wall thickness for internal pressure containment for a
    thin walled pipe.

    Equation (3)
    """
    return abs(P_i - P_o) * D_o / (2 * sig_A)


def hoop_thickness_thick(P_i, P_o, D_o, sig_A):
    """
    Number [Pa], Number [Pa], Number [m], Number [Pa] -> Number [m]

    Returns the minimum wall thickness for internal pressure containment for a
    thick walled pipe.

    Equation (5)
    """
    eq = math.sqrt((((sig_A - abs(P_i - P_o))) * D_o**2) /
                   (sig_A + abs(P_i - P_o)))
    return 0.5 * (D_o - eq)


def hoop_thickness(P_i, P_o_min, D_o, sig_A):
    """
    Number [Pa], Number [Pa], Number [m], Number [Pa] -> Number [m]

    Returns the minimum (note not nominal) wall thickness for internal pressure
    containment.

    Considers:
    - Allowable hoop stress
    - Worst case maximum pressure difference
    - Appropriate wall thickness theory, i.e. thick or thin
    """
    t_min_thin = hoop_thickness_thin(P_i, P_o_min, D_o, sig_A)

    # Select appropriate wall theory based on minimum thin wall thickness
    if D_o / t_min_thin > 20:
        t_min = t_min_thin
    else:
        t_min = hoop_thickness_thick(P_i, P_o_min, D_o, sig_A)

    return t_min


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


# G.1.4 Bending
# =============


def reeling_thickness(D_o, R_reel, t_coat):
    """
    Number [m], Number [m], Number [m] -> Number [m]

    Returns the minimum wall thickness based on Reeling Criteria - Local
    Buckling - Bending During Reeling.

    Applicable for a pipe bent around a curvature on a vessel during
    installation.
    """
    # Strain factor for reeling (based on previous project experience)
    df_s = 0.67

    if R_reel > 0:
        # Functional strain from bending around vessel reel radius
        epsilon_b = D_o / (2 * (R_reel + 0.5 * D_o + t_coat))

        # Characteristic bending strain for buckling due to bending moments
        # acting alone Equation (G.8)
        return D_o * math.sqrt(epsilon_b / (15 * df_s))
    else:
        return 0


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


def leak_test_pressure(P_d):
    """
    Number [Pa] -> Number [Pa]

    Return leak test pressure: 1.1 * MAOP (design pressure) at LAT

    Section 11.5.3
    """

    return 1.1 * P_d


class Pd8010(object):
    """
    Calculate the required wall thickness of a single walled flowline
    installed on the seabed in accordance with allowable stress design code
    PD 8010-2.

    Considers the following criteria:
    1. Reeling (if applicable)
    2. Pressure containment (bursting)
    3. Local buckling (collapse)
    4. Propagation buckling

    Also determines recommended hydrostatic strength and leak test pressures.
    """

    def __init__(self, data):
        """
        Initialise and run wall thickness calculations
        """

        # Associate input data with design calculation object
        self.f_tol = data['f_tol']
        self.B = data['B']
        self.t_corr = data['t_corr']
        self.D_o = data['D_o']
        self.material = data['material']
        self.f_0 = data['f_0']
        self.rho_w = data['rho_w']
        self.d_max = data['d_max']
        self.d_min = data['d_min']
        self.P_d = data['P_d']
        self.T_d = data['T_d']
        self.sig_y_d = data['sig_y_d']
        self.P_h = data['P_h']
        self.P_o_min = data['P_o_min']
        self.P_o_max = data['P_o_max']
        self.g = data['g']

    @property
    def sig_y_d(self):
        '''
        Return derated yield strength
        '''
        sig_y = material_dict[self.material].sig_y
        return dnvf101.derate_material(self.material, sig_y,
                                       self.T_d)

    @property
    def P_h_d(self):
        ''''
        Number [kg/m^3], Number [m/s/s], Number [m], Number [m] -> Number [Pa]

        Returns pressure head considering the reference height relative to LAT.
        Assumes minimum water depth for worst case pressure differential.
        '''
        return pressure_head(self.rho_d, self.g, self.d_min,
                             self.h_ref)

    @property
    def P_i(self):
        return self.process.P_d + self.P_h_d

    @property
    def P_o_min(self):
        return pressure_head(self.process.rho_d, self.env.g, self.env.d_min, 0)

    @property
    def P_o_max(self):
        return pressure_head(self.process.rho_d, self.env.g, self.env.d_max, 0)

    @property
    def t_r_nom(self):

        # Strain factor for reeling (based on previous project experience)
        df_s = 0.67

        if self.pipe.R_reel > 0:
            # Functional strain from bending around vessel reel radius
            epsilon_b = self.pipe.D_o / (2 * (self.pipe.R_reel +
                                              0.5 * self.pipe.D_o +
                                              self.pipe.t_coat))

            # Characteristic bending strain for buckling due to bending moments
            # acting alone Equation (G.8)
            return self.pipe.D_o * math.sqrt(epsilon_b / (15 * df_s))
        else:
            return 0

    @property
    def t_h_nom(self):
        # Hoop stress design factor from Table 2
        sig_A = 0.72 * self.sig_y_d

        t_min_thin = abs(self.process.P_i - self.P_o_min) * \
            self.pipe.D_o / (2 * sig_A)

        # Select appropriate wall theory based on minimum thin wall thickness
        if self.pipe.D_o / t_min_thin > 20:
            t_min = t_min_thin
        else:
            eq = math.sqrt((((sig_A - abs(self.P_o_min - self.P_o_min))) * self.pipe.D_o**2) /
                           (sig_A + abs(self.P_o_min - self.P_o_min)))
            t_min = 0.5 * (self.pipe.D_o - eq)

        return self.req_thickness(t_min, self.pipe.t_corr, self.pipe.f_tol)

    @property
    def t_h_nom_bt(self):
        ''' Bend thinning '''
        return self.t_h_nom / (1 - self.pipe.B)

    @staticmethod
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

    @property
    def t_c_nom(self):
        # Hydrostatic Collapse
        E = material_dict[self.pipe.material].E
        v = material_dict[self.pipe.material].v
        return collapse_thickness(self.P_o_max,
                                  self.sig_y_d,
                                  E,
                                  v,
                                  self.pipe.D_o,
                                  self.pipe.f_0)

    @property
    def t_b_nom(self):
        # Local Buckle Propagation
        return buckle_thickness(
            self.pipe.D_o, self.P_o_max, self.sig_y_d)

    @property
    def t_rec(self):
        # Recommended API 5L wall thickness
        max_t_nom = max(self.t_r_nom, self.t_h_nom,
                        self.t_h_nom_bt, self.t_c_nom,
                        self.t_b_nom)
        return api5l.recommended_wall_thickness(
            self.pipe.D_o, max_t_nom)

    @property
    def P_st(self):
        ''' Strength test pressure '''
        # Pressure head
        P_h_t = pressure_head(1025, self.env.g,
                              self.env.d_min, self.process.h_ref)
        sig_y = material_dict[self.pipe.material].sig_y
        return strength_test_pressure(self.pipe.t_sel,
                                      self.pipe.f_tol,
                                      sig_y,
                                      self.pipe.D_o,
                                      self.process.P_d,
                                      self.P_o_min,
                                      P_h_t)

    @property
    def P_lt(self):
        ''' Leak test pressure '''
        return leak_test_pressure(self.process.P_d)

    def __str__(self):
        return """{0}

Wall Thickness Design
=====================

Pipeline: {1}

Reeling Criterion:                               {2:0.2f} mm
Pressure Containment:                            {3:0.2f} mm
Pressure Containment (incl. bend thinning):      {4:0.2f} mm
Hydrostatic Collapse:                            {5:0.2f} mm
Propagation buckling:                            {6:0.2f} mm

Minimum Recommended API Wall Thickness:          {7:0.2f} mm
Selected Wall Thickness:                         {8:0.2f} mm

Strength Test Pressure:                          {9:0.2f} bar
Leak Test Pressure:                              {10:0.2f} bar
""".format(datetime.date.today(),
           "NAME...",
           1000 * self.t_r_nom,
           1000 * self.t_h_nom,
           1000 * self.t_h_nom_bt,
           1000 * self.t_c_nom,
           1000 * self.t_b_nom,
           1000 * self.t_rec,
           1000 * self.t_sel,
           1e-5 * self.P_st,
           1e-5 * self.P_lt)
