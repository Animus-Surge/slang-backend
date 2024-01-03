"""
Database handler for Slang

Changelog:
Surge: Initial Commit
Surge: Create migration system, add init function, add database functions
"""

import psycopg
from loguru import logger

conn = None

# Database functions

def create_message(group: int, channel: int, user: int, content: str):
  """
  Create message in database

  Args:
    group (int): ID of group to create message in
    channel (int): ID of channel to create message in
    user (int): ID of user to create message as
    content (str): Content of message

  Returns:
    int: ID of message
  """
  global conn
  cur = conn.cursor()

  cur.execute("INSERT INTO sl_msgs (group_id, channel_id, user_id, content) VALUES (%s, %s, %s, %s) RETURNING id;", (group, channel, user, content))
  conn.commit()

  return cur.fetchone()[0]

def get_messages(group: int, channel: int):
  """
  Get messages from database

  Args:
    group (int): ID of group to get messages from
    channel (int): ID of channel to get messages from

  Returns:
    list: List of messages
  """
  global conn
  cur = conn.cursor()
  cur.execute("SELECT * FROM sl_msgs WHERE group_id=%s AND channel_id=%s;", (group, channel))
  return cur.fetchall()

def init():
  global conn
  logger.info("Initializing database...")

  conn = psycopg.connect("dbname=slangdb user=postgres")

  # Do some checking to see if we need to initialize the database
  cur = conn.cursor()

  # Check if database is initialized
  cur.execute("SELECT * FROM information_schema.tables WHERE table_name='sl_msgs';")
  if cur.rowcount == 0:
    # Database is not initialized, initialize it
    # Load schema from ./sql_migrations/slangdb-migrations.sql
    logger.info("Database not initialized, initializing...")
    with open("./sql_migrations/slangdb-migrations.sql", "r") as f:
      cur.execute(f.read())
    conn.commit()

  logger.info("Database initialized.")
  pass