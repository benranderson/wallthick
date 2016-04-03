"""
Wall Thickness Analysis Module Header
"""
import wallthick.codes.pd8010 as pd8010
import wallthick.codes.dnvf101 as dnvf101
# from wallthick.codes.dnvf101 import Dnvf101


class WallThick:
    """ Represents wall thickness analysis """

    def __init__(self, data):

        # Initialise design codes
        self.pd8010 = Pd8010()
        self.dnvf101 = Dnvf101()

        # Determine derated yield strength
        # self.sig_y_d = self.dnvf101.derate_material(data.pipe.material.name,
        #                                             data.pipe.material.sig_y,
        #                                             data.process.T_d)

        # Calculate the maximum external hydrostatic pressure
        # P_e_max = data.environment.hydro_pressure()

        # Calculate the minimum WT for internal pressure containment
        # t_h_nom = self.calculate_hoop_thickness(P_i, P_o, D_o)
        # self.t_h_req = self.pd8010.req_thickness(t_h_nom, t_corr, f_tol)

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

        pass

    def calculate_hoop_thickness(self, P_i):
        return P_i + 1

    def calculate_collapse_thickness(self):
        pass

    def calculate_buckle_thickness(self):
        pass

    def determine_recommended_thickness(self, *thicknesses):
        pass

    def calculate_test_pressures(self):
        pass

    def calculate_test_presure_ur(self):
        pass

if __name__ == "__main__":  # pragma: no cover
    pass
