import typing

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.schemes.stream_state_response_schema import StreamStateResponse
from src.schemes.streaming_device import StreamingDevice, State
from src.services.receiver_service import ReceiverService

app = FastAPI()
receiver_service = ReceiverService()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post(
    "/api/v1/stream",
    response_model=StreamStateResponse,
    responses={status.HTTP_404_NOT_FOUND: {"message": "Device not found"}},
)
async def change_stream_state(device: StreamingDevice):
    response = StreamStateResponse(mac=device.mac, address="", state=State.STOPPED)

    try:
        if device.state == State.PLAYING:
            response.address, response.state = receiver_service.start_capture(
                device.mac
            )
        else:
            response.address, response.state = receiver_service.stop_capture(device.mac)
    except KeyError:
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Device not found"},
        )
    return response


@app.post(
    "/api/v1/devices",
    responses={
        status.HTTP_201_CREATED: {"message": "Device added successfully"},
        status.HTTP_409_CONFLICT: {"message": "Device already exists"},
    },
)
async def add_device(device: StreamingDevice):
    if receiver_service.add_device(device):
        response = JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Device added successfully"},
        )
    else:
        response = JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "Device already exists"},
        )

    return response


@app.delete("/api/v1/devices")
async def remove_device(device: StreamingDevice):
    try:
        receiver_service.remove_device(device)
    except KeyError:
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Device not found"},
        )
    else:
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Device deleted"}
        )

    return response


@app.get("/api/v1/devices", response_model=typing.List[StreamingDevice])
async def get_devices():
    return list(receiver_service.devices.values())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
