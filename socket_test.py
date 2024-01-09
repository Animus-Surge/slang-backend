#!/usr/bin/env python3

from websockets.sync.client import connect
from loguru import logger

def main():
  with connect('ws://localhost:8000/sock') as socket:
    try:
      while True:
        message = input("> ")
        socket.send(message)

        incoming = socket.recv()
        logger.debug(incoming)
    except KeyboardInterrupt:
      logger.info('Shutting down...')
      socket.close()

if __name__=='__main__':
  main()