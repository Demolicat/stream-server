import threading
import typing

from src.schemes.streaming_device import StreamingDevice, State


class ReceiverService:
    def __init__(self):
        self.devices: typing.Dict[str, StreamingDevice] = {}

    def start_capture(self, device_id: str) -> typing.Tuple[str, State]:
        if device_id in self.devices:
            threading.Thread(target=self.devices.get(device_id).start_playing).start()
        else:
            raise KeyError()

        return (
            self.devices.get(device_id).get_address(),
            self.devices.get(device_id).state,
        )

    def stop_capture(self, device_id: str) -> typing.Tuple[str, State]:
        if device_id in self.devices:
            self.devices.get(device_id).stop_playing()
        else:
            raise KeyError()

        return (
            self.devices.get(device_id).get_address(),
            self.devices.get(device_id).state,
        )

    def add_device(self, device: StreamingDevice) -> bool:
        result = False
        if device.mac not in self.devices:
            self.devices[device.mac] = device
            result = True

        return result

    def remove_device(self, device: StreamingDevice):
        self.devices.pop(device.mac)
