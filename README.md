# Wallthick

![Pipeline](https://s3-eu-west-1.amazonaws.com/openreply-enidays/wp-content/uploads/2017/03/ss-pipeline-pipe.jpg)

[![Build Status][travis-image]][travis-url]
[![Coverage Status][coveralls-image]][coveralls-url]

This library calculates the required wall thickness and recommended test pressures for a single walled subsea flowline in accordance with allowable stress design code [PD 8010-2](https://shop.bsigroup.com/ProductDetail?pid=000000000030344663).


The calculations consider the following criterion:
* Internal pressure (hoop stress)
* Hydrostatic collapse
* Local buckle propagation

Along with pressures for the following hydrostatic tests:
* Strength test
* Leak test

## Tutorial and Usage

Input file in json, e.g.:

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
$ wallthick [input-file-path]
```

For example:

```sh
$ wallthick inputs/inputs.json
```

## Installation

Clone repository:

```sh
$ git clone https://github.com/benranderson/wallthick.git
```

Navigate in to package directory:

```sh
$ cd wallthick
```

Install dependencies (using [pipenv](https://github.com/pypa/pipenv)):

```sh
$ pipenv install
```

Activiate virtualenv:

```sh
$ pipenv shell
```

Install wallthick package in environment (macOS):

```sh
$ make install
```

Install wallthick package in environment (Windows):

```sh
$ python setup.py install
```

## Development Setup

Install dev dependencies:

```sh
$ pipenv install --dev
```

Run tests (macOS):

```sh
$ make test
```

Run tests (Windows):

```sh
$ py.test tests/
```

<!-- Markdown link & img dfn's -->
[travis-image]: https://travis-ci.org/benranderson/wallthick.svg?branch=master
[travis-url]: https://travis-ci.org/benranderson/wallthick
[coveralls-image]:
https://coveralls.io/repos/github/benranderson/wallthick/badge.svg?branch=master
[coveralls-url]:
https://coveralls.io/github/benranderson/wallthick?branch=master