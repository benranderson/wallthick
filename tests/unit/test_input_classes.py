import importlib
from wallthick.input_classes import read_input_data
from wallthick.input_classes import InputData
from wallthick.input_classes import Pipe
from wallthick.input_classes import Environment


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_read_input_data():
    case = importlib.import_module(
        "wallthick.input_data_files.pipe1")
    data = read_input_data(case)
    assert isinstance(data, InputData)


class TestPipe:
    def test_thin_wall_check(self):
        pipe = Pipe(None, 20, None, None, None, None)
        assert pipe.thin_wall_check(1) is True
        assert pipe.thin_wall_check(0.5) is True
        assert pipe.thin_wall_check(2) is False


class TestEnvironment:
    def test_hydro_pressure(self):
        assert Environment(100).hydro_pressure() == 1005525
