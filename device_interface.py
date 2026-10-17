from abc import ABC, abstractmethod


class DeviceInterface(ABC):
    @abstractmethod
    def up(self) -> bool:
        """Start the device. Returns true if successful false otherwise."""

    @abstractmethod
    def down(self) -> bool:
        """Stop the device. Returns true if successful false otherwise."""
