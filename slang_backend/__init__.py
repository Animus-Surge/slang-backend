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
from .models import *
from loguru import logger
from fastapi import FastAPI, Response, WebSocket
from starlette.websockets import WebSocketDisconnect, WebSocketState
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware # NOTE: No HTTPS support as of 1/4/24
import uvicorn

from . import sockethandler

# Config variables
REST_PORT = 8000
SOCKET_PORT = 8765

UVICORN_LOG = "./log_config.ini" # TODO: make the logs look consistent

app = FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)

connected_clients = []

@app.get("/")
async def root():
  resp = Response(content="unimplemented", status_code=418)
  return resp

# BEGIN: API routes

# Messenger routes

# GET: https://api.slang.com/v1/[group]/[channel]/[message]
# GET: https://api.slang.com/v1/[group]/[channel]/messages
@app.post('/v1/{group}/{channel}/messages')
async def api_get_messages(group: int, channel: int, limit: int = 50):
  pass

# POST: https://api.slang.com/v1/[group]/[channel]/send
@app.post('/v1/{group}/{channel}/send')
async def api_send_message(group: int, channel: int, message: NewMessage):

  pass

# PATCH: https://api.slang.com/v1/[group]/[channel]/[message]/edit
# DELETE: https://api.slang.com/v1/[group]/[channel]/[message]/delete

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

# Post routes

# GET: https://api.slang.com/v1/[group]/posts
# GET: https://api.slang.com/v1/[group]/posts/[post]
# POST: https://api.slang.com/v1/[group]/posts/create
# PATCH: https://api.slang.com/v1/[group]/posts/[post]/edit
# DELETE: https://api.slang.com/v1/[group]/posts/[post]/delete

# User routes

# GET: https://api.slang.com/v1/users
# GET: https://api.slang.com/v1/users/[user]
# POST: https://api.slang.com/v1/users/new
# PATCH: https://api.slang.com/v1/users/[user]/edit - Auth header MUST match [user] for this to work
# DELETE: https://api.slang.com/v1/users/[user]/delete - Auth header MUST match [user] for this to work

# Role routes

# GET: https://api.slang.com/v1/[group]/roles
# GET: https://api.slang.com/v1/[group]/roles/[role]
# POST: https://api.slang.com/v1/[group]/roles/new
# PATCH: https://api.slang.com/v1/[group]/roles/[role]/edit
# DELETE: https://api.slang.com/v1/[group]/roles/[role]/delete

# END: API routes

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