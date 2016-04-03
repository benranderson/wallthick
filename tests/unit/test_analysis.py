from __future__ import print_function
import pytest
from wallthick.input_classes import Pipe
from wallthick.input_classes import Environment
from wallthick.input_classes import Process
from wallthick.input_classes import InputData
from wallthick.analysis import WallThick


@pytest.fixture(scope='class', params=[
    # name
    "pipe1",
    "pipe2",
    "pipe3",
    ],
    autouse=False)
def wallthick_data(request):
    print('\n-----------------')
    print('fixturename : %s' % request.fixturename)
    print('scope       : %s' % request.scope)
    # print('function    : %s' % request.function.__name__)
    print('cls         : %s' % request.cls)
    print('module      : %s' % request.module.__name__)
    print('fspath      : %s' % request.fspath)
    print('param      : %s' % request.param)
    print('-----------------')

    pipe = Pipe(None, None, None, None, None, None)
    environment = Environment(None, None, None, None)
    process = Process(None, None, None)
    data = InputData(request.param, pipe, process, environment)

    return WallThick(data)


class TestWallThick:
    @pytest.fixture(params=[
        # tuple with (input, expectedOutput)
        (1, 2),
        (2, 3),
        (3, 4)
        ])
    def test_data(self, request):
        return request.param

    def test_calculate_hoop_thickness(self, wallthick_data, test_data):
        (the_input, the_expected_output) = test_data
        print(wallthick_data)
        assert wallthick_data.calculate_hoop_thickness(the_input) == the_expected_output
