"""
Slang REST API handler

Author: Surge
Version: 0.1.0
License: Apache 2.0

Changelog:
Surge: Begin work on handlers and postgres implementation
"""

from loguru import logger
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root(uid: str = None):
  logger.info("GET: / from {client}", client=uid)
  return {"message": "Hello World!"}

# async def init():
#   logger.info("Initializing Slang REST API...")
#   config = uvicorn.Config(app, port=3101, log_level="info")
#   server = uvicorn.Server(config)
#   await server.serve()
#   pass