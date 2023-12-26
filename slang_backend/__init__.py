"""
Main module

Changelog:
Surge: Initial commit
"""

from . import dbhandler, slang_socket

# Main function
def main():
  dbhandler.init()
  slang_socket.init()

