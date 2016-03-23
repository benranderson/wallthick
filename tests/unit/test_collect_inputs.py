import importlib
from wallthick.input_classes import InputData
from wallthick.collect_inputs import collect_inputs


def test_collect_inputs():
    pipe = importlib.import_module("wallthick.input_data_files.pipe1")
    input_data = collect_inputs(pipe)
    assert isinstance(input_data, InputData)
