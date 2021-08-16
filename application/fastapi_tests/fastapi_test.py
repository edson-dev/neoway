from fastapi.testclient import TestClient

import sys


sys.path.append("../fastapi")
from main import app
import nest_asyncio
nest_asyncio.apply()

client = TestClient(app)


async def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

async def test_read_table():
    response = client.get("/api/table/base_teste")
    assert response.status_code == 200