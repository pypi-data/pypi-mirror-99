import unittest
from tests import test_osio,test_utils

loader = unittest.TestLoader()
suite = unittest.TestSuite()


suite.addTest(loader.loadTestsFromModule(test_osio))
suite.addTest(loader.loadTestsFromModule(test_utils))

runner = unittest.TextTestRunner(verbosity=3)

if __name__ == '__main__':
    result = runner.run(suite)