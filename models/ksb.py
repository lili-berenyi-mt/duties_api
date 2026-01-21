from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from . import db
import uuid

class Base(DeclarativeBase):
    pass

class Ksb(db.Model):
    __tablename__ = 'ksbs'
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    code = db.Column('name', db.String(255), nullable=False)
    description = db.Column('description', db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "description": self.description
        }