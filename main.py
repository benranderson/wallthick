"""
Python module header
"""

import importlib
import sys
from wallthick.input_classes import read_input_data
from wallthick.analysis import WallThick
from wallthick.post_process import post_process


def main(case):
    """ Manager function to carry out input data reading, analysis and post
    processing
    """
    data = read_input_data(case)
    analysis = WallThick(data)
    post_process(analysis)

if __name__ == "__main__":  # pragma: no cover
    # Determine case on which to run analysis from cmd line arg
    case_file = sys.argv[1]
    # Import module associated with case
    case = importlib.import_module("input_data.{}".format(case_file))

    main(case)
