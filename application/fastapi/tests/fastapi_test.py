from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


async def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

async def test_read_table():
    response = client.get("/api/table/base_teste")
    assert response.status_code == 200