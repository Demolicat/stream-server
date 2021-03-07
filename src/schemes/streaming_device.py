import ipaddress
import re
from typing import Optional

from pydantic import BaseModel, validator, Field
from enum import Enum
import cv2 as cv
import imagezmq
from utils import get_local_ip


class State(Enum):
    PLAYING = "play"
    STOPPED = "stop"


class StreamingDevice(BaseModel):
    name: str
    mac: str = Field(example="00-D0-56-F2-B5-12")
    ip: ipaddress.IPv4Address
    state: Optional[State]

    @validator("mac")
    def mac_match_global_standard(cls, mac):
        if not re.match(
            "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()
        ):
            raise ValueError("Mac address must match the IEEE EUI-48 standard")

        return mac

    def start_playing(self):
        self.state = State.PLAYING
        image_hub = imagezmq.ImageHub(open_port=self.get_address())

        while self.state == State.PLAYING:
            rpi_name, image = image_hub.recv_image()
            cv.imshow(rpi_name, image)

            cv.waitKey(1)
            image_hub.send_reply(b"OK")
        cv.destroyAllWindows()
        image_hub.close()

    def stop_playing(self):
        self.state = State.STOPPED

    def get_address(self):
        return f"tcp://{get_local_ip()}:5555"
