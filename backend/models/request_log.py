from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, validates
from . import db
import uuid
import re

class Base(DeclarativeBase):
    pass

class RequestLog(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    method = db.Column(db.String(10))
    path = db.Column(db.String(255))
    status_code = db.Column(db.Integer)
    remote_address = db.Column(db.String(45))

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "method": self.method,
            "path": self.path,
            "status_code": self.status_code,
            "remote_address": self.remote_address
        }