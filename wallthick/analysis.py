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

        t_h_req = pd8010.req_thickness(t_h_nom, data.pipe.t_corr,
                                       data.pipe.f_tol)

        print(t_h_req)

        # # Calculate the minimum WT for local buckling due to external pressure
        # t_c_nom = self.calculate_collapse_thickness(P_i, P_o, D_o)
        # self.t_c_req = self.pd8010.req_thickness(t_c_nom, t_corr, f_tol)

        # # Calculate the minimum WT for propagation buckling due to external
        # # pressure
        # t_b_nom = self.calculate_buckle_thickness(P_i, P_o, D_o)
        # self.t_b_req = self.pd8010.req_thickness(t_b_nom, t_corr, f_tol)

        # # Determine Recommended Minimum Standard API 5L Pipe Size
        # t_rec = self.determine_recommended_thickness(self.t_h_req,
        #                                              self.t_c_req,
        #                                              self.t_b_req)

        # Test Pressure Based on Selected Wall Thickness
            # Calculate test pressures
                # Strength test
                # Leak test
            # Check UR for strength test

    # def calculate_hoop_thickness(self, P_i, P_o, D_o)):

    #     # Allowabe hoop stress
    #     sig_h_a = pd8010.allowable_stress(self.sig_y_d)

    #     return P_i + 1

    # def calculate_collapse_thickness(self):
    #     pass

    # def calculate_buckle_thickness(self):
    #     pass

    # def determine_recommended_thickness(self, *thicknesses):
    #     pass

    # def calculate_test_pressures(self):
    #     pass

    # def calculate_test_presure_ur(self):
    #     pass

if __name__ == "__main__":  # pragma: no cover
    pass
