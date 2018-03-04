# -*- coding: utf-8 -*-

'''Console script for wallthick.'''

import click
import json

from wallthick.pd8010 import Pd8010

req_inputs = [
    't_sel',
    'f_tol',
    'B',
    't_corr',
    'D_o',
    'sig_y',
    'sig_y_d',
    'v',
    'E',
    'f_0',
    'rho_w',
    'h',
    'H_t',
    'H',
    'P_d',
    'P_h',
    'g',
    'f_s',
]


@click.command()
@click.argument('inputs', type=click.File('rb'))
def main(inputs):
    """Console script for wallthick."""
    data = json.load(inputs)
    if all(param in data for param in req_inputs):
        click.echo('Running PD 8010-2 wall thickness calculation...')
        pd = Pd8010(data)
        click.echo(f'\nNominal Wall thicknesses')
        click.echo(f'------------------------\n')
        click.echo(f'Pressure Containment: {1000*pd.t_h:.3f} mm')
        click.echo(f'Hydrostatic Collapse: {1000*pd.t_c:.3f} mm')
        click.echo(f'Propagation buckling: {1000*pd.t_b:.3f} mm')
        click.echo(f'\nTest Pressures')
        click.echo(f'--------------\n')
        click.echo(f'Strength Test Pressure: {0.00001*pd.P_st:.1f} bar')
        click.echo(f'Leak Test Pressure: {0.00001*pd.P_lt:.1f} bar')
    else:
        click.echo(
            f'Check input data file includes all of the following: {req_inputs}')
    return 0


if __name__ == '__main__':  # pragma: no cover
    main()
