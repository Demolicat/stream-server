from unittest import mock

import pytest

from src.schemes.streaming_device import StreamingDevice, State
from src.services.receiver_service import ReceiverService


def test_stop_capture_called_once_for_existing_device():
    service = ReceiverService()
    device_id = mock.Mock(str)
    device = mock.Mock(StreamingDevice)
    device.state = State.PLAYING
    service.devices = {device_id: device}

    service.stop_capture(device_id)

    device.stop_playing.assert_called_once()


def test_stop_capture_raise_key_error():
    service = ReceiverService()

    with pytest.raises(KeyError):
        service.stop_capture(mock.Mock(str))


def test_stop_reuturn_address_and_state():
    expected_address = "tcp://127.8.0.1:5555"

    service = ReceiverService()
    device_id = mock.Mock(str)
    device = mock.Mock(StreamingDevice)
    device.state = State.PLAYING
    device.get_address.return_value = expected_address
    service.devices = {device_id: device}

    address, state = service.stop_capture(device_id)

    assert address == expected_address
    assert state == State.PLAYING


def test_add_device_already_exists():
    device = mock.Mock(StreamingDevice)
    device.mac = mock.Mock(str)
    service = ReceiverService()
    service.devices = {device.mac: device}

    result = service.add_device(device)

    assert not result


def test_add_device():
    service = ReceiverService()
    device = mock.Mock(StreamingDevice)
    device.mac = mock.Mock(str)
    result = service.add_device(device)

    assert result


def test_remove_device():
    service = ReceiverService()
    device = mock.Mock(StreamingDevice)
    device.mac = mock.Mock(str)
    service.devices = {device.mac: device}

    assert service.devices == {device.mac: device}

    service.remove_device(device)

    assert service.devices == {}


def test_remove_device_doesnt_exists():
    service = ReceiverService()
    device = mock.Mock(StreamingDevice)
    device.mac = mock.Mock(str)

    assert service.devices == {}

    with pytest.raises(KeyError):
        service.remove_device(device)
