from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ServerStateModel(db.Model):  # type: ignore[name-defined]
    __tablename__ = "server_states"

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.String(32), nullable=False)
