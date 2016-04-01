"""
Wall Thickness Analysis Module Header
"""


class WallThick:
    """ Represents wall thickness analysis """

    def __init__(self, data):
        # Initialise design codes
        self.init_codes()

        # Determine derated yield strength
        self.sig_y_d = self.dnvf101.derate_material(data.pipe.material.name,
                                                    data.pipe.material.sig_y,
                                                    data.process.T_d)

        # Calculate the maximum external hydrostatic pressure
        P_e_max = data.environment.hydro_pressure()

        
        # Calculate the minimum WT for internal pressure containment
        # Calculate the minimum WT for local buckling due to external pressure
        # Calculate the minimum WT for propagation buckling due to external pressure
        # Display Recommended Minimum Standard API 5L Pipe Size
        # Test Pressure Based on Selected Wall Thickness
            # Calculate test pressures
                # Strength test
                # Leak test
            # Check UR for strength test

        pass

    def init_codes(self):
        """ Initialise design codes """
        # PD8010
        # DNV F101
        pass
        