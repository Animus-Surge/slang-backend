-- Slang Backend Postgres Database Migrations
-- This file contains all the migrations for the slang backend database
-- The migrations are run in order, and are idempotent
-- Author: Surge
-- Version: 0.1.1
-- Date: 2023-12-26

-- Create the messages table
CREATE TABLE IF NOT EXISTS sl_msgs (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  author INTEGER NOT NULL,
  group_id INTEGER NOT NULL,
  channel_id INTEGER NOT NULL,
  edited BOOLEAN NOT NULL DEFAULT FALSE,
  send_date TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create the channels table
CREATE TABLE IF NOT EXISTS sl_chnl (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  pins INTEGER ARRAY,
  group_id INTEGER NOT NULL,
  role_overrides TEXT ARRAY,
  sensitive BOOLEAN NOT NULL DEFAULT FALSE
);
-- See docs/channels for role_overrides info

-- Create the posts table
CREATE TABLE IF NOT EXISTS sl_post (
  id SERIAL PRIMARY KEY,
  title TEXT,
  group_id INTEGER NOT NULL DEFAULT -1,
  op INTEGER NOT NULL,
  content TEXT NOT NULL
);
-- group -1 is public group everyone's in

-- Create the groups table
CREATE TABLE IF NOT EXISTS sl_grps (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  owner INTEGER NOT NULL,
  banner TEXT,
  roles INTEGER ARRAY,
  admins INTEGER ARRAY
);

-- Reserved groups: -10 user messages (channels will match user ids); -1 global group

-- Create the roles table
CREATE TABLE IF NOT EXISTS sl_role (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  permissions INTEGER NOT NULL DEFAULT 0,
  color INTEGER NOT NULL DEFAULT 16777215,
  users INTEGER ARRAY
);

-- Create the users table
CREATE TABLE IF NOT EXISTS sl_usrs (
  id SERIAL PRIMARY KEY,
  guid TEXT NOT NULL,
  username TEXT NOT NULL,
  displayname TEXT,
  bio TEXT,
  status TEXT,
  pronouns TEXT,
  flags INTEGER NOT NULL DEFAULT 0,
  groups INTEGER ARRAY,
  friends INTEGER ARRAY,
  blocked INTEGER ARRAY,
  posts INTEGER ARRAY,
  lockdown BOOLEAN NOT NULL DEFAULT FALSE, --Shouldn't be visible to anyone but slang staff
  UNIQUE(username, guid)
);
-- See docs/users for more info on the difference between the id and guid and flags and lockdown information