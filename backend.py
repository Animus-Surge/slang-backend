#!/usr/bin/env python3
"""
Slang - An open source social media platform
Backend module

Author: Surge
Version: 0.1.0
License: Apache 2.0
"""

import slang_backend
from loguru import logger

"""
TODO BOARD:

- Socket handling
- Database schema (wip)
- Administration system
- Test database
...
"""

if __name__ == "__main__":
  try:
    slang_backend.main()
  except KeyboardInterrupt:
    logger.info("Shutting down...")
    exit(0)