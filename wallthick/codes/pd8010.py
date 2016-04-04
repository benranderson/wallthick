"""
PD 8010-2:2015
Pipeline Systems - Part 2: Subsea pipelines – Code of practice
"""
import math
import scipy.optimize

"""
General information
===================
"""

title = "PD 8010-2"
year = 2015

"""
Table 2 - Design Factors
========================
"""

# Hoop Stress
df_h = 0.72

# Equivalent stress
df_e = {'Temporary': 1.0,
        'Operational': 0.96}

"""
6.4.2.1 Allowable Stress
========================
"""


def allowable_stress(sig_y):
    """Number [Pa], Number [m], Number [Pa] -> Number [m]
    Allowable Stress - Equation (2)
    """
    return df_h * sig_y

"""
6.4.2.2 Hoop Stress
===================
"""


def hoop_thickness_thin(delta_P, D_o, sig_A):
    """Number [Pa], Number [m], Number [Pa] -> Number [m]
    Thin wall - Equation (3)
    """
    return delta_P*D_o/(2*sig_A)


def req_thickness(t, t_corr, f_tol):
    """Number [m], Number [m], Number [-] -> Number [m]
    Determine required wall thickness based on mechanical allowances.
    Exrapolated from equation (4)"""
    try:
        return (t + t_corr) / (1 - f_tol)
    except ZeroDivisionError:
        print("Divide by zero. Check f_tol is in meters.")
        raise


def hoop_thickness_thick(delta_P, D_o, sig_A):
    """Number [Pa], Number [m], Number [Pa] -> Number [m]
    Thick wall - Equation (5)
    """
    eq = math.sqrt((((sig_A-delta_P))*D_o**2) / (sig_A+delta_P))
    return 0.5 * (D_o - eq)

"""
G.1.2 External Pressure
======================
"""


def collapse_thickness(P_o, sig_y_d, E, v, D_o, f_0):
    """Local Buckling Due to External Over Pressure
    (Clause G.1.2)
    Considers:
    - minimum internal pressure (zero)
    - maximum external pressure (at water depth, d)"""

    def P_e(t):
        """Critical Pressure for an Elastic Critical Tube
        Equation (G.2)"""
        return 2*E/(1-v**2)*(t/D_o)**3

    def P_y(t):
        """Yield Pressure
        Equation (G.3)"""
        return 2*sig_y_d*(t/D_o)

    def char_resist(t):
        """Characteristic resistance for external pressure
        Equation (G.1)"""
        term_1 = ((P_o/P_e(t))-1)
        term_2 = ((P_o/P_y(t))**2-1)
        return term_1 * term_2 - (P_o/P_y(t))*f_0*(D_o/t)

    return scipy.optimize.newton(char_resist, 1e-3)

"""
G.2 Propagation Buckling
========================
"""


def buckle_thickness(D_o, P_p, sig_y):
    """Propagation pressure
    Equation (G.21)"""
    return D_o*(P_p/(10.7*sig_y))**(4/9)

if __name__ == "__main__":  # pragma: no cover
    pass
