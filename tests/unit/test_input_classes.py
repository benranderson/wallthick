import pytest
from tests.unit.test_headers import *
import importlib
from wallthick.input_classes import read_input_data
from wallthick.input_classes import InputData
from wallthick.input_classes import Pipe
from wallthick.input_classes import Environment


def test_read_input_data():
    # Update to set up and teardown input data file
    case = importlib.import_module(
        "input_data_files.test_data_file")
    data = read_input_data(case)
    assert isinstance(data, InputData)


class TestPipe:
    @pytest.fixture(params=[
        # tuple with (D_o, t, expected)
        (20, 1, True),
        (20, 0.5, True),
        (20, 2, False)
        ])
    def test_cases(self, request):
        print('param       : {}'.format(request.param))
        return request.param

    def test_thin_wall_check(self, test_cases):
        (D_o, t, expected) = test_cases
        pipe = Pipe(None, D_o, None, None, None, None, None, None)
        assert pipe.thin_wall_check(t) is expected


class TestEnvironment:
    @pytest.fixture(params=[
        # tuple with (d, grav, expected)
        (100, 9.81, 1005525),
        (0, 9.81, 0),
        ])
    def test_cases(self, request):
        return request.param

    def test_hydro_pressure(self, test_cases):
        (d, grav, expected) = test_cases
        assert Environment(None, None, g=grav).hydro_pressure(d) == expected
