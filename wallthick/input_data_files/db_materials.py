"""
Material Database
=================
Name, Density, Young's Modulus, Poisson's Ratio, SMYS, Thermal Expansion Coef
"""

from collections import namedtuple

Material = namedtuple("Material", "name rho E, v, sig_y, alpha")

materials = {
    "CS X52": Material("CS X52", 7850, 2.07e11, 0.3, 360e6, 1.17e-5),
    "CS X60": Material("CS X60", 7850, 2.07e11, 0.3, 415e6, 1.17e-5),
    "CS X65": Material("CS X65", 7850, 2.07e11, 0.3, 450e6, 1.17e-5),
    "CS X70": Material("CS X70", 7850, 2.07e11, 0.3, 485e6, 1.17e-5),
    "22Cr": Material("22Cr", 7800, 2.00e11, 0.3, 360e6, 1.30e-5),
    "25Cr": Material("22Cr", 7800, 2.00e11, 0.3, 360e6, 1.35e-5),
    "13Cr": Material("13Cr", 7690, 2.01e11, 0.27, 360e6, 1.07e-5),
    "Coat1": Material("Coat1", 1000, None, None, None, None),
    "Coat2": Material("Coat1", 652, None, None, None, None)
}

if __name__ == "__main__":  #pragma: no cover
    for mat in materials:
        print(mat)
