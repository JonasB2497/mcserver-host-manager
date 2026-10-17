import requests

from device_interface import DeviceInterface


class WebhookDevice(DeviceInterface):
    def __init__(self, url: str):
        self.url = url

    def up(self) -> bool:
        try:
            response = requests.post(self.url, json={"state": "on"})
            return response.ok
        except requests.RequestException:
            return False

    def down(self) -> bool:
        try:
            response = requests.post(self.url, json={"state": "off"})
            return response.ok
        except requests.RequestException:
            return False
