-- Slang Backend Postgres Database Migrations
-- This file contains all the migrations for the slang backend database
-- The migrations are run in order, and are idempotent
-- Author: Surge
-- Version: 0.1.0
-- Date: 2023-12-26

-- Create the messages table
CREATE TABLE IF NOT EXISTS sl_msgs (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  author INTEGER NOT NULL,
  groupid INTEGER NOT NULL,
  channelid INTEGER NOT NULL,
  sendDate TIMESTAMP NOT NULL DEFAULT NOW(),
);

-- TODO: groups, channels, roles, posts

-- Create the users table
CREATE TABLE IF NOT EXISTS sl_usrs (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  displayname TEXT,
  flags TEXT NOT NULL DEFAULT "",
  groups TEXT,
  friends TEXT,
  posts TEXT,
  lockdown BOOLEAN NOT NULL DEFAULT FALSE,
  UNIQUE(username)
);