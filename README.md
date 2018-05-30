# Wallthick

![Pipeline](https://s3-eu-west-1.amazonaws.com/openreply-enidays/wp-content/uploads/2017/03/ss-pipeline-pipe.jpg)

[![PyPI Status][pypi-image]][pypi-url]
[![Build Status][travis-image]][travis-url]
[![Coverage Status][coveralls-image]][coveralls-url]

This library calculates the required wall thickness and recommended test pressures for a single walled subsea flowline in accordance with allowable stress design code [PD 8010-2](https://shop.bsigroup.com/ProductDetail?pid=000000000030344663).

The calculations consider the following criterion:

*   Internal pressure (hoop stress)
*   Hydrostatic collapse
*   Local buckle propagation

Along with pressures for the following hydrostatic tests:

*   Strength test
*   Leak test

## Tutorial and Usage

Input json file:

```json
{
    "name": "Test Pipe",
    "t_sel": 0.01097,
    "f_tol": 0.125,
    "B": 0,
    "t_corr": 0.001,
    "D_o": 0.1683,
    "sig_y": 450000000,
    "sig_y_d": 370000000,
    "v": 0.3,
    "E": 207000000000,
    "f_0": 0.025,
    "rho_w": 1027,
    "h": 111,
    "H_t": 1.47,
    "H": 26.1,
    "P_d": 13000000,
    "P_h": 0,
    "g": 9.81,
    "f_s": 2
}
```

Uses [click](http://click.pocoo.org) cli to run calculations, i.e.:

```sh
$ wallthick path/to/input/file
```

For example:

```sh
$ wallthick inputs/inputs.json
```

Gives the following output in the terminal:

```
Running PD 8010-2 wall thickness calculation...

Nominal Wall Thicknesses
------------------------
Pressure Containment:   5.480 mm
Hydrostatic Collapse:   3.260 mm
Propagation Buckling:   4.704 mm

Test Pressures
--------------
Strength Test Pressure: 195.0 bar
Leak Test Pressure:     143.0 bar
```

## Installation

```sh
$ pip install wallthick
```

<!-- Markdown link & img dfn's -->

[pypi-image]: https://img.shields.io/pypi/v/wallthick.svg
[pypi-url]: https://pypi.python.org/pypi/wallthick
[travis-image]: https://travis-ci.org/benranderson/wallthick.svg?branch=master
[travis-url]: https://travis-ci.org/benranderson/wallthick
[coveralls-image]: https://coveralls.io/repos/github/benranderson/wallthick/badge.svg?branch=master
[coveralls-url]: https://coveralls.io/github/benranderson/wallthick?branch=master
