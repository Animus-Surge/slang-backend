"""
Slang database models

Changelog:
Surge: Create models
Surge - 01/08/24: Model work
"""

from typing import Union

from pydantic import BaseModel
import datetime

# Query options

class QueryOptions(BaseModel):
  author: Union[int, None]
  group: Union[int, None]
  channel: Union[int, None]

  # TODO: more query options

# Messages

class NewMessage(BaseModel):
  author: int
  content: str
  group_id: int
  channel_id: int

class UpdateMessage(BaseModel):
  message: int
  content: str

class Message(BaseModel):
  id: int
  groupID: int
  channelID: int
  author: int
  authorDname: str
  content: str
  edited: bool
  stamp: datetime.datetime

