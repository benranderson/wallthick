"""
INPUT DATA FILE
===============
"""

name = "Aviat 4in X65"

# Pipe
t_sel = 0.0064  # Selected wall thickness [m]
D_o = 114.3e-3  # Outside diameter [m]
t_corr = 1.5e-3  # Corrosion thickness [m]
f_tol = 0.125  # Fabrication tolerance [-]
f_0 = 0.025  # Initial ovalisation [-]
B = 0.1  # Bend thinning [-]
mat_p = "CS X65"  # Pipe material
t_coat = 2.5e-3  # Overall coating thickness [m]

# Process
T_d = 50  # Design temperature [degC]
P_d = 179.3e5  # Design pressure [Pa]
h_ref = 0  # Reference height above water level [m]
rho_d = 1025  # Density of operational contents [kgm^3]
R_reel = 7.5  # Vessel reel radius [m]
T_lay = 0  # Residual lay tension after pipeline installation [m]

# Environment
d_max = 124.247  # Maximum water depth [m]
d_min = 80.5  # Minimum water depth [m]
T_a = 3.6  # Ambient temperature [degC]
g = 9.80665  # Gravitational acceleration [m/s/s]
rho_w = 1025  # Seawater density [kg/m^3]

if __name__ == "__main__":  # pragma: no cover
    pass
