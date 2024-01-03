"""
Main module, handles REST api

Changelog:
Surge: Initial commit
Surge: Move REST api to this file
"""

from . import dbhandler, slang_socket
from loguru import logger
from fastapi import FastAPI, Response
import asyncio
import uvicorn

# Config variables
REST_PORT = 8000

app = FastAPI()

@app.get("/")
async def root():
  resp = Response(status_code=204)
  return resp

# BEGIN: API routes

# Messenger routes

# GET: https://api.slang.com/v1/messages
@app.get("/v1/messages")
async def api_get_messages(group: int = -1, channel: int = -1):
  # TODO: Add authentication
  resp = Response()

  # If either group or channel is -1, return 400
  if group == -1 or channel == -1:
    resp.status_code = 400
    resp.content = "Invalid group or channel ID"
  else:
    
    pass

  return resp

# POST: https://api.slang.com/v1/messages/create
@app.post("/v1/messages/send")
async def api_send_message(group: int = -1, channel: int = -1, user: int = -1, content: str = ""):
  pass



# END: API routes

# Main function
async def main():
  logger.info("Initializing Slang backend...")
  dbhandler.init()
  config = uvicorn.Config(app, log_level="info")
  server = uvicorn.Server(config)
  logger.info("Slang backend initialized.")
  await server.serve()

