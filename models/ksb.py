from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, validates
from . import db
import uuid
import re

class Base(DeclarativeBase):
    pass

class Ksb(db.Model):
    __tablename__ = 'ksbs'
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    code = db.Column('name', db.String(255), nullable=False)
    description = db.Column('description', db.Text)

    @validates('code')
    def validate_code(self, key, value):
        pattern = r"^[KSB](\d{1}|\d{3})$"
        if not value or not re.match(pattern, value):
            raise ValueError(f"Invalid code '{value}'. Must start with K, S, or B followed by 1 or 3 digits (e.g., K1, S101).")
        return value

    @validates('description')
    def validate_description(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 255:
            raise ValueError("Description must be a non-empty string under 255 characters.")
        return value
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "description": self.description
        }
    
    def update(self, new_code, new_description):
        self.code = new_code
        self.description = new_description