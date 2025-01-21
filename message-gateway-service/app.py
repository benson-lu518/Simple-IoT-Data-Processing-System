from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

DEVICE_SERVICE_URL = "http://device-service:8001"
# DEVICE_SERVICE_URL = "http://localhost:8001"
READING_SERVICE_URL = "http://reading-service:8002"

class RegistrationData(BaseModel):
    username: str

class ReadingData(BaseModel):
    reading: float

class Message(BaseModel):
    deviceId: str
    type: str
    data: dict

@app.post("/messages")
async def handle_message(message: Message):
    try:
        device_id = message.deviceId
        if message.type == "registration":
            # Parse request data to registration data 
            registration_data = RegistrationData(**message.data)
            # Forward to device-service
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"{DEVICE_SERVICE_URL}/devices/{device_id}",
                    json=registration_data.model_dump()
                )
                response.raise_for_status()
            return {"message": "Registration processed successfully"}
        elif message.type == "reading":
            # Fetch username from device-service
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{DEVICE_SERVICE_URL}/devices/{device_id}/username")
                response.raise_for_status()
                username = response.json()["username"]
            # Forward to reading-service
            reading_data = ReadingData(**message.data)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{READING_SERVICE_URL}/readings",
                    json={
                        "deviceId": device_id,
                        "username": username,
                        "reading": reading_data.reading
                    }
                )
                response.raise_for_status()
            return {"message": "Reading processed successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid message type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
