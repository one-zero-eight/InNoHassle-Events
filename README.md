# Events API in InNoHassle ecosystem

> Trust the system more than the memory

## Table of contents

- [Description](#description)
- [How to use](#how-to-use)
- [Project Structure](#project-structure)

## Description

This is the API for events in InNoHassle ecosystem. It is written in Python 3.11
using [FastAPI](https://fastapi.tiangolo.com/).

## How to use

1. Install dependencies with [poetry](https://python-poetry.org/docs/).
    ```bash
    poetry install
    ```
2. Setup environment variables in `.env.local` file.
    ```bash
    cp .env.example .env.local
    ```
3. Run the ASGI server using src/dev.py script
    ```bash
    poetry shell
    python -m src.dev
    ```
   OR using uvicorn directly
    ```bash
    poetry run uvicorn src.main:app --reload
    ```
   OR using 'Dev server' configuration in PyCharm.

## Project Structure

```
*
|   .env.example  # Example of environment variables for local development
|   (.env.local)  # Environment variables for local development
|   .gitignore
|   LICENSE
|   poetry.lock
|   pyproject.toml   # Poetry project configuration
|   README.md
|
+---.run
|       Dev server.run.xml    # PyCharm run configuration for local development
|       
\---src
    |   config.py       # Configuration module for the application (using ENV variables)
    |   dev.py          # Script for local development
    |   exceptions.py   # Custom exceptions
    |   main.py         # Represents ASGI application and initializes FastAPI application
    |
    +---app       # Represents FastAPI application with routers, dependencies, schemas, etc.
    |   |   dependencies.py      # Includes FastAPI dependencies for dependency injection
    |   |   routers.py           # Includes FastAPI routers for API endpoints
    |   |   schemas.py           # Includes Pydantic schemas for API request and response bodies
    |   |
    |   +---auth              # Module for authentication and authorization
    |   |   |   common.py
    |   |   |   dependencies.py
    |   |   |   dev.py
    |   |   |   innopolis.py
    |   |   \---jwt.py
    |   |
    |   +---event_groups      # Module for event groups
    |   |   |   routes.py        # Includes API endpoints for event group-related operations
    |   |   |   schemas.py       # Includes Pydantic schemas for event group-related operations
    |   +---users             # Module for users
    |   |   |   routes.py
    |   |   \---schemas.py       
    |
    +---repositories # Represents repositories layer for data access and manipulation
    |   |   
    |   +---event_groups
    |   |   |   abc.py  # Abstract base class for event group repository
    |   |   \---repository.py # SQLAlchemy repository for event group connected methods
    |   |           
    |   +---users
    |   |   |   abc.py  # Abstract base class for user repository
    |   |   |   json_repository.py  # JSON repository for predefined groups and users
    |   |   |   sql_repository.py   # SQLAlchemy repository for user connected methods
    |   |   |   (predefined_groups.json)  # Predefined groups data
    |   |   \---(innopolis_user_data.json) # Innopolis users data
    \---storages  # Represents data storage such as databases, third-party APIs, etc.
        |   
        \---sql   # SQLAlchemy storage
            |   storage.py    # SQLAlchemy session factory
            |
            \---models  # SQLAlchemy ORM models representing database tables

```