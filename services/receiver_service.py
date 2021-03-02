import typing

from schemes.streaming_device import StreamingDevice


class ReceiverService:
    def __init__(self):
        self.devices: typing.Dict[str, StreamingDevice] = {}

    # TODO throw exception if device doesn't exists
    def start_capture(self, device_id: str):
        if device_id in self.devices:
            self.devices.get(device_id).start_playing()

    def stop_capture(self, device_id: str):
        if device_id in self.devices:
            self.devices.get(device_id).stop_playing()

    def add_device(self, device: StreamingDevice):
        self.devices[device.mac] = device

    def remove_device(self, device: StreamingDevice):
        self.devices.pop(device.mac)
