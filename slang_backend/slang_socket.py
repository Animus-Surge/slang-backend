"""
Websocket server for Slang

Changelog:
Surge: Initial commit
"""

import asyncio
from websockets.server import serve
from loguru import logger
import json

# TODO: message handling, async handling

PORT = 3100

async def handler(websocket):
  async for message in websocket:
    logger.debug(f"Received message: {message}")
    # data = json.loads(message)
    # print(data)
    await websocket.send("Hello World!")

async def init():
  logger.info("Initializing Slang websocket server...")
  async with serve(handler, "localhost", PORT):
    await asyncio.Future()  # run forever - TODO


# TODO: Add SSL support, add authentication, add database support

"""
Websocket message format (Goes in both directions):

{
  "type": "message", // Type of message, one of: message, group, user, moderation, admin, ack
  "timestamp": <timestamp:timestamp/string/integer>, // Timestamp of message
  "sender": <userid:integer>, // Sender of message, -1 if server
  "action": "create", // Action of message, one of: create, delete, edit, get, join, leave
  "data": {
    // Message data
    "id": <messageid:integer>, // ID of message, -1 if not applicable (i.e. if creating)
    "content": <content:string>, // Content of message
    "oldContent": <oldcontent:string>, // Old content of message, blank if not applicable (i.e. if creating)
    "group": <groupid:string>, // Group of message, prepended with 'user:' if direct message, or 'gdm:' if group direct message
    "channel": <channelid:integer>, // Channel of message, -1 if direct message or group direct message
    "user": <userid:integer>, // Author of message
    "attachments": <attachments:array>, // Attachments of message, blank if none, each is url

    // Group data
    //  Create action
    "name": <name:string>, // Name of group
    "owner": <ownerid:integer>, // Owner of group

    //  Get action
    "id": <groupid:integer>, // ID of group

    //  Delete action
    "id": <groupid:integer>, // ID of group

    //  Edit action
    "id": <groupid:integer>, // ID of group
    "name": <name:string>, // New name of group, blank if not updating
    "owner": <ownerid:integer>, // New owner of group, -1 if not updating
    "image": <image:string>, // New profile image of group, blank if not updating
    "banner": <banner:string>, // New banner image of group, blank if not updating

    //TODO

    // User data

    //TODO

    // Moderation data

    //TODO

    // Admin data

    //TODO

    // Ack data
    "errcode": <errcode:integer>, // Error code, 0 if no error; see below for error codes
    "errmsg": <errmsg:string> // Error message, 'OK' if no error
  }
}

Error codes:
-1: Serverside error (500)
0: No error (200)
1: Invalid message data, see errmsg field (400)
2: Invalid message type, see errmsg field (400)
3: Invalid action, see errm sg field (400)
4: Insufficient permissions (403)
5. Authentication error (401)
6. Invalid group or channel (404)

"""
