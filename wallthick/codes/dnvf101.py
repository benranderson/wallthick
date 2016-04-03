"""
Offshore Standard DNV-OS-F101 Subsea Pipeline Systems August 2012
"""
from scipy.interpolate import interp1d
# import matplotlib.pyplot as plt

title = "DNV-OS-F101"
year = 2012

"""
(Table 2-4)
Determine normal classification (Low, Medium or High) of safety
class based on:
- Fluid Category (A, B, C, D or E)
- Location Class (1 or 2)
- Phase (Temporary or Operational)

use:
safety_class[fluid_cat][loc_class][phase]
"""
safety_class = {'A': {1: {'Temporary': 'Low', 'Operational': 'Low'},
                      2: {'Temporary': 'Low', 'Operational': 'Medium'}},
                'C': {1: {'Temporary': 'Low', 'Operational': 'Low'},
                      2: {'Temporary': 'Low', 'Operational': 'Medium'}},
                'B': {1: {'Temporary': 'Low', 'Operational': 'Medium'},
                      2: {'Temporary': 'Low', 'Operational': 'High'}},
                'D': {1: {'Temporary': 'Low', 'Operational': 'Medium'},
                      2: {'Temporary': 'Low', 'Operational': 'High'}},
                'E': {1: {'Temporary': 'Low', 'Operational': 'Medium'},
                      2: {'Temporary': 'Low', 'Operational': 'High'}}}

"""Table 5-3
use:
safety_class_rf[usage][safety_class]"""
safety_class_rf = {'Pressure containment': {'Low': 1.046,
                                            'Medium': 1.138,
                                            'High': 1.308},
                   'Other': {'Low': 1.04,
                             'Medium': 1.14,
                             'High': 1.26}}


def derate_material(grade, sig_y, temp):
    """ String, Number [Pa], Number [degC] -> Number [Pa]
    Function to return derated yield stress based on temperature """

    # To Do...
    # - Move plot to separate function

    # x-axis:
    tempeartures = [0, 25, 50, 100, 150, 200]

    # y-axis:
    deratings = {"steel": [0, 0, 0, 30e6, 50e6, 70e6],
                 "duplex": [0, 0, 40e6, 90e6, 120e6, 140e6]}

    steel_grades = ["CS X52", "CS X60", "CS X65", "CS X70"]
    duplex_grades = ["22Cr", "25Cr", "13Cr"]

    try:
        if grade in steel_grades:
            derating = deratings["steel"]
        elif grade in duplex_grades:
            derating = deratings["duplex"]
    except:
        print("Select suitable material grade option")

    f = interp1d(tempeartures, derating, bounds_error=False,
                 fill_value=max(derating))

    # # Plot Stress Derating Curve
    # x = []
    # y = []

    # for point in stress_derate:
    #     x.append(point[0])
    #     y.append(point[1])

    # plt.plot(x, y, label=grade + ' Strength Derating')
    # plt.plot(temp, derating, 'ro', label='Design Value')
    # plt.xlabel('Temperature [degC]')
    # plt.ylabel('Strength Derating [Pa]')
    # plt.legend(loc=0)
    # plt.savefig('Material Strength Derating.png')

    return sig_y - f(temp)


def t_1(t_nom, fab_tol, t_cor):
    """ Characteristic wall thicknesses (Table 5-6)
    t_1 used where failure is likely to occur in connection with a low
    capacity:
    - Burst
    - Collapse """
    return t_nom - fab_tol - t_cor


def t_2(t_nom, t_cor):
    """ Characteristic wall thicknesses (Table 5-6)
    t_2 used where failure is likely to occur in connection with an
    extreme load effect at a location with average thickness:
    - Buckle """
    return t_nom - t_cor


def ovality(fab_ov, od, t_nom, t_cor):
    """ Determine ovality tolerance (Table 7-17) """

    if fab_ov == "dnv":
        if od < 60.3e-3:
            ovality = 0
        if od >= 60.3e-3 and od <= 610e-3:
            ovality = 0.015
        if od > 610e-3 and od <= 1422e-3:
            if od / (t_nom-t_cor) <= 75:
                ovality = min(0.01, 10e-3/od)
            else:
                ovality = 0
    else:
        ovality = fab_ov

    return ovality


def effective_axial_force(H, delta_P, A_i, v, A_s, E, alpha, delta_T):
    """ -> Number [N]
    Paragraph 411, Equation (4.12)
    Determine the effective axial force of a totally restrained pipe in
    the linear elastic stress range """

    pressure_term = delta_P*A_i*(1-2*v)
    temperature_term = A_s*E*alpha*delta_T

    return H - pressure_term - temperature_term


if __name__ == "__main__":  # pragma: no cover
    pass
