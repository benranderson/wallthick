from __future__ import print_function
import pytest
from wallthick.input_classes import Pipe
from wallthick.input_classes import Environment
from wallthick.input_classes import Process
from wallthick.input_classes import InputData
from wallthick.analysis import WallThick
from wallthick.input_data_files.db_materials import materials


@pytest.fixture(scope='class', params=[
    # tuple with (WallThick(InputData(name,
    #                                 Pipe(t_sel, D_o, t_corr, f_tol, f_0,
    #                                      material),
    #                                 Process(T_d, P_d, P_h, T_t),
    #                                 Environment(d_max, d_min, T_a, rho_w,
    #                                             g))),
    #             expected_t_h, expected_t_c, expected_t_b)
    (WallThick(InputData("pipe1",
                         Pipe(0.0111, 60.3e-3, 0, 0.125, 0.025,
                              materials["CS X65"]),
                         Process(0, 861.8e5, 0, 4),
                         Environment(114.5, 87.5, 4, 1027, 9.81))),
     8.143e-3, 1.271e-3, 1.695e-3),
    ])
def wallthick_data(request):
    return request.param


class TestWallThick:

    def test_thickness_hoop(self, wallthick_data):
        (wallthick, expected_t_h, expected_t_c, expected_t_b) = wallthick_data
        assert abs(wallthick.t_h_req - expected_t_h) < 1e-6

    def test_thickness_collapse(self, wallthick_data):
        (wallthick, expected_t_h, expected_t_c, expected_t_b) = wallthick_data
        assert abs(wallthick.t_c_req - expected_t_c) < 1e-6

    def test_thickness_buckle(self, wallthick_data):
        (wallthick, expected_t_h, expected_t_c, expected_t_b) = wallthick_data
        assert abs(wallthick.t_b_req - expected_t_b) < 1e-6
