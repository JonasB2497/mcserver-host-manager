from datetime import UTC, datetime

from flask import Blueprint, jsonify, request

from config_utils import ServerStatus
from device import create_device
from models import ServerStateModel, db

scale_bp = Blueprint("scale_bp", __name__)


@scale_bp.route("/scale", methods=["POST"])
def scale():
    # Import app inside the function to break circular dependency
    from app import app as flask_app

    data = request.get_json()
    print(data)
    action = data.get("action")
    server_address = data.get("serverAddress")

    if not action or not server_address:
        return jsonify(
            {"status": "error", "message": "Missing action or serverAddress"}
        ), 400

    config = flask_app.config["CONFIG_DATA"]

    # Find the device associated with this serverAddress
    device_cfg = next(
        (
            d
            for d in config.get("devices", [])
            if any(s["hostname"] == server_address for s in d.get("servers", []))
        ),
        None,
    )

    if not device_cfg:
        return jsonify(
            {"status": "error", "message": "Server address not found in config"}
        ), 404

    device_name = device_cfg["name"]
    device_hostnames = [s["hostname"] for s in device_cfg.get("servers", [])]

    if action == "up":
        target = ServerStateModel.query.filter_by(hostname=server_address).first()
        device_states = ServerStateModel.query.filter(
            ServerStateModel.hostname.in_(device_hostnames)
        ).all()

        is_online = any(s.status == ServerStatus.ONLINE.value for s in device_states)

        if target and target.status != ServerStatus.ONLINE.value:
            target.status = ServerStatus.ONLINE.value
            target.updated_at = datetime.now(UTC)
            db.session.commit()

        if not is_online:
            device = create_device(device_cfg)
            if not device.up():
                return jsonify(
                    {"status": "error", "message": "Failed to power up device"}
                ), 500

        return jsonify(
            {"status": "success", "device": device_name, "action": "up"}
        ), 200

    elif action == "down":
        target = ServerStateModel.query.filter_by(hostname=server_address).first()
        device_states = ServerStateModel.query.filter(
            ServerStateModel.hostname.in_(device_hostnames)
        ).all()

        other_online = any(
            s.hostname != server_address and s.status == ServerStatus.ONLINE.value
            for s in device_states
        )
        was_last_online = (
            target is not None
            and target.status == ServerStatus.ONLINE.value
            and not other_online
        )

        if target and target.status != ServerStatus.OFFLINE.value:
            target.status = ServerStatus.OFFLINE.value
            target.updated_at = datetime.now(UTC)
            db.session.commit()

        if was_last_online:
            device = create_device(device_cfg)
            if not device.down():
                return jsonify(
                    {"status": "error", "message": "Failed to power down device"}
                ), 500

        return jsonify(
            {"status": "success", "device": device_name, "action": "down"}
        ), 200

    return jsonify({"status": "error", "message": "Invalid action"}), 400


@scale_bp.route("/status", methods=["GET"])
def status():
    servers = ServerStateModel.query.all()
    result = [
        {
            "hostname": s.hostname,
            "status": s.status,
            "updated_at": s.updated_at.isoformat() if s.updated_at else None,
        }
        for s in servers
    ]
    return jsonify({"status": "success", "servers": result}), 200
