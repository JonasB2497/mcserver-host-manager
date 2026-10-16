from device_interface import DeviceInterface


class DeviceDebug(DeviceInterface):
    def __init__(self, name: str):
        self.name = name

    def up(self) -> None:
        print(f"Device {self.name} is now UP")

    def down(self) -> None:
        print(f"Device {self.name} is now DOWN")
