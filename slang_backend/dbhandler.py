"""
Database handler for Slang

Changelog:
Surge: Initial Commit
Surge: Create migration system, add init function, add database functions
Surge - 01/07/24: Add migration error checking, testing
Surge - 01/17/24: Add initial messenger data handling
Surge - 01/30/24: Remove functionality, database rework in progress
"""

import psycopg
from loguru import logger

from .models import NewMessage, NewChannel, NewGroup, NewUser

conn = None

# Database functions

#Check functions
def check_group_exists(group_id: int):
  pass

def check_channel_exists(channel_id: int):
  pass

def check_message_exists(message_id: int):
  pass

def check_channel_in_group(channel_id: int, group_id: int):
  pass

#User functions
def create_new_user(user: NewUser):
  pass
#Message functions
def create_new_message(message: NewMessage):
  pass

#Channel functions
def create_new_channel(channel: NewChannel):
  pass

#Group functions
def create_new_group(group: NewGroup):
  pass

# Initialization
def init():
  logger.warning('Database rework in progress, database handler is not functional')
  return True

# Slangdb Test System
def __test():
  logger.error('Database rework in progress, database handler is not functional')
