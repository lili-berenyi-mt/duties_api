from . import db
from sqlalchemy.orm import DeclarativeBase, validates
import uuid


class Base(DeclarativeBase):
    pass

theme_duty = db.Table('theme_duty',
    db.Column('theme_id', db.String(36), db.ForeignKey('themes.id'), primary_key=True),
    db.Column('duty_id', db.String(36), db.ForeignKey('duties.id'), primary_key=True)
)

class Theme(db.Model):
    __tablename__ = 'themes'
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = db.Column('name', db.String(255), nullable=False, unique=True)
    description = db.Column('description', db.String(255), nullable=False)
    duties = db.relationship('Duty', secondary=theme_duty, backref='themes')

    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 255:
            raise ValueError("Name must be a non-empty string under 255 characters.")
        return value
    
    @validates('description')
    def validate_description(self, key, value):
        if not isinstance(value, str) or not value.strip() or len(value) > 255:
            raise ValueError("Description must be a non-empty string under 255 characters.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "duties": [duty.code for duty in self.duties]
        }
    
    