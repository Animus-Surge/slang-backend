"""
Websocket server for Slang

Changelog:
Surge: Initial commit
"""

import asyncio
from websockets.server import serve
import json

# TODO: message handling

async def handler(websocket):
  async for message in websocket:
    data = json.loads(message)
    print(data)
    await websocket.send("Hello World!")

async def init():
  async with serve(handler, "localhost", 8765):
    await asyncio.Future()  # run forever

# TODO: Add SSL support, add authentication, add database support
