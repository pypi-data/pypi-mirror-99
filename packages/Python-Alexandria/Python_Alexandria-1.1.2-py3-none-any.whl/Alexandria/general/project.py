import os
import sys


def root():
    """
    :return: Project root directory
    """
    return os.path.dirname(sys.modules['__main__'].__file__)
