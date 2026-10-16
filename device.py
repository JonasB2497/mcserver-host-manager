from config_utils import Device
from device_debug import DeviceDebug
from device_interface import DeviceInterface
from device_webhook import WebhookDevice


def create_device(device_cfg: Device) -> DeviceInterface:
    if "debug" in device_cfg:
        return DeviceDebug(device_cfg["name"])

    if "webhook" in device_cfg:
        return WebhookDevice(device_cfg["webhook"]["webhook"])

    if "wol" in device_cfg:
        # WOL implementation empty for now
        raise NotImplementedError("WOL device not yet implemented")

    raise ValueError(
        f"No valid startup method found for device {device_cfg.get('name')}"
    )
