from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from init_database import get_connection, initialize_db
app = FastAPI()

# Initialize the database
initialize_db()

class Device(BaseModel):
    username: str # for incoming requests

@app.put("/devices/{deviceId}")
async def update_device(deviceId: str, device: Device):
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO devices (deviceId, username) 
                VALUES (?, ?) 
                ON CONFLICT(deviceId) DO UPDATE 
                SET username = excluded.username
            """, (deviceId, device.username))
        return {"message": "Device updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/devices/{deviceId}/username")
async def get_username(deviceId: str):
    try:
        with get_connection() as conn:
            result = conn.execute(
                "SELECT username FROM devices WHERE deviceId = ?", 
                (deviceId,)).fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Device not found")
            return {"username": result["username"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

