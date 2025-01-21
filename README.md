
# Description

This project implements a microservice-based architecture using FastAPI to manage devices and readings. The system consists of two main services:

1. **Device Service**: Handles device registration and username retrieval by ID.
2. **Message Gateway Service**: Processes messages of type `registration` and `reading`.

## Features
- **Device Service**:
  - Register or update a device's username using its ID.
  `**PUT /devices/:deviceId**`
  - Retrieve the username associated with a device.
  `**GET /devices/:deviceId/username**`


- **Message Handling Service**:
    ```POST /messages**

    - **Request Body**:
        json
        {
            "deviceId": "my-device",
            "type": "registration",
            "data": {
                "username": "my-username"
            }
        }
    ```
  - Process `registration` messages to `Device Service`  register/update a device.
  - Process `reading` messages to `POST /readings` to store readings, associated with its username from `Device Service`.

## Installation and Setup

### Prerequisites
- Python 3.9 or higher
- FastAPI
- SQLite (for database storage)
- Docker
  
### Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
docker-compose up --build
```