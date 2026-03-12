from . import db
from sqlalchemy.orm import DeclarativeBase, validates
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
    pass

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    