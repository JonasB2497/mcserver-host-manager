import requests

from device_interface import DeviceInterface


class WebhookDevice(DeviceInterface):
    def __init__(self, url: str):
        self.url = url

    def up(self) -> None:
        requests.post(self.url, json={"state": "on"})

    def down(self) -> None:
        requests.post(self.url, json={"state": "off"})
