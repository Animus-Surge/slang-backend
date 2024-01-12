from fastapi.websockets import WebSocket
from loguru import logger

import json

def generate_error(message: str, http_code: int):
  return {
    'err':message,
    'http':http_code
  }

async def handle(sock: WebSocket):
  data = json.loads(await sock.receive_text())

  if 'type' not in data:
    await sock.send_text(json.dumps(generate_error("Missing required field: 'type'", 400)))
    return

  dt = data['type']

  if 'data' not in data:
    await sock.send_text(json.dumps(generate_error("Missing required field: 'data'", 400)))

  if dt == 'ping':
    await sock.send_text('Pong!')
  elif dt == 'new_msg':
    # TODO
    logger.debug(data['data'])
    sock.send_text('202 ACCEPTED')
  
  else:
    await sock.send_text(json.dumps(generate_error(f"Invalid type: {dt}", 400)))

  pass