from __future__ import print_function
import pytest
import time


@pytest.fixture(scope="module", autouse=True)
def mod_header(request):
    print('\n-----------------')
    print('module      : {}'.format(request.module.__name__))
    print('-----------------')


@pytest.fixture(scope="function", autouse=True)
def func_header(request):
    print('\n-----------------')
    print('function    : %s' % request.function.__name__)
    print('time        : %s' % time.asctime())

    # print('\n-----------------')
    # print('fixturename : %s' % request.fixturename)
    # print('scope       : %s' % request.scope)
    # # print('function    : %s' % request.function.__name__)
    # print('cls         : %s' % request.cls)
    # print('module      : %s' % request.module.__name__)
    # print('fspath      : %s' % request.fspath)
    # print('param      : %s' % request.param)
    # print('-----------------')
