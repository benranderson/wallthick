"""
PD 8010-2:2015

Pipeline Systems - Part 2: Subsea pipelines – Code of practice - 2015
"""
import math
import scipy.optimize
import wallthick.codes.dnvf101 as dnvf101
import wallthick.codes.api5l as api5l


# General Code Information
# ========================

title = "PD 8010-2"
year = 2015


# General Calcuations
# ===================


def internal_pressure(P_d, rho_c, g, d, h_ref):
    """
    Number [Pa], Number [kg/m^3], Number [m/s/s], Number [m], Number [m] ->
    Number [Pa]

    Return the pipe internal pressure at seabed. Considers pressure head.
    """
    return P_d + rho_c*g*(d + h_ref)


# 6.4.1 Design Factors (Table 2)
# ==============================

# Hoop Stress
df_h = 0.72

# Equivalent stress
df_e = {'Temporary': 1.0,
        'Operational': 0.96}

# Strain factor for reeling (based on previous project experience)
df_s = 0.67


# 6.4.2.1 Allowable Stress
# ========================


def allowable_stress(sig_y):
    """
    Number [Pa], Number [m], Number [Pa] -> Number [m]

    Allowable Stress - Equation (2)
    """
    return df_h * sig_y


# 6.4.2.2 Hoop Stress
# ===================


def hoop_thickness_thin(delta_P, D_o, sig_A):
    """
    Number [Pa], Number [m], Number [Pa] -> Number [m]

    Thin wall - Equation (3)
    """
    return delta_P*D_o/(2*sig_A)


def hoop_thickness_thick(delta_P, D_o, sig_A):
    """
    Number [Pa], Number [m], Number [Pa] -> Number [m]

    Thick wall - Equation (5)
    """
    eq = math.sqrt((((sig_A-delta_P))*D_o**2) / (sig_A+delta_P))
    return 0.5 * (D_o - eq)


def req_thickness(t_min, t_corr, f_tol):
    """
    Number [m], Number [m], Number [-] -> Number [m]

    Determine required wall thickness based on mechanical allowances:
    - corrosion allowance
    - fabrication tolerance

    Exrapolated from equation (4)
    """
    try:
        return (t_min + t_corr) / (1 - f_tol)
    except ZeroDivisionError:
        print("Divide by zero. Check fabrication tolerance.")
        raise


# G.1.2 External Pressure - Hydrostatic Collapse
# ==============================================


def collapse_thickness(P_o, sig_y_d, E, v, D_o, f_0):
    """
    Number [Pa], Number [Pa], Number [Pa], Number [-], Number [m], Number [-]
    -> Number [m]

    Local Buckling Due to External Over Pressure
    (Clause G.1.2)
    Considers:
    - minimum internal pressure (zero)
    - maximum external pressure (at water depth, d)
    """

    def P_e(t):
        """
        Critical Pressure for an Elastic Critical Tube

        Equation (G.2)
        """
        return 2*E/(1-v**2)*(t/D_o)**3

    def P_y(t):
        """
        Yield Pressure

        Equation (G.3)
        """
        return 2*sig_y_d*(t/D_o)

    def char_resist(t):
        """
        Characteristic resistance for external pressure

        Equation (G.1)
        """
        term_1 = ((P_o/P_e(t))-1)
        term_2 = ((P_o/P_y(t))**2-1)
        return term_1 * term_2 - (P_o/P_y(t))*f_0*(D_o/t)

    return scipy.optimize.newton(char_resist, 1e-3)


# G.2 Propagation Buckling
# ========================


def buckle_thickness(D_o, P_p, sig_y):
    """
    Number [m], Number [Pa], Number [Pa] -> Number [m]

    Return the nominal buckle thickness based on the propagation pressure

    Equation (G.21)
    """
    return D_o*(P_p/(10.7*sig_y))**(4/9)


# G.1.4 Bending
# =============


def reeling_thickness(D_o, R_reel, t_coat):
    """
    Number [m], Number [m], Number [m] -> Number [m]

    Return the minimum reelable wall thickness
    """
    if R_reel > 0:
        # Functional strain from bending around vessel reel radius
        epsilon_b = D_o / (2*(R_reel + 0.5*D_o + t_coat))

        # Characteristic bending strain for buckling due to bending moments
        # acting alone Equation (G.8)
        return D_o * math.sqrt(epsilon_b/(15*df_s))
    else:
        return 0


# 11 Construction - Testing
# =========================


def calculate_strength_test_pressure(data):
    """
    InputData -> Number [Pa]

    Return the strength test pressure, the minimum of:
    - 1.5 * design pressure
        Note that hydrostatic head is not multiplied by 1.5 (interpreted by
        last paragraph of Section 11.5.2)
    - the pressure that induces a hoop stress of 90 percent SMYS at nominal
        wall thickness.

    (Section 11.5.1, Ref.1)
    """

    # Determine nominal wall thickness (no corrosion)
    t_min = data.pipe.t_sel * (1 - data.pipe.f_tol)

    # Determine pressure that induces 90 percent SMYS using correct wall
    # theory (i.e. thick or thin)
    if data.pipe.thin_wall_check(t_min):
        # Thin wall equation
        P_hoop = 0.9*data.pipe.material.sig_y*2*t_min/data.pipe.D_o + \
            data.environment.hydro_pressure(data.environment.d_min)
    else:
        # Thick wall equation
        num = 0.9*data.pipe.material.sig_y*(data.pipe.D_o**2 - (data.pipe.D_o - 2*t_min)**2)
        den = data.pipe.D_o**2 + (data.pipe.D_o - 2*t_min)**2
        P_hoop = num / den

    # Determine 1.5 * Design Pressure
    P_h = data.environment.rho_w*data.environment.g*data.process.h_ref
    P_test = 1.5*data.process.P_d + P_h

    # Return strength test pressure
    return min(P_hoop, P_test)


def calculate_leak_test_pressure(P_d):
    """
    Number [Pa] -> Number [Pa]

    Return leak test pressure: 1.1 * MAOP (design pressure) at LAT

    Section 11.5.3
    """

    return 1.1*P_d


class WallThick:
    """
    Calculate the required wall thickness of a single walled flowline
    installed on the seabed in accordance with allowable stress design code
    PD 8010.

    Considers the following load scenarios:
    1. Reeling (if applicable)
    2. Pressure containment (bursting)
    3. Local buckling (collapse)
    4. Propagation buckling

    Also determines the hydrostatic strength and leak test pressures.
    """

    def __init__(self, data):

        # Associate input data with design calculation object
        self.data = data
        self.results = self.run_analysis(data)

    def run_analysis(self, data):
        """
        InputData -> dict

        Manager method to carry out analysis
        """

        initial_results = self.initial_calcs(data)
        thicknesses = self.calculate_thicknesses(data, initial_results)
        test_pressures = self.calculate_test_pressures(data)

        return {"thicknesses": thicknesses,
                "test_pressures": test_pressures}

    def initial_calcs(self, data):
        """
        InputData -> tuple

        Initial calculations
        """

        # Determine derated yield strength
        sig_y_d = dnvf101.derate_material(data.pipe.material.name,
                                          data.pipe.material.sig_y,
                                          data.process.T_d)

        # Calculate internal pressure at seabed
        P_i = internal_pressure(data.process.P_d, data.process.rho_d,
                                data.environment.g,
                                data.environment.d_min,
                                data.process.h_ref)

        # Calculate characteristic external pressures
        P_o_min = data.environment.hydro_pressure(data.environment.d_min)
        P_o_max = data.environment.hydro_pressure(data.environment.d_max)

        # Calculate the pressure difference
        delta_P_max = P_i - P_o_min
        delta_P_min = P_i - P_o_max

        return (sig_y_d, P_i, P_o_min, P_o_max, delta_P_max, delta_P_min)

    def calculate_thicknesses(self, data, initial_results):
        """
        InputData, tuple -> dict

        Return dictionary of nominal wall thickness.

        Reeling Criteria - Local Buckling - Bending During Reeling
        ----------------------------------------------------------
        Note calculation applicable for a pipe bent around a curvature on a
        vessel during installation.

        Internal pressure containment (Hoop)
        ------------------------------------
        Calculate the allowable hoop stress
        Note the maximum pressure difference is used
        Consider correct wall theory, i.e. thick or thin
        Consider bend thinning

        Hydrostatic Collapse
        --------------------
        Calculate the minimum WT for local buckling due to external pressure
        Note characteristic external pressure equal to max external pressure

        Local Buckle Propagation
        ------------------------
        Calculate the minimum WT for propagation buckling due to external
        pressure.
        Note use maximum external pressure and ignore internal pressure.

        Recommended Standard API 5L Pipe Size
        -------------------------------------
        Advise recommended size

        """

        (sig_y_d, P_i, P_o_min, P_o_max, delta_P_max,
         delta_P_min) = initial_results

        # Reeling Criteria
        t_r_nom = reeling_thickness(data.pipe.D_o, data.process.R_reel,
                                    data.pipe.t_coat)

        # Hoop
        sig_A = allowable_stress(sig_y_d)
        t_h_min_thin = hoop_thickness_thin(delta_P_max, data.pipe.D_o, sig_A)

        # Wall theory check
        if data.pipe.thin_wall_check(t_h_min_thin):
            t_h_min = t_h_min_thin
        else:
            t_h_min = hoop_thickness_thick(delta_P_max, data.pipe.D_o, sig_A)

        t_h_nom = req_thickness(t_h_min, data.pipe.t_corr, data.pipe.f_tol)

        # Bend thinning
        t_h_nom_bt = t_h_nom / (1 - data.pipe.B)

        # Hydrostatic Collapse
        t_c_nom = collapse_thickness(P_o_max, sig_y_d, data.pipe.material.E,
                                     data.pipe.material.v,
                                     data.pipe.D_o,
                                     data.pipe.f_0)

        # Local Buckle Propagation
        t_b_nom = buckle_thickness(data.pipe.D_o, P_o_max, sig_y_d)

        # Recommended size
        t_rec = api5l.recommended_wall_thickness(data.pipe.D_o, max(t_r_nom,
                                                                    t_h_nom,
                                                                    t_h_nom_bt,
                                                                    t_c_nom,
                                                                    t_b_nom))

        return {"t_r_nom": t_r_nom,
                "t_h_nom": t_h_nom,
                "t_h_nom_bt": t_h_nom_bt,
                "t_c_nom": t_c_nom,
                "t_b_nom": t_b_nom,
                "t_rec": t_rec}

    def calculate_test_pressures(self, data):
        """
        InputData -> dict
        """

        P_st = calculate_strength_test_pressure(data)
        P_lt = calculate_leak_test_pressure(data.process.P_d)

        return {"P_st": P_st,
                "P_lt": P_lt}

    def write_results(self):
        """
        Print results to text file
        """

        results = """Wall Thickness Design
=====================

Pipeline: {0}

Reeling Criterion:                               {1:0.2f} mm
Pressure Containment:                            {2:0.2f} mm
Pressure Containment (incl. bend thinning):      {3:0.2f} mm
Hydrostatic Collapse:                            {4:0.2f} mm
Propagation buckling:                            {5:0.2f} mm

Minimum Recommended API Wall Thickness:          {6:0.2f} mm
Selected Wall Thickness:                         {7:0.2f} mm

Strength Test Pressure:                          {8:0.2f} bar
Leak Test Pressure:                              {9:0.2f} bar
""".format(self.data.name,
           1000*self.results["thicknesses"]["t_r_nom"],
           1000*self.results["thicknesses"]["t_h_nom"],
           1000*self.results["thicknesses"]["t_h_nom_bt"],
           1000*self.results["thicknesses"]["t_c_nom"],
           1000*self.results["thicknesses"]["t_b_nom"],
           1000*self.results["thicknesses"]["t_rec"],
           1000*self.data.pipe.t_sel,
           1e-5*self.results["test_pressures"]["P_st"],
           1e-5*self.results["test_pressures"]["P_lt"])

        with open("results/{} Results.txt".format(self.data.name), "w") as out:
            out.write(results)

    def plot_results(self):
        """
        Visually display analysis results.
        """
        pass

if __name__ == "__main__":  # pragma: no cover
    pass
