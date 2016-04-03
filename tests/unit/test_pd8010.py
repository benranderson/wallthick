import pytest
from tests.unit.test_headers import *
from wallthick.codes.pd8010 import req_thickness


@pytest.fixture(params=[
    # tuple with (t, t_corr, f_tol, expected)
    ((2, 2, 0.5, 8)),
    ((1, 1, 1, "Divide by zero")),
    ((2, 2, 0.5, 8))
    ])
def test_data(request):
    return request.param


def test_req_thickness(test_data):
    (t, t_corr, f_tol, expected) = test_data

    if expected == "Divide by zero":
        with pytest.raises(ZeroDivisionError):
            req_thickness(t, t_corr, f_tol)
    else:
        assert req_thickness(t, t_corr, f_tol) == expected
