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
import asyncio
"""
TODO BOARD:

- Socket handling
- Database schema (wip)
- Administration system
- Test database
...
"""

if __name__ == "__main__":
  slang_backend.main()