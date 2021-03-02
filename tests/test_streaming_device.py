import logging
from unittest import TestCase
import pytest
from pydantic import ValidationError

from schemes.streaming_device import StreamingDevice


class TestStreamingDevice(TestCase):

    def test_mac_match_global_standard(self):
        try:
            StreamingDevice(name='RPILEFT', mac='00-D0-56-F2-B5-12', ip='128.0.0.1', streamAddress='')
        except ValidationError as e:
            self.fail(e)

    def test_mac_not_match_global_standard(self):
        with pytest.raises(ValidationError):
            StreamingDevice(name='RPILEFT', mac='00-D0-56-F2-B5-', ip='128.0.0.1', streamAddress='')

    def test_ip_match_global_standard(self):
        try:
            StreamingDevice(name='RPILEFT', mac='00-D0-56-F2-B5-12', ip='128.0.0.1', streamAddress='')
        except ValidationError as e:
            self.fail(e)

    def test_ip_not_match_global_standard(self):
        with pytest.raises(ValidationError):
            StreamingDevice(name='RPILEFT', mac='00-D0-56-F2-B5-', ip='128.0.0.0.1', streamAddress='')
