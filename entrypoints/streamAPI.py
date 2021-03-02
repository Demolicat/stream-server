import typing
import uvicorn
from fastapi import FastAPI, Depends, BackgroundTasks
from schemes.streaming_device import StreamingDevice
from schemes.user import User
from schemes.userCredentials import UserCredentials
from services.receiver_service import ReceiverService

app = FastAPI()

receiver_service = ReceiverService()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/v1/login", response_model=User)
async def login(credentials: UserCredentials):
    # TODO add JWT authentication
    # TODO db integration
    if credentials.username == "san" and credentials.password == 5:
        return {"message: Good"}
    return {"message": "Failed"}


@app.post("/api/v1/register")
async def register(req: User):
    # TODO add JWT authentication
    # TODO db integration
    if req.name == "san" and req.age == '5':
        return {"message": "Success"}
    return {"message": "Failed"}


@app.post("/api/v1/stream")
async def change_stream_state(device: StreamingDevice):
    # TODO return http status code 404 if device doens't exists
    receiver_service.start_capture(device.mac)
    return {"message": "Success"}


@app.post("/api/v1/devices")
async def add_device(device: StreamingDevice):
    receiver_service.add_device(device)
    return {"message": "Success"}


@app.delete("/api/v1/devices")
async def remove_device(device: StreamingDevice):
    receiver_service.remove_device(device)
    return {"message": "Success"}


@app.get("/api/v1/devices", response_model=typing.List[StreamingDevice])
async def get_devices():
    return list(receiver_service.devices.values())


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
