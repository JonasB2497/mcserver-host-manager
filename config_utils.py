import os
from enum import Enum
from typing import NotRequired, TypedDict

CONFIG_FILE = os.environ.get("CONFIG_PATH", "config.yaml")
DATABASE_PATH = os.environ.get("DATABASE_PATH", "server_states.db")


class ServerStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class Server(TypedDict):
    hostname: str


class Wol(TypedDict):
    host: str
    mac: str


class Webhook(TypedDict):
    webhook: str


class Device(TypedDict):
    name: str
    servers: list[Server]
    wol: NotRequired[Wol]
    webhook: NotRequired[Webhook]
    debug: NotRequired[str]


type Config = dict[str, list[Device]]


def validate_config(cfg: Config) -> None:
    if not cfg or "devices" not in cfg:
        raise ValueError("Config must contain a 'devices' list")

    for i, device in enumerate(cfg["devices"]):
        if "name" not in device:
            raise ValueError(f"Device at index {i} is missing 'name'")
        if "servers" not in device:
            raise ValueError(f"Device '{device.get('name', i)}' is missing 'servers'")

        has_wol = "wol" in device
        has_webhook = "webhook" in device
        has_debug = "debug" in device

        if (has_wol + has_webhook + has_debug) != 1:
            raise ValueError(
                f"Device '{device.get('name', i)}' must have exactly one of 'wol', 'webhook' or 'debug'"
            )
