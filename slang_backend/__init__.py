"""
Main module, handles REST api

Changelog:
Surge: Initial commit
Surge: Move REST api to this file
"""

from . import dbhandler, slang_socket, apihandler
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
@app.get("/v1/messages")
async def api_get_messages(): # api.slang.com/v1/messages?group=1&channel=1 - body contains json with additional parameters, or {} if none
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

