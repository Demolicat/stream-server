import typing

from dependency_injector.wiring import Provide, inject
from fastapi import status, Depends, APIRouter
from fastapi.responses import JSONResponse

from di.container import Container
from src.schemes.stream_state_response_schema import StreamStateResponse
from src.schemes.streaming_device import StreamingDevice, State
from src.services.receiver_service import ReceiverService

router = APIRouter()


@router.post(
    "/api/v1/stream",
    response_model=StreamStateResponse,
    responses={status.HTTP_404_NOT_FOUND: {"message": "Device not found"}},
)
@inject
async def change_stream_state(
    device: StreamingDevice,
    receiver_service: ReceiverService = Depends(Provide[Container.receiver_service]),
):
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


@router.post(
    "/api/v1/devices",
    responses={
        status.HTTP_201_CREATED: {"message": "Device added successfully"},
        status.HTTP_409_CONFLICT: {"message": "Device already exists"},
    },
)
@inject
async def add_device(
    device: StreamingDevice,
    receiver_service: ReceiverService = Depends(Provide[Container.receiver_service]),
):
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


@router.delete("/api/v1/devices")
@inject
async def remove_device(
    device: StreamingDevice,
    receiver_service: ReceiverService = Depends(Provide[Container.receiver_service]),
):
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


@router.get("/api/v1/devices", response_model=typing.List[StreamingDevice])
@inject
async def get_devices(
    receiver_service: ReceiverService = Depends(Provide[Container.receiver_service]),
):
    return list(receiver_service.devices.values())
