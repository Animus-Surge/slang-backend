from fastapi.websockets import WebSocket
from loguru import logger

from .models import *

import json

def generate_response(type: str, data: any = None):
  return json.dumps({
    'type': type,
    'data': data
  })
  pass

def generate_ack(message: str):
  return generate_response('ack', message)

def generate_message(code: int, message: any):
  return generate_response('msg', {'code':code, 'message': message})

def generate_error(message: str, http_code: int):
  return generate_response('error', {'code':http_code, 'message':message})

def generate_ping():
  return generate_response('pong')

async def handle(sock: WebSocket):
  data = json.loads(await sock.receive_text())

  logger.info('Received data: ' + json.dumps(data))

  if 'type' not in data:
    generate_error('Missing required field "type"', 400)
    return

  dt = data['type']

  if 'data' not in data:
    await sock.send_text(generate_error('Missing required field "data"', 400))
    return

  if dt == 'ping':
    await sock.send_text(generate_ping())
  elif dt == 'new_msg':
    value = data['data']
    value = NewMessage.model_validate(value)
    logger.debug(value)
    # TODO
    await sock.send_text(generate_ack('Unimplemented'))
  else:
    pass

  pass