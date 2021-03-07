from unittest import TestCase
from fastapi.testclient import TestClient
from fastapi import status
from src.entrypoints.streamAPI import app
import pytest

from src.schemes.streaming_device import StreamingDevice


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
        self.client.post(f"{self.base_url}/devices", json=self.payload)
        response = self.client.post(f"{self.base_url}/stream", json=self.payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["mac"] == self.payload["mac"]
        assert response.json()["state"] == "stop"

    def test_change_stream_state_starts(self):
        self.client.post(f"{self.base_url}/devices", json=self.payload)
        self.payload["state"] = "play"
        response = self.client.post(f"{self.base_url}/stream", json=self.payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["mac"] == self.payload["mac"]
        assert response.json()["state"] == "play"

    def test_add_device(self):
        response = self.client.post(f"{self.base_url}/devices", json=self.payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_device_already_exists(self):
        self.client.post(f"{self.base_url}/devices", json=self.payload)
        response = self.client.post(f"{self.base_url}/devices", json=self.payload)
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_remove_device(self):
        self.client.post(f"{self.base_url}/devices", json=self.payload)
        response = self.client.delete(f"{self.base_url}/devices", json=self.payload)
        assert response.status_code == status.HTTP_200_OK

    def test_remove_device_not_exists(self):
        self.client.delete(f"{self.base_url}/devices", json=self.payload)
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
        self.client.post(f"{self.base_url}/devices", json=self.payload)

        self.payload["mac"] = "48:45:20:28:4b:ee"
        self.client.post(f"{self.base_url}/devices", json=self.payload)

        self.payload["mac"] = "48:45:20:28:4b:ec"
        self.client.post(f"{self.base_url}/devices", json=self.payload)
        response = self.client.get(f"{self.base_url}/devices")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected

    def test_device_not_found_when_change_stream_state_without_register(self):
        self.client.delete(f"{self.base_url}/devices", json=self.payload)
        response = self.client.post(f"{self.base_url}/stream", json=self.payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "Device not found"}
