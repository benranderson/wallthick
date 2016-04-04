import pytest
# from tests.unit.test_headers import *
import wallthick.codes.pd8010 as pd8010


def test_allowable_stress():
    assert pd8010.allowable_stress(100) == 72

"""
-------------------------
"""


@pytest.fixture(params=[
    # tuple with (delta_P, D_o, sig_h_a, expected)
    (852.984e5, 60.3e-3, 324e6, 7.937e-3)
    ])
def test_hoop_thickness_thin_data(request):
    return request.param


def test_hoop_thickness_thin(test_hoop_thickness_thin_data):
    (delta_P, D_o, sig_h_a, expected) = test_hoop_thickness_thin_data
    assert abs(pd8010.hoop_thickness_thin(delta_P, D_o, sig_h_a) - expected) < 1e-6


@pytest.fixture(params=[
    # tuple with (t, t_corr, f_tol, expected)
    (2, 2, 0.5, 8),
    (1, 1, 1, "Divide by zero")
    ])
def test_data(request):
    return request.param


def test_req_thickness(test_data):
    (t, t_corr, f_tol, expected) = test_data

    if expected == "Divide by zero":
        with pytest.raises(ZeroDivisionError):
            pd8010.req_thickness(t, t_corr, f_tol)
    else:
        assert pd8010.req_thickness(t, t_corr, f_tol) == expected


@pytest.fixture(params=[
    # tuple with (delta_P, D_o, sig_h_a, expected)
    (852.984e5, 60.3e-3, 324e6, 7.125e-3)
    ])
def test_hoop_thickness_thick_data(request):
    return request.param


def test_hoop_thickness_thick(test_hoop_thickness_thick_data):
    (delta_P, D_o, sig_h_a, expected) = test_hoop_thickness_thick_data
    assert abs(pd8010.hoop_thickness_thick(delta_P, D_o,
                                           sig_h_a) - expected) < 1e-6


"""
-------------------------
"""


@pytest.fixture(params=[
    # tuple with (P_o, sig_y, E, v, D_o, f_0, expected)
    (23.071e5, 450e6, 207e9, 0.3, 60.3e-3, 2.5e-2, 1.112316e-3),
    ])
def test_collapse_thickness_data(request):
    return request.param


def test_collapse_thickness(test_collapse_thickness_data):
    (P_o, sig_y, E, v, D_o, f_0, expected) = test_collapse_thickness_data
    assert abs(pd8010.collapse_thickness(P_o, sig_y, E, v, D_o,
                                         f_0) - expected) < 1e-6

"""
-------------------------
"""


@pytest.fixture(params=[
    # tuple with (D_o, P_p, sig_y, expected)
    (60.3e-3, 11.536e5, 450e6, 1.483e-3),
    ])
def test_buckle_thickness_data(request):
    return request.param


def test_buckle_thickness(test_buckle_thickness_data):
    (D_o, P_p, sig_y, expected) = test_buckle_thickness_data
    assert abs(pd8010.buckle_thickness(D_o, P_p, sig_y) - expected) < 1e-6
