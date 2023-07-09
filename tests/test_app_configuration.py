from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest


@pytest.mark.asyncio
async def test_startup():
    from src.main import app

    assert isinstance(app, FastAPI)

    with TestClient(app):
        ...
