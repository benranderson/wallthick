import pytest

from wallthick import dnvf101 as dnv


@pytest.fixture(params=[
    # tuple with (grade, sig_y, temp, expected)
    ("CS X52", 450e6, 0, 450e6),
    ("CS X52", 450e6, 100, 420e6),
    ("CS X52", 450e6, 200, 380e6),
    ("CS X52", 450e6, 250, 380e6),
    ("CS X52", 450e6, 125, 410e6),
    ("22Cr", 450e6, 100, 360e6),
    ("Wrong Input", 450e6, 100, "Value Error"),
])
def test_derate_material_data(request):
    return request.param


def test_derate_material(test_derate_material_data):
    (grade, sig_y, temp, expected) = test_derate_material_data
    if expected == "Value Error":
        with pytest.raises(ValueError):
            dnv.derate_material(grade, sig_y, temp)
    else:
        func = dnv.derate_material(grade, sig_y, temp)
        assert abs(func - expected) < 1e-6


def test_t_1():
    assert dnv.t_1(20, 1, 1) == 18


def test_t_2():
    assert dnv.t_2(20, 1) == 19


@pytest.fixture(params=[
    # tuple with (fab_ov, D_o, t_nom, t_cor, expected)
    ("dnv", 20e-3, 0, 0, 0),
    ("dnv", 100e-3, 0, 0, 0.015),
    ("dnv", 1000e-3, 100e-3, 0, 0.01),
    ("dnv", 1000e-3, 4e-3, 2e-3, 0),
    (0.1, 0, 0, 0, 0.1)
])
def test_ovality_data(request):
    return request.param


def test_ovality(test_ovality_data):
    (fab_ov, D_o, t_nom, t_cor, expected) = test_ovality_data
    assert dnv.ovality(fab_ov, D_o, t_nom, t_cor) == expected


@pytest.fixture(params=[
    # tuple with (H, delta_P, A_i, v, A_s, E, alpha, delta_T, expected)
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
])
def effective_axial_force_data(request):
    return request.param


@pytest.mark.skip(reason="do later")
def test_effective_axial_force(effective_axial_force_data):
    (H, delta_P, A_i, v, A_s, E, alpha, delta_T,
     expected) = effective_axial_force_data
    assert dnv.effective_axial_force(H, delta_P, A_i, v, A_s, E, alpha,
                                     delta_T,) == expected
