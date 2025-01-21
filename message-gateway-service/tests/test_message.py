import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import respx
import httpx
import sys
sys.path.append("..")
from app import app

client = TestClient(app)

DEVICE_SERVICE_URL = "http://device-service:8001"
READING_SERVICE_URL = "http://reading-service:8002"


@pytest.fixture
def registration_message():
    return {
        "deviceId": "device123",
        "type": "registration",
        "data": {"username": "test_user"}
    }


@pytest.fixture
def reading_message():
    return {
        "deviceId": "device123",
        "type": "reading",
        "data": {"reading": 42.5}
    }


@respx.mock
def test_handle_registration_message(registration_message):
    # Mock device-service registration endpoint
    respx.put(f"{DEVICE_SERVICE_URL}/devices/device123").mock(
        return_value=httpx.Response(200)
    )

    response = client.post("/messages", json=registration_message)

    assert response.status_code == 200
    assert response.json() == {"message": "Registration processed successfully"}



@respx.mock
def test_handle_reading_message(reading_message):
    # Mock fetching username from device-service
    respx.get(f"{DEVICE_SERVICE_URL}/devices/device123/username").mock(
        return_value=httpx.Response(200, json={"username": "test_user"})
    )

    # Mock posting reading to reading-service
    respx.post(f"{READING_SERVICE_URL}/readings").mock(
        return_value=httpx.Response(200)
    )

    response = client.post("/messages", json=reading_message)

    assert response.status_code == 200
    assert response.json() == {"message": "Reading processed successfully"}


@respx.mock
def test_handle_invalid_message_type():
    invalid_message = {
        "deviceId": "device123",
        "type": "invalid_type",
        "data": {}
    }

    response = client.post("/messages", json=invalid_message)

    assert response.status_code == 500
    assert response.json() == {"detail": "400: Invalid message type"}