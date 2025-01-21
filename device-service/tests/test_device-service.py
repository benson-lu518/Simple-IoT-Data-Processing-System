import pytest
from httpx import AsyncClient
import sys
sys.path.append("..")
from app import app  # Make sure the app is imported correctly
import sqlite3

# Mock SQLite fixture for testing
@pytest.fixture(scope="function")
def mock_db():
    # Create an in-memory SQLite database for each test (mocked database)
    conn = sqlite3.connect(":memory:")
    conn.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                deviceId TEXT PRIMARY KEY,
                username TEXT NOT NULL
            )
        """)

    yield conn  # Yield the connection to the test

    conn.close()  # Close the connection after the test is finished


@pytest.mark.asyncio
async def test_update_device():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Test PUT /devices/:deviceId with a new device
        response = await client.put("/devices/test-device", json={"username": "test-user"})
        assert response.status_code == 200
        assert response.json() == {"message": "Device updated successfully"}

        # Test GET /devices/:deviceId/username to verify the update
        response = await client.get("/devices/test-device/username")
        assert response.status_code == 200
        assert response.json() == {"username": "test-user"}

@pytest.mark.asyncio
async def test_get_nonexistent_device():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Test GET /devices/:deviceId/username for a nonexistent device
        response = await client.get("/devices/nonexistent/username")
        assert response.status_code == 500
        assert response.json() == {"detail": "404: Device not found"}

@pytest.mark.asyncio
async def test_update_device_wrong_type():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Test PUT /devices/:deviceId with a new device
        response = await client.put("/devices/test1-device", json={"username": 123})
        assert response.status_code == 422
        