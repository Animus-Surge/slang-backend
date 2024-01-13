from fastapi.websockets import WebSocket
from loguru import logger

import json

def generate_response(type: str, data: any = None):
  return json.dumps({
    'type': type,
    'data': data
  })
  pass

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
    # TODO
    logger.debug(data['data'])
    await sock.send_text(generate_response('msg', {'code': 418, 'message': 'Acknowledged, unimplemented'}))
  else:
    pass

  pass