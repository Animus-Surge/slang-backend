# Slang Backend Dockerfile
#   Author: Surge
#   Version: 0.1.1

# Initialization
FROM python:3.x
WORKDIR /app

# Install poetry, copy deps, and install
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock /app/
RUN poetry install

# Copy files
COPY . /app/

# Expose ports for websocket and REST api
EXPOSE 8000 8765
#TODO: set ports as environment variables

# Run
RUN poetry run ./backend.py
