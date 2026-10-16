from abc import ABC, abstractmethod


class DeviceInterface(ABC):
    @abstractmethod
    def up(self) -> None:
        """Start the device."""

    @abstractmethod
    def down(self) -> None:
        """Stop the device."""
