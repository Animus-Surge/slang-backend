"""
Slang database models

Changelog:
Surge: Create models
"""

from pydantic import BaseModel

class Message(BaseModel):
  content: str
  user: int

class Group(BaseModel):
  name: str
  owner: int
  # TODO

class User(BaseModel):
  # TODO
  pass

