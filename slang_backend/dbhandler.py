"""
Database handler for Slang

Changelog:
Surge: Initial Commit
Surge: Create migration system, add init function, add database functions
Surge - 01/07/24: Add migration error checking, testing
Surge - 01/17/24: Add initial messenger data handling
"""

import psycopg
from loguru import logger

from .models import NewMessage, NewChannel, NewGroup, NewUser

conn = None

# Database functions

#Check functions
def check_group_exists(group_id: int):
  cur = conn.cursor()

  cur.execute(f'SELECT id FROM sl_grps WHERE id={group_id};')
  rowid = cur.fetchone()[0]

  return rowid == group_id

def check_channel_exists(channel_id: int):
  cur = conn.cursor()

  cur.execute(f'SELECT id FROM sl_chnl WHERE id={channel_id};')
  rowid = cur.fetchone()[0]

  return rowid == channel_id

def check_message_exists(message_id: int):
  cur = conn.cursor()

  cur.execute(f'SELECT id FROM sl_msgs WHERE id={message_id};')  
  rowid = cur.fetchone()[0]

  return rowid == message_id

def check_channel_in_group(channel_id: int, group_id: int):
  cur = conn.cursor()

  cur.execute(f'SELECT group_id FROM sl_chnl WHERE id={channel_id}')
  rowid = cur.fetchone()[0]

  return rowid == group_id

#User functions
def create_new_user(user: NewUser):
  cur = conn.cursor()

  try:
    cur.execute(f"INSERT INTO sl_usrs(guid, username) VALUES ('{user.guid}', '{user.username}') RETURNING id;")
    rowid = cur.fetchone()[0]
    conn.commit()

    retmsg = (200, rowid)
  except Exception:
    logger.exception('Failed to create a new user')
    retmsg = (500, 'Error inserting into database')
  
  return retmsg

#Message functions
def create_new_message(message: NewMessage):
  retmsg = None

  # Checking to make sure that the channel and group exists, and the channel exists in the group
  if not check_group_exists(message.group_id):
    retmsg = (404, 'Group does not exist')
    return retmsg
  
  if not check_channel_exists(message.channel_id):
    retmsg = (404, 'Channel does not exist')
    return retmsg

  if not check_channel_in_group(message.channel_id, message.group_id):
    retmsg = (400, 'Channel does not exist in group')
    return retmsg
  
  cur = conn.cursor()

  try:
    cur.execute(f'INSERT INTO sl_msgs(author, content, group_id, channel_id) VALUES ({message.author}, \'{message.content}\', {message.group_id}, {message.channel_id}) RETURNING id;')
    rowid = cur.fetchone()[0]
    conn.commit()

    retmsg = (200, rowid)
  except Exception:
    logger.exception('Failed to create a new message')
    retmsg = (500, 'Error inserting into database')

  return retmsg

#Channel functions
def create_new_channel(channel: NewChannel):
  retmsg = None
  # Checking to make sure that the group exists
  if check_group_exists(channel.group_id):
    data = (channel.name, channel.group_id, channel.sensitive)
    cur = conn.cursor()
    try:
      cur.execute(f'INSERT INTO sl_chnl (name, group_id, sensitive) VALUES (\'{data[0]}\', \'{data[1]}\', \'{data[2]}\') RETURNING id;')
      rowid = cur.fetchone()[0]
      conn.commit()

      retmsg = (200, rowid)
    except Exception:
      logger.exception('Failed to create a new channel')
      retmsg = (500, 'Error inserting into database')
  # Doesn't exist, therefore we cannot continue.
  else:
    retmsg = (404, 'Specified group does not exist')

  return retmsg

#Group functions
def create_new_group(group: NewGroup):
  cur = conn.cursor()

  retmsg = None

  try:
    cur.execute(f'INSERT INTO sl_grps(name, owner) VALUES (\'{group.name}\', {group.owner}) RETURNING id;')
    rowid = cur.fetchone()[0]
    conn.commit()

    retmsg = (200, rowid)
  except Exception:
    logger.exception('Failed to create a new group')
    retmsg = (500, 'Error inserting into database')
  finally:
    cur.close()
  
  return retmsg

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

# Slangdb Test System
def __test():
  # Initialize test database in slangdb_test db

  global conn
  logger.info('Initializing database testing...')
  conn = psycopg.connect('dbname=slangdb_test user=postgres')

  # Clear everything before trying again (yes its expensive I know)
  cur = conn.cursor()
  with open('./sql_migrations/slangdb-dropall.sql', 'r') as drop:
    cur.execute(drop.read())
  
  conn.commit()

  # Create the tables in our test database
  with open('./sql_migrations/slangdb-migrations.sql', 'r') as mig:
    try:
      cur.execute(mig.read())
    except psycopg.errors.SyntaxError:
      logger.exception('Syntax error whilst attempting database migration run in test')
      return
  
  conn.commit()

  logger.info('Test database initialized.')
