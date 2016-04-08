"""
Python module header
"""

import timeit
import importlib
import sys
from wallthick.input_classes import read_input_data
from wallthick.codes.pd8010 import WallThick
from wallthick.post_process import post_process


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def main(case):
    """ Manager function to carry out input data reading, analysis and post
    processing
    """
    data = read_input_data(case)
    wallthick = WallThick(data)
    wallthick.write_results()

if __name__ == "__main__":  # pragma: no cover
    # Determine case on which to run analysis from cmd line arg
    case_file = sys.argv[1]
    # Import module associated with case
    case = importlib.import_module("input_data_files.{}".format(case_file))

    # wrapped_main = wrapper(main, case)
    # print(timeit.timeit(wrapped_main, number=10000)/10000)

    main(case)
