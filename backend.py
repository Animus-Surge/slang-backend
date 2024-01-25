#!/usr/bin/env python3
"""
Slang - An open source social media platform
Backend module

Author: Surge
Version: 0.1.0
License: Apache 2.0
"""

import slang_backend
from loguru import logger
import psycopg
import sys
import tests
"""
TODO BOARD:

- Administration system
- Test database
...
"""

if __name__ == "__main__":
  # Check if --remigrate flag is set
  if len(sys.argv) > 1:
    arg = sys.argv[1]
    
    # Remigrate clears ALL the data from the database
    if arg == '--remigrate':
      # Confirm if the user actually wants to do this
      logger.warning('THIS OPERATION WILL DELETE ALL DATA. Continue? y/N')
      conf = input('> ')

      if conf.lower() != 'y':
        logger.info('Aborting...')
        exit(0)

      logger.info('Running...')

      # Load and run the dropall migration
      conn = psycopg.connect('dbname=slangdb user=postgres')
      cur = conn.cursor()

      with open('./sql_migrations/slangdb-dropall.sql', 'r') as mig:
        try:
          cur.execute(mig.read())
        except psycopg.errors.SyntaxError:
          logger.exception('Syntax error whilst attempting database migration run')
          exit(1)

      conn.commit()

      logger.success('Table drop complete.')
      exit(0)
    elif arg == '--test':
      logger.info('Running test system...')

      tests.run_tests()

      exit(0)
    else:
      logger.error(f'Unknown argument {arg}')
      exit(1)

  # Run main
  slang_backend.main()