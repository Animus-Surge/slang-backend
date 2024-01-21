"""
Slang database models

Changelog:
Surge: Create models
Surge - 01/08/24: Model work
Surge - 01/17/24: Rewrite models for clarity
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
# Most people should be able to access all the fields
class Message(BaseModel):
  id: int
  groupID: int
  channelID: int
  author: int
  authorDname: str
  content: str
  edited: bool
  stamp: datetime.datetime

# Users

class NewUser(BaseModel): # Only gets called from the frontend after auth has been completed
  guid: str
  username: str

class UpdateUser(BaseModel): # Null fields indicate not changed
  id: int
  username: str
  displayname: str
  bio: str
  status: str
  pronouns: str
# Depending on your auth header, some fields will be null
class User(BaseModel):
  id: int
  guid: str
  username: str
  displayname: str
  bio: str
  status: str
  pronouns: str
  flags: int
  groups: list[int]
  friends: list[int]
  blocked: list[int]
  # Lockdown field NOT shown to anyone except slang staff

# Groups
class Group(BaseModel):
  id: int
  name: str
  owner: int
  banner: str
  roles: list[int]
  admins: list[int]

class NewGroup(BaseModel):
  name: str
  owner: int

# Channels
class Channel(BaseModel):
  id: int
  name: str
  description: str
  pins: list[int]
  group_id: int
  channel_group_id: int # Future proofing
  role_overrides: list[str]
  sensitive: bool

class NewChannel(BaseModel):
  name: str
  group_id: int
  sensitive: bool

class UpdateChannel(BaseModel):
  name: str
  description: str
  channel_group_id: int
  sensitive: bool

# Roles
class Role(BaseModel):
  pass

# Posts
class Post(BaseModel):
  pass