import pytest
import importlib
from .context import inputs


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
        pipe = inputs.Pipe(None, D_o, None, None, None, None, None, None)
        assert pipe.thin_wall_check(t) is expected
