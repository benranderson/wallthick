import pytest
import os
# from tests.unit.test_headers import *
import wallthick.codes.pd8010 as pd8010
from wallthick.input_classes import Pipe
from wallthick.input_classes import Environment
from wallthick.input_classes import Process
from wallthick.input_classes import InputData
from input_data_files.db_materials import materials


@pytest.fixture(params=[
    # tuple with (rho, g, d, h_ref, expected)
    (1025, 9.81, 100, 0, 10.05525e5),
    ])
def test_pressure_head_data(request):
    return request.param
def test_pressure_head(test_pressure_head_data):
    (rho, g, d, h_ref, expected) = test_pressure_head_data
    assert abs(pd8010.pressure_head(rho, g, d, h_ref) - expected) < (expected/10e5)


def test_allowable_stress():
    assert pd8010.allowable_stress(100) == 72


@pytest.fixture(params=[
    # tuple with (t, D_o, P_o, sig, expected)
    (9.713e-3, 219.1e-3, P_o, 405, 187.392e5),
    ])
def test_hoop_pressure_thin_data(request):
    return request.param
def test_hoop_pressure_thin(test_hoop_pressure_thin_data):
    (t, D_o, P_o, sig, expected) = test_hoop_pressure_thin_data
    assert abs(pd8010.hoop_pressure_thin(t, D_o, P_o, sig) - expected) < (expected/10e5)


@pytest.fixture(params=[
    # tuple with (t, D_o, P_o, sig, expected)
    (t, D_o, P_o, sig, 187.392e5),
    ])
def test_hoop_pressure_thick_data(request):
    return request.param
def test_hoop_pressure_thick(test_hoop_pressure_thick_data):
    (t, D_o, P_o, sig, expected) = test_hoop_pressure_thick_data
    assert abs(pd8010.hoop_pressure_thin(t, D_o, P_o, sig) - expected) < (expected/10e5)


@pytest.fixture(params=[
    # tuple with (P_i, P_o, D_o, sig_A, expected)
    (187.392e5, 809171.21, 219.1e-3, 324e6, 6.06e-3)
    ])
def test_hoop_thickness_thin_data(request):
    return request.param
def test_hoop_thickness_thin(test_hoop_thickness_thin_data):
    (P_i, P_o, D_o, sig_A, expected) = test_hoop_thickness_thin_data
    assert abs(pd8010.hoop_thickness_thin(P_i, P_o, D_o,
                                          sig_A) - expected) < 1e-6


@pytest.fixture(params=[
    # tuple with (P_i, P_o, D_o, sig_A, expected)
    (187.392e5, 809171.21, 219.1e-3, 324e6, 5.9e-3)
    ])
def test_hoop_thickness_thick_data(request):
    return request.param
def test_hoop_thickness_thick(test_hoop_thickness_thick_data):
    (P_i, P_o, D_o, sig_A, expected) = test_hoop_thickness_thick_data
    assert abs(pd8010.hoop_thickness_thick(P_i, P_o, D_o,
                                           sig_A) - expected) < 1e-6


@pytest.fixture(params=[
    # tuple with (P_i, P_o_min, D_o, sig_A, expected)
    (187.392e5, 809171.21, 219.1e-3, 324e6, 5.9e-3)
    ])
def test_hoop_thickness_data(request):
    return request.param
def test_hoop_thickness_thick(test_hoop_thickness_data):
    (P_i, P_o_min, D_o, sig_A, expected) = test_hoop_thickness_data
    assert abs(pd8010.hoop_thickness_thick(P_i, P_o_min, D_o,
                                           sig_A) - expected) < 1e-6


@pytest.fixture(params=[
    # tuple with (t, t_corr, f_tol, expected)
    (2, 2, 0, 4),
    ])
def test_data(request):
    return request.param
def test_req_thickness(test_data):
    (t, t_corr, f_tol, expected) = test_data
    assert pd8010.req_thickness(t, t_corr, f_tol) == expected
def test_req_thickness_zerodiv(test_data):
    with pytest.raises(ZeroDivisionError):
            pd8010.req_thickness(1, 1, 1, "Divide by zero. Check fabrication "
                                 "tolerance.")


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


@pytest.fixture(params=[
    # tuple with (D_o, P_p, sig_y, expected)
    (60.3e-3, 11.536e5, 450e6, 1.483e-3),
    ])
def test_buckle_thickness_data(request):
    return request.param
def test_buckle_thickness(test_buckle_thickness_data):
    (D_o, P_p, sig_y, expected) = test_buckle_thickness_data
    assert abs(pd8010.buckle_thickness(D_o, P_p, sig_y) - expected) < 1e-6


@pytest.fixture(params=[
    # tuple with (D_o, R_reel, t_coat, expected)
    (219.1e-3, 7.5, 2.5e-3, 8.29e-3),
    (114.3e-3, 0, 2.5e-3, 0)
    ])
def test_reeling_thickness_data(request):
    return request.param
def test_reeling_thickness(test_reeling_thickness_data):
    (D_o, R_reel, t_coat, expected) = test_reeling_thickness_data
    assert abs(pd8010.reeling_thickness(D_o, R_reel,
                                        t_coat) - expected) < 1e-5


@pytest.fixture(params=[
    # tuple with (t_sel, f_tol, sig_y, D_o, P_d, P_o, P_h, expected)
    (t_sel, f_tol, sig_y, D_o, P_d, P_o, P_h, expected),
    ])
def test_strength_test_pressure_data(request):
    return request.param
def test_strength_test_pressure(test_strength_test_pressure_data):
    (t_sel, f_tol, sig_y, D_o, P_d, P_o, P_h,
     expected) = test_strength_test_pressure_data
    assert abs(pd8010.strength_test_pressure(t_sel, f_tol, sig_y, D_o, P_d,
                                             P_o, P_h) - expected) < (P_d/10e5)


@pytest.fixture(params=[
    # tuple with (P_d, expected)
    (100e5, 110e5),
    (0, 0)
    ])
def test_leak_test_pressure_data(request):
    return request.param
def test_leak_test_pressure(test_leak_test_pressure_data):
    (P_d, expected) = test_leak_test_pressure_data
    assert abs(pd8010.leak_test_pressure(P_d) - expected) < (P_d/10e5)


@pytest.fixture(scope='class', params=[
    # tuple with (WallThick(InputData(name,
    #                                 Pipe(t_sel, D_o, t_corr, f_tol, f_0, B
    #                                      material, t_coat),
    #                                 Process(T_d, P_d, h_ref, rho_d, R_reel,
    #                                         T_lay),
    #                                 Environment(d_max, d_min, T_a, rho_w,
    #                                             g))),
    #             expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
    #             expected_t_b_nom, expected_t_rec, expected_P_st,
    #             expected_P_lt)
    (pd8010.WallThick(InputData("Aviat 8in X65",
                                Pipe(0.0111, 219.1e-3, 1.5e-3, 0.125, 0.025,
                                     0.1, materials["CS X65"], 2.5e-3),
                                Process(50, 179.3e5, 0, 1025, 7.5, 0),
                                Environment(124.247, 80.5, 3.6, 1025,
                                            9.80665))),
     8.29e-3, 8.64e-3, 3.25e-3, 5.58e-3, 11.1e-3, 268.9e5, 197.23e5),
    (pd8010.WallThick(InputData("Aviat 4in X65",
                                Pipe(0.0064, 114.3e-3, 1.5e-3, 0.125, 0.025,
                                     0.1, materials["CS X65"], 2.5e-3),
                                Process(50, 179.3e5, 0, 1025, 0, 0),
                                Environment(124.247, 80.5, 3.6, 1025,
                                            9.80665))),
     0, 5.33e-3, 1.7e-3, 2.91e-3, 14.3e-3, 268.9e5, 197.23e5),
    ])
def wallthick_data(request):
    return request.param


class TestWallThick:

    # def test_initial_calcs(self, wallthick_data):
    #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
    #      expected_t_b_nom, expected_t_rec, expected_P_st,
    #      expected_P_lt) = wallthick_data

    def test_run_analysis(self, wallthick_data):
        (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
         expected_t_b_nom, expected_t_rec, expected_P_st,
         expected_P_lt) = wallthick_data
        results = wallthick.results
        assert abs(results["thicknesses"]["t_r_nom"] - expected_t_r_nom) < 1e-5

    # def test_write_results(self, tmpdir, wallthick_data):
    #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
    #      expected_t_b_nom, expected_t_rec, expected_P_st,
    #      expected_P_lt) = wallthick_data
    #     file = tmpdir.join("hello.txt")
    #     file.write('Hello')
    #     wallthick.write_results()
    #     assert p.read() == "content"
    #     assert len(tmpdir.listdir()) == 1

    # def test_initial_calcs(self, wallthick_data):
    #     results = wallthick_data[0].results
    #     assert isinstance(results, dict)

    # def test_thickness_reel(self, wallthick_data):
    #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
    #      expected_t_b_nom, expected_P_st, expected_P_lt) = wallthick_data
    #     assert abs(wallthick.t_r_nom - expected_t_r_nom) < 1e-5

    # def test_thickness_hoop(self, wallthick_data):
    #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
    #      expected_t_b_nom, expected_P_st, expected_P_lt) = wallthick_data
    #     assert abs(wallthick.t_h_nom - expected_t_h_nom) < 1e-5

    # def test_thickness_collapse(self, wallthick_data):
    #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
    #      expected_t_b_nom, expected_P_st, expected_P_lt) = wallthick_data
    #     assert abs(wallthick.t_c_nom - expected_t_c_nom) < 1e-5

    # def test_thickness_buckle(self, wallthick_data):
    #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
    #      expected_t_b_nom, expected_P_st, expected_P_lt) = wallthick_data
    #     assert abs(wallthick.t_b_nom - expected_t_b_nom) < 1e-5

    # def test_strength_test_pressure(self, wallthick_data):
    #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
    #      expected_t_b_nom, expected_P_st, expected_P_lt) = wallthick_data
    #     assert abs(wallthick.P_st - expected_P_st) < 1e4

    # def test_leak_test_pressure(self, wallthick_data):
    #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
    #      expected_t_b_nom, expected_P_st, expected_P_lt) = wallthick_data
    #     assert abs(wallthick.P_lt - expected_P_lt) < 1e4
