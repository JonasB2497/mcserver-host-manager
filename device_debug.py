from device_interface import DeviceInterface


class DeviceDebug(DeviceInterface):
    def __init__(self, name: str):
        self.name = name

    def up(self) -> bool:
        print(f"Device {self.name} is now UP")
        return True

    def down(self) -> bool:
        print(f"Device {self.name} is now DOWN")
        return True
