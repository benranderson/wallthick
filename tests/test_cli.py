#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for cli module."""

import pytest
import json

import click

from click.testing import CliRunner

from wallthick import cli

test_inputs = {
    "name": "Test Pipe",
    "t_sel": 0.01097,
    "f_tol": 0.0125,
    "B": 0,
    "t_corr": 0,
    "D_o": 0.1683,
    "sig_y": 450000000,
    "sig_y_d": 370000000,
    "v": 0.3,
    "E": 207000000000,
    "f_0": 0.0025,
    "rho_w": 1027,
    "h": 111,
    "H_t": 1.47,
    "H": 26.1,
    "P_d": 13000000,
    "P_h": 0,
    "g": 9.81,
    "f_s": 2
}


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('inputs.json', 'w') as f:
            json.dump(test_inputs, f)

        result = runner.invoke(cli.main, ['inputs.json'])
        assert result.exit_code == 0
        assert 'Running PD 8010-2 wall thickness calculation...' in result.output

        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


def test_command_line_interface_missing_params():
    """Test the CLI."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_inputs_missing = {
            "D_o": 50
        }
        with open('inputs.json', 'w') as f:
            json.dump(test_inputs_missing, f)

        result = runner.invoke(cli.main, ['inputs.json'])
        assert result.exit_code == 0
        assert 'Check input data file includes all of the following:' in result.output
