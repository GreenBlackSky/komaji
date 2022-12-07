"""Data base models."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    BigInteger,
)
from sqlalchemy.orm import relationship


Base = declarative_base()

class Serializable:
    def to_dict(self) -> dict:
        raise NotImplementedError

    def to_dict_raw(self) -> dict:
        raise NotImplementedError


class UserModel(Base, Serializable):
    """Well, it's User."""

    __tablename__ = "users"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    name = Column(String(200), nullable=False)
    password_hash = Column(String(500), nullable=False)
    notes = relationship("NoteModel", back_populates="user", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def to_dict_raw(self):
        return {
            "id": self.id,
            "name": self.name,
            "password_hash": self.password_hash
        }


class NoteModel(Base, Serializable):
    "DB model for note."

    __tablename__ = "notes"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    user_id = Column(
        BigInteger().with_variant(Integer, "sqlite"), ForeignKey("users.id")
    )
    text = Column(String(2000), nullable=False)
    user = relationship("UserModel", back_populates="notes")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "text": self.text, 
        }

    def to_dict_raw(self):
        return self.to_dict()