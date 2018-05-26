from wallthick import pd8010 as pd
import pytest

tol_pc = 0.001

test_data = [
    {
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


@pytest.mark.parametrize("rho_w, g, d, expected", [
    (1027, 9.81, 97.95, 986800)
])
def test_external_pressure(rho_w, g, d, expected):
    assert abs(pd.external_pressure(rho_w, g, d) -
               expected) <= tol_pc * expected


@pytest.mark.parametrize("rho, g, d, h_ref, expected", [
    (1025, 9.81, 100, 0, 10.05525e5),
])
def test_pressure_head(rho, g, d, h_ref, expected):
    assert abs(pd.pressure_head(
        rho, g, d, h_ref) - expected) <= tol_pc * expected


def test_allowable_hoop_stress():
    assert pd.allowable_hoop_stress(100) == 72


@pytest.mark.xfail
@pytest.mark.parametrize("t, D_o, P_o, sig, expected", [
    (9.713e-3, 219.1e-3, None, 405, 187.392e5),
])
def test_hoop_pressure_thin(t, D_o, P_o, sig, expected):
    assert abs(pd.hoop_pressure_thin(
        t, D_o, P_o, sig) - expected) <= tol_pc * expected


@pytest.mark.xfail
@pytest.mark.parametrize("t, D_o, P_o, sig, expected", [
    (None, None, None, None, 187.392e5),
])
def test_hoop_pressure_thick(t, D_o, P_o, sig, expected):
    assert abs(pd.hoop_pressure_thick(
        t, D_o, P_o, sig) - expected) <= tol_pc * expected


@pytest.mark.parametrize("P_i, P_o, D_o, sig_A, expected", [
    (187.392e5, 809171.21, 219.1e-3, 324e6, 6.06e-3),
])
def test_hoop_thickness_thin(P_i, P_o, D_o, sig_A, expected):
    assert abs(pd.hoop_thickness_thin(
        P_i, P_o, D_o, sig_A) - expected) <= tol_pc * expected


@pytest.mark.parametrize("P_i, P_o, D_o, sig_A, expected", [
    (187.392e5, 809171.21, 219.1e-3, 324e6, 5.9e-3),
])
def test_hoop_thickness_thick(P_i, P_o, D_o, sig_A, expected):
    assert abs(pd.hoop_thickness_thick(
        P_i, P_o, D_o, sig_A) - expected) <= tol_pc * expected


@pytest.mark.parametrize("P_i, P_o, D_o, sig_A, expected", [
    (187.392e5, 809171.21, 219.1e-3, 324e6, 5.9e-3),
    (187.392e5, 809171.21, 219.1e-3, 324e6, 5.9e-3),
])
def test_hoop_thickness(P_i, P_o, D_o, sig_A, expected):
    assert abs(pd.hoop_thickness(
        P_i, P_o, D_o, sig_A) - expected) <= tol_pc * expected


@pytest.mark.parametrize("t_min, t_corr, f_tol, expected", [
    (2, 2, 0, 4)
])
def test_req_thickness(t_min, t_corr, f_tol, expected):
    assert pd.req_thickness(t_min, t_corr, f_tol) == expected


def test_req_thickness_zerodiv():
    with pytest.raises(ZeroDivisionError):
        pd.req_thickness(1, 1, 1)


@pytest.mark.parametrize("P_o, sig_y, E, v, D_o, f_0, expected", [
    (23.071e5, 450e6, 207e9, 0.3, 60.3e-3, 2.5e-2, 1.112316e-3)
])
def test_collapse_thickness(P_o, sig_y, E, v, D_o, f_0, expected):
    assert abs(pd.collapse_thickness(
        P_o, sig_y, E, v, D_o, f_0) - expected) <= tol_pc * expected


@pytest.mark.parametrize("D_o, P_p, sig_y, expected", [
    (60.3e-3, 11.536e5, 450e6, 1.483e-3)
])
def test_buckle_thickness(D_o, P_p, sig_y, expected):
    assert abs(pd.buckle_thickness(
        D_o, P_p, sig_y) - expected) <= tol_pc * expected


@pytest.mark.parametrize("D_o, R_reel, t_coat, expected", [
    (219.1e-3, 7.5, 2.5e-3, 8.29e-3),
    (114.3e-3, 0, 2.5e-3, 0)
])
def test_reeling_thickness(D_o, R_reel, t_coat, expected):
    assert abs(pd.reeling_thickness(
        D_o, R_reel, t_coat) - expected) <= tol_pc * expected


@pytest.mark.xfail
@pytest.mark.parametrize("t_sel, f_tol, sig_y, D_o, P_d, P_o, P_h, expected", [
    (None, None, None, None, None, None, None, None)
])
def test_strength_test_pressure(t_sel, f_tol, sig_y, D_o, P_d, P_o, P_h, expected):
    assert abs(pd.strength_test_pressure(
        t_sel, f_tol, sig_y, D_o, P_d, P_o, P_h) - expected) <= tol_pc * expected


@pytest.mark.parametrize("P_d, expected", [
    (100e5, 110e5),
    (0, 0)
])
def test_leak_test_pressure(P_d, expected):
    assert abs(pd.leak_test_pressure(P_d) - expected) <= tol_pc * expected


test_cases = [{"pipe": Pipe(0.0111, 219.1e-3, 1.5e-3, 0.125, 0.025, 0.1,
                            "CS X65", 2.5e-3),
               "process": Process(50, 179.3e5, 0, 1025, 7.5, 0),
               "env": Environment(124.247, 80.5, 3.6, 1025, 9.80665)},
              {"pipe": Pipe(0.0111, 219.1e-3, 1.5e-3, 0.125, 0.025, 0.1,
                            "CS X65", 2.5e-3),
               "process": Process(50, 179.3e5, 0, 1025, 7.5, 0),
               "env": Environment(124.247, 80.5, 3.6, 1025, 9.80665)},
              {"pipe": Pipe(0.0064, 114.3e-3, 1.5e-3, 0.125, 0.025, 0.1,
                            "CS X65", 2.5e-3),
               "process": Process(50, 179.3e5, 0, 1025, 0, 0),
               "env": Environment(124.247, 80.5, 3.6, 1025, 9.80665)}]


@pytest.mark.xfail
@pytest.mark.parametrize("test_cases, expected", [
    (test_cases[0], {"sig_y_d": 1,
                     "P_h_d": 1,
                     "P_i": 1,
                     "P_o_min": 1,
                     "P_o_max": 1
                     }
     ),
    (test_cases[1], {"sig_y_d": 1,
                     "P_h_d": 1,
                     "P_i": 1,
                     "P_o_min": 1,
                     "P_o_max": 1
                     }
     ),
    (test_cases[2], {"sig_y_d": 1,
                     "P_h_d": 1,
                     "P_i": 1,
                     "P_o_min": 1,
                     "P_o_max": 1
                     }
     )
])
def test_pd_prelim_vals(test_cases, expected):
    pd = pd.pd(test_cases["pipe"], test_cases["process"],
               test_cases["env"])
    assert abs(pd._prelim_calcs()["sig_y_d"] -
               expected["sig_y_d"]) <= tol_pc * expected["sig_y_d"]
    assert abs(pd._prelim_calcs()["P_h_d"] -
               expected["P_h_d"]) <= tol_pc * expected["P_h_d"]
    assert abs(pd._prelim_calcs()["P_i"] -
               expected["P_i"]) <= tol_pc * expected["P_i"]
    assert abs(pd._prelim_calcs()["P_o_min"] -
               expected["P_o_min"]) <= tol_pc * expected["P_o_min"]
    assert abs(pd._prelim_calcs()["P_o_max"] -
               expected["P_o_max"]) <= tol_pc * expected["P_o_max"]


@pytest.mark.xfail
@pytest.mark.parametrize("test_cases, expected", [
    (test_cases[0], {"t_r_nom": 1,
                     "t_h_nom": 1,
                     "t_h_nom_bt": 1,
                     "t_c_nom": 1,
                     "t_b_nom": 1,
                     "t_rec": 1
                     }
     ),
    (test_cases[1], {"t_r_nom": 1,
                     "t_h_nom": 1,
                     "t_h_nom_bt": 1,
                     "t_c_nom": 1,
                     "t_b_nom": 1,
                     "t_rec": 1
                     }
     ),
    (test_cases[2], {"t_r_nom": 1,
                     "t_h_nom": 1,
                     "t_h_nom_bt": 1,
                     "t_c_nom": 1,
                     "t_b_nom": 1,
                     "t_rec": 1
                     }
     )
])
def test_pd_wallthicks(test_cases, expected):
    pd = pd.pd(test_cases["pipe"], test_cases["process"],
               test_cases["env"])
    assert abs(pd._thickness_calcs()["t_r_nom"] -
               expected["t_r_nom"]) <= tol_pc * expected["t_r_nom"]
    assert abs(pd._thickness_calcs()["t_h_nom"] -
               expected["t_h_nom"]) <= tol_pc * expected["t_h_nom"]
    assert abs(pd._thickness_calcs()[
               "t_h_nom_bt"] - expected["t_h_nom_bt"]) <= tol_pc * expected["t_h_nom_bt"]
    assert abs(pd._thickness_calcs()["t_c_nom"] -
               expected["t_c_nom"]) <= tol_pc * expected["t_c_nom"]
    assert abs(pd._thickness_calcs()["t_b_nom"] -
               expected["t_b_nom"]) <= tol_pc * expected["t_b_nom"]
    assert abs(pd._thickness_calcs()["t_rec"] -
               expected["t_rec"]) <= tol_pc * expected["t_rec"]


@pytest.mark.xfail
@pytest.mark.parametrize("test_cases, expected", [
    (test_cases[0], {"P_st": 268.9e5,
                     "P_lt": 197.23e5
                     }
     ),
    (test_cases[1], {"P_st": 268.9e5,
                     "P_lt": 197.23e5
                     }
     ),
    (test_cases[2], {"P_st": 268.9e5,
                     "P_lt": 197.23e5
                     }
     )
])
def test_pd_test_pressures(test_cases, expected):
    pd = pd.pd(test_cases["pipe"], test_cases["process"],
               test_cases["env"])
    P_o_min = pd._prelim_calcs()["P_o_min"]
    assert abs(pd._test_pressure_calcs(P_o_min)[
               "P_st"] - expected["P_st"]) <= tol_pc * expected["P_st"]
    assert abs(pd._test_pressure_calcs(P_o_min)[
               "P_lt"] - expected["P_lt"]) <= tol_pc * expected["P_lt"]

# @pytest.fixture(scope='class', params=[
#     # tuple with (WallThick(InputData(name,
#     #                                 Pipe(t_sel, D_o, t_corr, f_tol, f_0, B
#     #                                      material, t_coat),
#     #                                 Process(T_d, P_d, h_ref, rho_d, R_reel,
#     #                                         T_lay),
#     #                                 Environment(d_max, d_min, T_a, rho_w,
#     #                                             g))),
#     #             expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
#     #             expected_t_b_nom, expected_t_rec, expected_P_st,
#     #             expected_P_lt)
#     (pd.WallThick(InputData("Aviat 8in X65",
#                                 Pipe(0.0111, 219.1e-3, 1.5e-3, 0.125, 0.025,
#                                      0.1, materials["CS X65"], 2.5e-3),
#                                 Process(50, 179.3e5, 0, 1025, 7.5, 0),
#                                 Environment(124.247, 80.5, 3.6, 1025,
#                                             9.80665))),
#      8.29e-3, 8.64e-3, 3.25e-3, 5.58e-3, 11.1e-3, 268.9e5, 197.23e5),
#     (pd.WallThick(InputData("Aviat 4in X65",
#                                 Pipe(0.0064, 114.3e-3, 1.5e-3, 0.125, 0.025,
#                                      0.1, materials["CS X65"], 2.5e-3),
#                                 Process(50, 179.3e5, 0, 1025, 0, 0),
#                                 Environment(124.247, 80.5, 3.6, 1025,
#                                             9.80665))),
#      0, 5.33e-3, 1.7e-3, 2.91e-3, 14.3e-3, 268.9e5, 197.23e5),
# ])
# def wallthick_data(request):
#     return request.param


# class TestWallThick:

#     # def test_initial_calcs(self, wallthick_data):
#     #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
#     #      expected_t_b_nom, expected_t_rec, expected_P_st,
#     #      expected_P_lt) = wallthick_data

#     def test_t_r_nom(self, wallthick_data):
#         (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
#          expected_t_b_nom, expected_t_rec, expected_P_st,
#          expected_P_lt) = wallthick_data
#         assert abs(wallthick.results["t_r_nom"] - expected_t_r_nom) <= 1e-5

#     # def test_write_results(self, tmpdir, wallthick_data):
#     #     (wallthick, expected_t_r_nom, expected_t_h_nom, expected_t_c_nom,
#     #      expected_t_b_nom, expected_t_rec, expected_P_st,
#     #      expected_P_lt) = wallthick_data
#     #     file = tmpdir.join("hello.txt")
#     #     file.write('Hello')
#     #     wallthick.write_results()
#     #     assert p.read() == "content"
#     #     assert len(tmpdir.listdir()) == 1
