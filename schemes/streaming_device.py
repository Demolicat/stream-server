import ipaddress
import re
from typing import Optional

from pydantic import BaseModel, validator, Field
from enum import Enum
import cv2 as cv


class State(Enum):
    PLAYING = "play"
    STOPPED = "stop"


class StreamingDevice(BaseModel):
    name: str
    mac: str = Field(example='00-D0-56-F2-B5-12')
    ip: ipaddress.IPv4Address
    stream_address: str
    state: Optional[State]

    @validator('mac')
    def mac_match_global_standard(cls, mac):
        if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
            raise ValueError('Mac address must match the IEEE EUI-48 standard')

        return mac

    def start_playing(self):
        cap = cv.VideoCapture(self.stream_address)
        while self.state == State.PLAYING:
            # Capture frame-by-frame
            ret, frame = cap.read()

            cv.imshow('frame', frame)
        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()

    def stop_playing(self):
        self.state = State.STOPPED
