import unittest
from loguru import logger

from ..slang_backend import dbhandler

class TestDatabaseFunctions(unittest.TestCase):
  def setUp(self):
    dbhandler.__test()
  

def run_tests():
  logger.info('Running unit tests...')
  unittest.main()
  logger.info('Finished running tests.')