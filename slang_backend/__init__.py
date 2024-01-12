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
# TODO: import models
from loguru import logger
from fastapi import FastAPI, Response, WebSocket
from starlette.websockets import WebSocketDisconnect
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware # NOTE: No HTTPS support as of 1/4/24
import uvicorn

from . import sockethandler

# Config variables
REST_PORT = 8000
SOCKET_PORT = 8765

UVICORN_LOG = "./log_config.ini" # TODO: make the logs look consistent

app = FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)

@app.get("/")
async def root():
  resp = Response(content="unimplemented", status_code=418)
  return resp

# BEGIN: API routes

# Messenger routes

# GET: https://api.slang.com/v1/messages
@app.get("/v1/messages")
async def api_get_messages(group: int = -1, channel: int = -1):
  # TODO: Add authentication
  logger.info('GET: /v1/messages group:%s;channel:%s;', (group, channel))

  resp = Response(status_code=418)

  # If either group or channel is -1, return 400
  if group == -1 or channel == -1:
    logger.error('400 - group or channel argument = -1')
    resp.status_code = 400
    resp.content = "Invalid group or channel ID"
  else:
    _content = dbhandler.get_messages(1,1) # TESTING: bogus data
    pass

  return resp

# POST: https://api.slang.com/v1/messages/create
@app.post("/v1/messages/send")
async def api_send_message(group: int = -1, channel: int = -1, user: int = -1, content: str = ""):
  # TODO: send update to all connected sockets

  dbhandler.create_message(1, 1, 1, 'Hello, World!') # TESTING: bogus data

  return Response(status_code=418)

# END: API routes
# BEGIN: Websocket

# SOCKET: ws://api.slang.com/sock
@app.websocket("/sock")
async def socket(websocket: WebSocket):
  logger.info('WS: /sock')
  await websocket.accept()
  try:
    while True:
      await sockethandler.handle(websocket)
  except WebSocketDisconnect:
    logger.info('Client disconnected')
# END: Websocket

# Main function
def main():
  logger.debug("Slang Backend - Version 0.1.0")

  if not dbhandler.init():
    logger.critical('Fatal error whilst initializing database, unrecoverable error. Terminating...')
    exit(1)

  logger.info("Initializing Slang backend...")

  logger.info("Starting HTTP listener...")
  uvicorn.run(app, host='127.0.0.1', port=REST_PORT, log_level='info', log_config=UVICORN_LOG)