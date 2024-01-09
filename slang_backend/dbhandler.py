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
  logger.info('Method call: create_message, with arguments (group=%s, channel=%s, user=%s, content=%s)', (group, channel, user, content))

  cur = conn.cursor()

  cur.execute("INSERT INTO sl_msgs (groupid, channelid, author, content) VALUES (%s, %s, %s, %s) RETURNING id;", (group, channel, user, content))
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
  logger.info('Method call: get_messages, with arguments (group=%s, channel=%s)', (group, channel))
  cur = conn.cursor()
  cur.execute("SELECT content, author FROM sl_msgs WHERE group_id=%s AND channel_id=%s;", (group, channel))

  result = cur.fetchall()
  print(result)

  return None # TODO: convert result to json string

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

