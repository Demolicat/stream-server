from unittest import TestCase, mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from application import app
from src.schemes.streaming_device import StreamingDevice
from src.services.receiver_service import ReceiverService


@pytest.fixture
def setup(request):
    request.cls.client = TestClient(app)
    request.cls.payload = {
        "name": "SanMoshe",
        "mac": "48:45:20:28:4b:ea",
        "ip": "128.0.0.1",
        "state": "stop",
    }
    request.cls.base_url = "/api/v1"


@pytest.mark.usefixtures("setup")
class TestStreamAPI(TestCase):
    def test_change_stream_state_stops(self):
        service_mock = mock.Mock(ReceiverService)
        service_mock.stop_capture.return_value = "tcp://0.0.0.0:5555", "stop"

        app.container.receiver_service.override(service_mock)

        self.payload["state"] = "stop"
        response = self.client.post(f"{self.base_url}/stream", json=self.payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["mac"] == self.payload["mac"]
        assert response.json()["state"] == "stop"

    def test_change_stream_state_starts(self):
        service_mock = mock.Mock(ReceiverService)
        service_mock.start_capture.return_value = "tcp://0.0.0.0:5555", "play"

        app.container.receiver_service.override(service_mock)

        self.payload["state"] = "play"
        response = self.client.post(f"{self.base_url}/stream", json=self.payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["mac"] == self.payload["mac"]
        assert response.json()["state"] == "play"

    def test_add_device(self):
        service_mock = mock.Mock(ReceiverService)
        service_mock.add_device.return_value = True

        app.container.receiver_service.override(service_mock)

        response = self.client.post(f"{self.base_url}/devices", json=self.payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_device_already_exists(self):
        service_mock = mock.Mock(ReceiverService)
        service_mock.add_device.return_value = False

        app.container.receiver_service.override(service_mock)

        response = self.client.post(f"{self.base_url}/devices", json=self.payload)
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_remove_device(self):
        service_mock = mock.Mock(ReceiverService)

        app.container.receiver_service.override(service_mock)
        response = self.client.delete(f"{self.base_url}/devices", json=self.payload)
        assert response.status_code == status.HTTP_200_OK

    def test_remove_device_not_exists(self):
        service_mock = mock.Mock(ReceiverService)
        service_mock.remove_device.side_effect = KeyError

        app.container.receiver_service.override(service_mock)
        response = self.client.delete(f"{self.base_url}/devices", json=self.payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_devices(self):
        expected = list(
            (
                {
                    "name": "SanMoshe",
                    "mac": "48:45:20:28:4b:ea",
                    "ip": "128.0.0.1",
                    "state": "stop",
                },
                {
                    "name": "SanMoshe",
                    "mac": "48:45:20:28:4b:ee",
                    "ip": "128.0.0.1",
                    "state": "stop",
                },
                {
                    "name": "SanMoshe",
                    "mac": "48:45:20:28:4b:ec",
                    "ip": "128.0.0.1",
                    "state": "stop",
                },
            )
        )

        devices = dict(
            (device["mac"], StreamingDevice(**device)) for device in expected
        )

        service_mock = mock.Mock(ReceiverService)
        service_mock.devices = devices

        app.container.receiver_service.override(service_mock)

        response = self.client.get(f"{self.base_url}/devices")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected

    def test_device_not_found_when_change_stream_state_without_register(self):
        service_mock = mock.Mock(ReceiverService)
        service_mock.start_capture.side_effect = KeyError
        service_mock.stop_capture.side_effect = KeyError

        app.container.receiver_service.override(service_mock)
        response = self.client.post(f"{self.base_url}/stream", json=self.payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "Device not found"}
