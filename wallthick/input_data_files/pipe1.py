"""
INPUT DATA FILE
===============
"""

name = "pipe1"

# Pipe
t_sel = 0.0111  # Selected wall thickness [m]
D_o = 60.3e-3  # Outside diameter [m]
t_corr = 0  # Corrosion thickness [m]
f_tol = 0.125  # Fabrication tolerance [-]
f_0 = 0.0025  # Initial ovalisation [-]
mat_p = "CS X65"  # Pipe material

# Process
T_d = 0  # Design temperature [degC]
P_d = 861.8e5  # Design pressure [Pa]
P_h = 0  # Pressure head [Pa]
T_t = 4  # Test temperature [degC]

# Environment
T_a = 4  # Ambient temperature [degC]
g = 9.81  # Gravitational acceleration [m/s/s]
rho_w = 1027  # Seawater density [kg/m^3]
d_max = 114.5  # Maximum water depth [m]
d_min = 87.5  # Minimum water depth [m]

if __name__ == "__main__":  # pragma: no cover
    pass
