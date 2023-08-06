import os
import unittest


def suite():
    # Be sure to be on the top level directory of package
    return unittest.TestLoader().discover(
        os.path.join(os.path.dirname(__file__), '..'),
        pattern='*_test.py')


def run_tests():
    return unittest.TextTestRunner(verbosity=2).run(suite())


if __name__ == '__main__':
    if run_tests().wasSuccessful():
        exit(0)
    else:
        exit(1)
