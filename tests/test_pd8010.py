from wallthick import pd8010 as pd
import pytest

tol_pc = 0.001

test_data = [
    {
        "name": "Test Pipe",
        "t_sel": 0.01097,
        "f_tol": 0.125,
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
        "f_s": 2,
        "h_min": 97.95,
        "h_max": 125.52,
        "P_i": 130,
        "P_o_max": 1264600,
        "P_o_min": 986800,
        "delta_P_max": 12013200,
        "delta_P_min": 11735400,
        "t_h_thin": 0.003795,
        "t_h_thick": 0.003713,
        "t_h_n": 0.003795,
        "t_h": 0.004337,
        "P_o_c": 2529200,
        "t_c_n": 0.003259979,
        "t_c": 0.003726,
        "P_o_b": 1264666,
        "t_b_n": 0.004704,
        "t_b": 0.005376
    }
]


@pytest.mark.parametrize("P_d, P_h, expected", [
    (13000000, 0, 13000000)
])
def test_internal_pressure(P_d, P_h, expected):
    assert abs(pd.internal_pressure(P_d, P_h) -
               expected) <= tol_pc * expected


@pytest.mark.parametrize("h, H_t, H, expected", [
    (111, 1.47, 26.1, (97.95, 125.52))
])
def test_water_depths(h, H_t, H, expected):
    d_min, d_max = pd.water_depths(h, H_t, H)
    assert abs(d_min - expected[0]) <= tol_pc * expected[0]
    assert abs(d_max - expected[1]) <= tol_pc * expected[1]


@pytest.mark.parametrize("rho_w, g, d, expected", [
    (1027, 9.81, 97.95, 986800),
    (1027, 9.81, 125.52, 1264600)
])
def test_external_pressure(rho_w, g, d, expected):
    assert abs(pd.external_pressure(rho_w, g, d) -
               expected) <= tol_pc * expected


@pytest.mark.parametrize("P_i, P_o, D_o, sig_y_d, expected", [
    (130e5, 986800, 0.1683, 370e6, 3.795e-3),
])
def test_hoop_thickness_thin(P_i, P_o, D_o, sig_y_d, expected):
    assert abs(pd.hoop_thickness_thin(
        P_i, P_o, D_o, sig_y_d) - expected) <= tol_pc * expected


@pytest.mark.parametrize("P_i, P_o, D_o, sig_y_d, expected", [
    (130e5, 986800, 0.1683, 370e6, 3.713e-3),
])
def test_hoop_thickness_thick(P_i, P_o, D_o, sig_y_d, expected):
    assert abs(pd.hoop_thickness_thick(
        P_i, P_o, D_o, sig_y_d) - expected) <= tol_pc * expected


@pytest.mark.parametrize("P_i, P_o, D_o, sig_y_d, expected", [
    (130e5, 986800, 0.1683, 370e6, 3.795e-3),
])
def test_hoop_thickness(P_i, P_o, D_o, sig_y_d, expected):
    assert abs(pd.hoop_thickness(
        P_i, P_o, D_o, sig_y_d) - expected) <= tol_pc * expected


@pytest.mark.parametrize("t_min, t_corr, f_tol, expected", [
    (3.795e-3, 0, 0.125, 4.337e-3),
    (3.260e-3, 0, 0.125, 3.726e-3),
    (4.704e-3, 0, 0.125, 5.376e-3)
])
def test_req_thickness(t_min, t_corr, f_tol, expected):
    assert abs(pd.req_thickness(
        t_min, t_corr, f_tol) - expected) <= tol_pc * expected


def test_req_thickness_zerodiv():
    with pytest.raises(ZeroDivisionError):
        pd.req_thickness(1, 1, 1)


@pytest.mark.parametrize("P_o, sig_y, E, v, D_o, f_0, expected", [
    (25.292e5, 370e6, 207e9, 0.3, 0.1683, 2.5e-2, 3.260e-3),
    (23.071e5, 450e6, 207e9, 0.3, 60.3e-3, 2.5e-2, 1.112316e-3)
])
def test_collapse_thickness(P_o, sig_y, E, v, D_o, f_0, expected):
    assert abs(pd.collapse_thickness(
        P_o, sig_y, E, v, D_o, f_0) - expected) <= tol_pc * expected


@pytest.mark.parametrize("D_o, P_p, sig_y, expected", [
    (0.1683, 12.646e5, 370e6, 4.704e-3)
])
def test_buckle_thickness(D_o, P_p, sig_y, expected):
    assert abs(pd.buckle_thickness(
        D_o, P_p, sig_y) - expected) <= tol_pc * expected
