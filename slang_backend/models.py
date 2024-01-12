"""
Slang database models

Changelog:
Surge: Create models
Surge - 01/08/24: Model work
"""

from pydantic import BaseModel
import datetime

class Message(BaseModel):
  id: int
  author: int
  content: str
  group_id: int
  channel_id: int
  send_date: datetime.datetime
  edited: bool
class NewMessage(BaseModel):
  author: int
  content: str
  group_id: int
  channel_id: int

class Post(BaseModel):
  id: int
  title: str
  author: int
  content: str
  group_id: int
class NewPost(BaseModel):
  title: str
  author: int
  group_id: int
  content: str

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
  pass

class User(BaseModel):
  id: int
  guid: str
  username: str
  displayname: str
  bio: str
  status: str
  pronouns: str
  flags: str
  groups: list[int]
  friends: list[int]
  blocked: list[int]
  posts: list[int]
  lockdown: bool
class NewUser(BaseModel):
  username: str
  flags: str

class Role(BaseModel):
  id: int
  name: str
  permissions: int
  color: int
  users: list[int]
class NewRole(BaseModel):
  name: str

class Channel(BaseModel):
  id: int
  name: str
  group_id: int
  role_overrides: list[str]
  sensitive: bool
class NewChannel(BaseModel):
  name: str
  group_id: int