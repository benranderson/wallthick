# wallthick
Subsea pipeline wall thickness design calculations.

From input data python file, e.g.:

```python
"""
INPUT DATA FILE
===============
"""

name = "Shell 20in"

# Pipe
t_sel = 0.0143  # Selected wall thickness [m]
D_o = 508e-3  # Outside diameter [m]
t_corr = 1.5e-3  # Corrosion thickness [m]
f_tol = 0.125  # Fabrication tolerance [-]
f_0 = 0.025  # Initial ovalisation [-]
B = 0  # Bend thinning [-]
mat_p = "CS X65"  # Pipe material
t_coat = 0  # Overall coating thickness [m]

# Process
T_d = 50  # Design temperature [degC]
P_d = 132e5  # Design pressure [Pa]
h_ref = 16  # Reference height above water level [m]
rho_d = 1025  # Density of operational contents [kgm^3]
R_reel = 0  # Vessel reel radius [m]
T_lay = 0  # Residual lay tension after pipeline installation [m]

# Environment
d_max = 15.48  # Maximum water depth [m]
d_min = 11  # Minimum water depth [m]
T_a = 3.6  # Ambient temperature [degC]
g = 9.80665  # Gravitational acceleration [m/s/s]
rho_w = 1025  # Seawater density [kg/m^3]

if __name__ == "__main__":  # pragma: no cover
    pass
```

Generate output in results text file:

```
2017-01-27

Wall Thickness Design
=====================

Pipeline: Shell 20in

Reeling Criterion:                               0.00 mm
Pressure Containment:                            13.68 mm
Pressure Containment (incl. bend thinning):      13.68 mm
Hydrostatic Collapse:                            3.66 mm
Propagation buckling:                            5.13 mm

Minimum Recommended API Wall Thickness:          14.30 mm
Selected Wall Thickness:                         14.30 mm

Strength Test Pressure:                          200.62 bar
Leak Test Pressure:                              145.20 bar
```