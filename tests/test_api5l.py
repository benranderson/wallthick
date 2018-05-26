import pytest
from wallthick import api5l as api


@pytest.fixture(params=[
    # tuple with (D_o, req_wt, expected)
    (60.3e-3, 4.5e-3, 4.8e-3),
    (610e-3, 8.7e-3, 8.7e-3),
])
def test_recommended_wall_thickness_data(request):
    return request.param


def test_recommended_wall_thickness(test_recommended_wall_thickness_data):
    (D_o, req_wt, expected) = test_recommended_wall_thickness_data
    assert api.recommended_wall_thickness(D_o, req_wt) == expected


def test_recommended_wall_thickness_non_api_D_o():
    with pytest.raises(KeyError):
        api.recommended_wall_thickness(100e-3, 1e-3)


def test_recommended_wall_thickness_wt_greater_than_standard():
    with pytest.raises(ValueError):
        api.recommended_wall_thickness(60.3e-3, 12e-3)
