import unittest
import sys
import importlib
import logging
from config import LOG_FORMAT

logging.basicConfig(
    format=LOG_FORMAT,
    level=getattr(logging, 'DEBUG')
)

test = importlib.import_module("tests." + sys.argv[1])

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
