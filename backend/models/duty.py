from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, validates
from . import db
import uuid
import re

class Base(DeclarativeBase):
    pass

duty_ksb = db.Table('duty_ksb',
    db.Column('duty_id', db.String(36), db.ForeignKey('duties.id'), primary_key=True),
    db.Column('ksb_id', db.String(36), db.ForeignKey('ksbs.id'), primary_key=True)
)

class Duty(db.Model):
    __tablename__ = 'duties'
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    code = db.Column('code', db.String(10), nullable=False, unique=True)
    description = db.Column('description', db.String(255), nullable=False)
    ksbs = db.relationship('Ksb', secondary=duty_ksb, backref='duties')

    @validates('code')
    def validate_code(self, key, value):
        str_value = str(value)
        if str_value.isdigit():
            str_value = f"D{str_value}"
        pattern = r"^D\d{1,2}$"
        if not value or not re.match(pattern, str_value):
            raise ValueError(f"Invalid code '{value}'. Must start with 'D' followed by 1 or 2 digits (e.g., 'D1').")
        return str_value
    
    @validates('description')
    def validate_description(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 255:
            raise ValueError("Description must be a non-empty string under 255 characters.")
        return value
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "description": self.description,
            "ksbs": [ksb.code for ksb in self.ksbs]
        }