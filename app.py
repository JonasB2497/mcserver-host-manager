import sys

import yaml
from flask import Flask

from config_utils import (
    CONFIG_FILE,
    DATABASE_PATH,
    ServerStatus,
    validate_config,
)
from models import ServerStateModel, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with open(CONFIG_FILE, "r") as f:
    cfg = yaml.safe_load(f)

try:
    validate_config(cfg)
except ValueError as e:
    print(f"Configuration error: {e}")
    sys.exit(1)

app.config["CONFIG_DATA"] = cfg

with app.app_context():
    db.create_all()

    config_hostnames = {
        server["hostname"]
        for device in cfg.get("devices", [])
        for server in device.get("servers", [])
    }

    existing_rows = ServerStateModel.query.all()
    existing_hostnames = {row.hostname for row in existing_rows}

    for hostname in config_hostnames - existing_hostnames:
        db.session.add(
            ServerStateModel(
                hostname=hostname,
                status=ServerStatus.OFFLINE.value,
            )
        )

    for hostname in existing_hostnames - config_hostnames:
        ServerStateModel.query.filter_by(hostname=hostname).delete()

    db.session.commit()

from endpoints import scale_bp

app.register_blueprint(scale_bp)


@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
