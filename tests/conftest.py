import asyncio

import pytest
import uvloop
from aiohttp import ClientSession, TCPConnector

from mofh import Client, AsyncClient

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
def client():
    """
    Create a client for the tests.
    """
    with Client(username="example", password="password") as conn:
        yield conn


@pytest.fixture(scope="session")
async def async_client(event_loop):
    """
    Create an async client for the tests.
    """
    async with AsyncClient(
        username="example",
        password="password",
        session=ClientSession(connector=TCPConnector(), loop=event_loop),
    ) as conn:
        yield conn


@pytest.fixture(scope="session")
def event_loop():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
