import unittest
from loguru import logger

# TODO

def run_tests():
  logger.info('Running unit tests...')
  unittest.main(argv=['backend.py'], exit=False)
  logger.info('Finished running tests.')