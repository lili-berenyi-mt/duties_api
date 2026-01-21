from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from . import db

class Base(DeclarativeBase):
    pass

class Ksb(db.Model):
    __tablename__ = 'ksbs'
    id = db.Column('id', db.Integer, primary_key=True)
    code = db.Column('name', db.String(255), nullable=False)
    description = db.Column('description', db.Text)