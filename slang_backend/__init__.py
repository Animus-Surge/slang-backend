"""
Main module

Changelog:
Surge: Initial commit
"""

from . import dbhandler, slang_socket, apihandler
from loguru import logger
import asyncio

# Main function
def main():
  logger.info("Initializing Slang backend...")
  dbhandler.init()
  logger.info("Slang backend initialized.")

