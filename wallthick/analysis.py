"""
Wall Thickness Analysis Module Header
"""
import wallthick.codes.pd8010 as pd8010
import wallthick.codes.dnvf101 as dnvf101
# from wallthick.codes.dnvf101 import Dnvf101


class WallThick:
    """ Represents wall thickness analysis """

    def __init__(self, data):

        # Determine derated yield strength
        sig_y_d = dnvf101.derate_material(data.pipe.material.name,
                                          data.pipe.material.sig_y,
                                          data.process.T_d)

        # Calculate internal pressure at seabed
        P_i = data.process.P_d + data.process.P_h

        # Calculate characteristic external pressures
        P_o_min = data.environment.hydro_pressure(data.environment.d_min)
        P_o_max = data.environment.hydro_pressure(data.environment.d_max)

        # Calculate the pressure difference
        delta_P_max = P_i - P_o_min
        delta_P_min = P_i - P_o_max

        # Internal pressure containment (Hoop)
        # =====================================================================

        # Calculate the allowable hoop stress
        sig_A = pd8010.allowable_stress(sig_y_d)

        # Calculate the minimum WT for internal pressure containment
        # Note use maximum pressure difference
        t_h_nom_thin = pd8010.hoop_thickness_thin(delta_P_max, data.pipe.D_o,
                                                  sig_A)

        # Determine whether thick wall required
        if data.pipe.thin_wall_check(t_h_nom_thin):
            t_h_nom = t_h_nom_thin
        else:
            t_h_nom = pd8010.hoop_thickness_thick(delta_P_max, data.pipe.D_o,
                                                  sig_A)

        self.t_h_req = pd8010.req_thickness(t_h_nom, data.pipe.t_corr,
                                            data.pipe.f_tol)

        # Hydrostatic Collapse
        # =====================================================================

        # Safety to allow for external bending moment and axial compression
        f_safety = 2

        # Characteristic External Pressure
        P_o_char = P_o_max*f_safety

        # Calculate the minimum WT for local buckling due to external pressure
        t_c_nom = pd8010.collapse_thickness(P_o_char, sig_y_d,
                                            data.pipe.material.E,
                                            data.pipe.material.v,
                                            data.pipe.D_o,
                                            data.pipe.f_0)

        self.t_c_req = pd8010.req_thickness(t_c_nom, data.pipe.t_corr,
                                            data.pipe.f_tol)

        # Local Buckle Propagation
        # =====================================================================

        # Calculate the minimum WT for propagation buckling due to external
        # pressure
        # Note use maximum external pressure and ignore internal pressure
        t_b_nom = pd8010.buckle_thickness(data.pipe.D_o, P_o_max, sig_y_d)
        self.t_b_req = pd8010.req_thickness(t_b_nom, data.pipe.t_corr,
                                            data.pipe.f_tol)

        # # Determine Recommended Minimum Standard API 5L Pipe Size
        # t_rec = self.determine_recommended_thickness(self.t_h_req,
        #                                              self.t_c_req,
        #                                              self.t_b_req)

        # Test Pressure Based on Selected Wall Thickness
            # Calculate test pressures
                # Strength test
                # Leak test
            # Check UR for strength test

if __name__ == "__main__":  # pragma: no cover
    pass
