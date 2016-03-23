"""
INPUT DATA FILE
===============
"""

name = "pipe1"

# Pipe
t_sel = 0.01427  # Selected wall thickness [m]
D_o = 168.3e-3  # Outside diameter [m]
t_corr = 0.002  # Corrosion thickness [m]
f_tol = 0.125  # Fabrication tolerance [-]
f_0 = 0.015  # Initial ovalisation [-]
mat_p = "CS X60"  # Pipe material

# Process
T_d = 85  # Design temperature [degC]
P_d = 345e5  # Design pressure [Pa]
T_t = 4  # Test temperature [degC]

# Environment
T_a = 4  # Ambient temperature [degC]
g = 9.81  # Gravitational acceleration [m/s/s]
rho_w = 1025  # Seawater density [kg/m^3]
d = 110.39009473  # Water depth [m]

if __name__ == "__main__":    #pragma: no cover
    pass
