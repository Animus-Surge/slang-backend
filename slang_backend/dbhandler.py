"""
Database handler for Slang

Changelog:
Surge: Initial Commit
Surge: Create migration system, add init function, add database functions
Surge - 01/07/24: Add migration error checking, testing
"""

import psycopg
from loguru import logger

conn = None

# Database functions

#Message functions

def create_new_message():
  pass

# Initialization
def init():
  global conn

  logger.info("Initializing database...")

  conn = psycopg.connect("dbname=slangdb user=postgres")
  cur = conn.cursor()

  with open('./sql_migrations/slangdb-migrations.sql', 'r') as mig:
    try:
      cur.execute(mig.read())
    except psycopg.errors.SyntaxError:
      logger.exception('Syntax error whilst attempting database migration run')
      return False

  conn.commit()

  logger.info("Database initialized.")
  return True

