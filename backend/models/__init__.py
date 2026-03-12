from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

from .ksb import Ksb
from .duty import Duty
from .theme import Theme
from .user import User
