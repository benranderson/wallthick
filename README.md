# Wallthick

Calculate the required wall thickness of a single walled subsea flowline in accordance with allowable stress design code [PD 8010-2](https://shop.bsigroup.com/ProductDetail?pid=000000000030344663).

## Installation

```sh
$ git clone https://github.com/benranderson/wallthick.git
```

Install dependencies:

```sh
$ make Makefile
```

## Usage Example

Import module:

```python
>>> import wallthick as wt
```

Set pipe parameters:

```python
>>> pipe = wt.Pipe(t_sel=0.0143, D_o=508e-3, t_corr=1.5e-3, f_tol=0.125, f_0=0.025,
                   B=0, mat_p="CS X65", t_coat=0)
```
Where:
* t_sel = Selected wall thickness [m]
* D_o = Outside diameter [m]
* t_corr = Corrosion thickness [m]
* f_tol = Fabrication tolerance [-]
* f_0 = Initial ovalisation [-]
* B = Bend thinning [-]
* mat_p = Pipe material
* t_coat = Overall coating thickness [m]

Set process conditions:

```python
>>> process = wt.Process(T_d=50, P_d=132e5, h_ref=16, rho_d=1025, R_reel=0,
                         T_lay=0)
```

Where:
* T_d = Design temperature [degC]
* P_d = Design pressure [Pa]
* h_ref = Reference height above water level [m]
* rho_d = Density of operational contents [kgm^3]
* R_reel = Vessel reel radius [m]
* T_lay = Residual lay tension after pipeline installation [m]

Set environmental conditions:

```python
>>> env = wt.Environment(d_max=15.48, d_min=11, T_a=3.6)
```

Where:
* d_max = Maximum water depth [m]
* d_min = Minimum water depth [m]
* T_a = Ambient temperature [degC]

Create and run wall thickness analysis for selected input parameters:

```python
>>> pd8010 = wt.Pd8010(pipe, process, env)
```

Results:

```sh
>>> pd8010
2017-01-27

Wall Thickness Design
=====================

Pipeline: 20in X65

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

Where:

* Minimum wall thicknesses [m]: 
    * t_r_nom = Reeling Criterion
    * t_h_nom = Pressure Containment
    * t_h_nom_bt = Pressure Containment (incl. bend thinning)
    * t_c_nom = Hydrostatic Collapse
    * t_b_nom = Propagation buckling
    * t_rec = Minimum Recommended API Wall Thickness
* Test Pressures [barg]:
    * P_st = Strength Test Pressure:
    * P_lt = Leak Test Pressure

## Development Setup

Install dependencies:

```sh
$ make Makefile setup-dev
```

Run tests:

```sh
$ make Makefile test
```
