from enum import Enum

from pydantic import BaseModel

from src.schemes.streaming_device import State


class StreamStateResponse(BaseModel):
    mac: str
    address: str
    state: State
