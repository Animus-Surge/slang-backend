"""
Main module, handles websocket and REST API

Changelog:
Surge: Initial commit
Surge: Move REST api to this file
Surge - 01/04/24: Move websocket handler to this file
Surge - 01/07/24: Add database init function
Surge - 01/08/24: Remove multiprocessing bullcrap and add socket testing
"""

from . import dbhandler
from .models import NewMessage
from loguru import logger
from fastapi import FastAPI, Response, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware # NOTE: No HTTPS support as of 1/4/24
import uvicorn, datetime, time  # noqa: E401

from . import sockethandler

# Config variables
REST_PORT = 8000
SOCKET_PORT = 8765

UVICORN_LOG = "./log_config.ini" # TODO: make the logs look consistent

# Utitilty vars
start_time = time.time()

app = FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)

connected_clients = []

@app.get("/")
async def root():
  return Response()

# BEGIN: API routes

# Utility routes - No auth header required for these endpoints

# GET: https://api.slang.com/v1/time - Gets the time of the server
@app.get('/v1/time')
async def api_get_time():
  ti = datetime.datetime.now()
  return Response(ti)
  
# GET: https://api.slang.com/v1/ping - Pings the server for uptime
@app.get('/v1/uptime')
async def api_get_uptime():
  # TODO
  pass

# Messenger routes

# GET: https://api.slang.com/v1/[group]/[channel]/[message]
@app.get('/v1/{group}/{channel}/{message}')
async def api_get_message(group: int, channel: int, message: int):
  rsp = Response(None, 404)
  # Special group endpoint checks
  if group == -1: # Global group
    pass
  elif group == -2: # System messages
    pass
  elif group == -3: # Direct messages
    pass
  elif group == -4: # Group direct messages
    # User must be in [channel]
    pass

  return rsp

# GET: https://api.slang.com/v1/[group]/[channel]/messages
@app.get('/v1/{group}/{channel}/messages')
async def api_get_messages(group: int, channel: int, limit: int = 50):
  pass

# POST: https://api.slang.com/v1/[group]/[channel]/send
@app.post('/v1/{group}/{channel}/send')
async def api_send_message(group: int, channel: int, message: NewMessage):
  pass

# PATCH: https://api.slang.com/v1/[group]/[channel]/[message]/edit
# DELETE: https://api.slang.com/v1/[group]/[channel]/[message]/delete (2)

# -2 group endpoint used for system messages, such as security notifications and announcements; [channel] field not used
# All fields should be numbers. -3 group endpoint is used for messages, with [channel] as user id for user messages
# Group messages endpoint: -4, with [channel] being a real channel with group ID being -4

# Channel routes

# GET: https://api.slang.com/v1/[group]/channels
# GET: https://api.slang.com/v1/[group]/[channel]
# POST: https://api.slang.com/v1/[group]/newchannel
# PATCH: https://api.slang.com/v1/[group]/[channel]/edit
# DELETE: https://api.slang.com/v1/[group]/[channel]/delete

# Group routes

# GET: https://api.slang.com/v1/[group]
# POST: https://api.slang.com/v1/newgroup
# PATCH: https://api.slang.com/v1/[group]/edit
# DELETE: https://api.slang.com/v1/[group]/delete
# POST: https://api.slang.com/v1/[group]/join
# GET: https://api.slang.com/v1/[group]/invite

# Post routes

# GET: https://api.slang.com/v1/[group]/posts
# GET: https://api.slang.com/v1/[group]/posts/[post]
# POST: https://api.slang.com/v1/[group]/posts/create
# PATCH: https://api.slang.com/v1/[group]/posts/[post]/edit
# DELETE: https://api.slang.com/v1/[group]/posts/[post]/delete (2)
# POST: https://api.slang.com/v1/[group]/posts/[post]/like
# POST: https://api.slang.com/v1/[group]/posts/[post]/repost
# POST: https://api.slang.com/v1/[group]/posts/[post]/unlike

# User routes

# GET: https://api.slang.com/v1/users
# GET: https://api.slang.com/v1/users/[user]
# POST: https://api.slang.com/v1/users/new
# PATCH: https://api.slang.com/v1/users/[user]/edit (1)
# DELETE: https://api.slang.com/v1/users/[user]/delete (1)
# POST: https://api.slang.com/v1/users/[user]/friend
# POST: https://api.slang.com/v1/users/[user]/unfriend
# POST: https://api.slang.com/v1/users/[user]/block
# POST: https://api.slang.com/v1/users/[user]/unblock

# Role routes

# GET: https://api.slang.com/v1/[group]/roles
# GET: https://api.slang.com/v1/[group]/roles/[role]
# POST: https://api.slang.com/v1/[group]/roles/new
# PATCH: https://api.slang.com/v1/[group]/roles/[role]/edit
# DELETE: https://api.slang.com/v1/[group]/roles/[role]/delete
# POST: https://api.slang.com/v1/[group]/roles/[role]/adduser
# POST: https://api.slang.com/v1/[group]/roles/[role]/removeuser

# END: API routes

#1- Auth header must match [user]
#2- Auth header must either match high role with manage content (posts and messages will have separate perms), or match author/op field

# BEGIN: Websocket

# SOCKET: ws://api.slang.com/sock
@app.websocket("/sock")
async def socket(websocket: WebSocket):
  logger.info('WS: /sock')
  await websocket.accept()
  try:
    while True:
      connected_clients.append(websocket)
      await sockethandler.handle(websocket)
  except WebSocketDisconnect:
    # Go through all the connected clients and figure out which one's disconnected
    for sock in connected_clients:
      if sock.client_state == WebSocketState.DISCONNECTED: 
        connected_clients.remove(sock) # Does this work?
    logger.info('Client disconnected')

# END: Websocket

# Main function
def main():
  logger.debug("Slang Backend - Version 0.1.0")

  if not dbhandler.init(): # Don't allow the backend to continue if the database doesn't work at all, makes it useless
    logger.critical('Fatal error whilst initializing database, unrecoverable error. Terminating...')
    exit(1)

  logger.info("Initializing Slang backend...")

  logger.info("Starting HTTP listener...")
  uvicorn.run(app, host='127.0.0.1', port=REST_PORT, log_level='info', log_config=UVICORN_LOG)

def __test():
  logger.debug(start_time)
  pass