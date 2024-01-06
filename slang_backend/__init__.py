"""
Main module, handles websocket and REST API

Changelog:
Surge: Initial commit
Surge: Move REST api to this file
Surge - 01/04/24: Move websocket handler to this file
"""

from . import dbhandler, slang_socket
from loguru import logger
from fastapi import FastAPI, Response, WebSocket
from concurrent.futures import ThreadPoolExecutor
from websockets import serve
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware # NOTE: No HTTPS support as of 1/4/24
import asyncio, uvicorn, multiprocessing, signal

# Config variables
REST_PORT = 8000
SOCKET_PORT = 8765

UVICORN_LOG = "./uvicorn_log.ini" # TODO: make the logs look consistent

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
  resp = Response(status_code=418)

  # If either group or channel is -1, return 400
  if group == -1 or channel == -1:
    resp.status_code = 400
    resp.content = "Invalid group or channel ID"
  else:
    # TODO
    pass

  return resp

# POST: https://api.slang.com/v1/messages/create
@app.post("/v1/messages/send")
async def api_send_message(group: int = -1, channel: int = -1, user: int = -1, content: str = ""):
  return Response(status_code=418)

# END: API routes
# BEGIN: Websocket

@app.websocket("/sock")
async def socket(websocket: WebSocket):
  pass

# END: Websocket

def init_rest():
  logger.info("Starting HTTP listener...")
  uvicorn.run(app, host='127.0.0.1', port=REST_PORT, log_level='info')

def init_socket():
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)

  ws_server = serve(socket, '127.0.0.1', SOCKET_PORT)

  logger.info('Backend initialized')

  try:
    loop.run_until_complete(ws_server)
  finally:
    loop.close()

# Main function
def main():
  logger.debug("Slang Backend - Version 0.1.0")
  logger.info("Initializing Slang backend...")

  rest_process = multiprocessing.Process(target=init_rest)
  sock_process = multiprocessing.Process(target=init_socket)

  try:
    rest_process.start()
    sock_process.start()

    rest_process.join()
    sock_process.join()
  except KeyboardInterrupt:
    pass # ignore sigint