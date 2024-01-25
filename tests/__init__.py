import unittest
from loguru import logger

from slang_backend import __test, dbhandler

class TestDatabaseFunctions(unittest.TestCase):
  def setUp(self):
    dbhandler.__test()
    __test() # __init__.__test()

  def test_db_functions(self):
    rslt = dbhandler.create_new_user()
    self.assertEqual(rslt, (200, 1))

def run_tests():
  logger.info('Running unit tests...')
  unittest.main(argv=['backend.py'], exit=False)
  logger.info('Finished running tests.')