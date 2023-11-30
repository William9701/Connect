from hashlib import md5

from models.base_models import Basemodels, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
import models
from models.content import Content
from models.comment import Comment
from sqlalchemy.orm import relationship, Session


class User(Basemodels, Base):
    __tablename__ = 'users'
    if models.storage_t == "db":

        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        location = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=False)
        contents = relationship("Content", backref="user", cascade="all, delete, delete-orphan")
        comments = relationship("Comment", backref="user", cascade="all, delete, delete-orphan")
    else:
        first_name = ""
        last_name = ""
        email = ""
        password = ""
        location = ""
        description = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

    @classmethod
    def login(cls, email, password):
        """Log in a user with the given email and password."""
        # Hash the password
        hashed_password = md5(password.encode()).hexdigest()

        # Create a session
        session = Session(models.storage.__engine)

        # Query for the user
        user = session.query(cls).filter_by(email=email, password=hashed_password).first()

        # If the user was found and the password is correct, return the user
        if user is not None:
            return user

        # If the user was not found or the password is incorrect, return None
        return None