"""Data base models."""

import datetime as dt

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger


Base = declarative_base()


class Serializable:
    def to_dict(self):
        return {
            key: (
                value.timestamp()
                if isinstance(value := getattr(self, key), dt.datetime)
                else value
            )
            for key in dir(self)
            if (
                not key.startswith("_")
                and key
                not in ("to_dict_safe", "to_dict", "metadata", "registry")
            )
        }


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

    def to_dict_safe(self):
        user_data = super().to_dict()
        del user_data["password_hash"]
        return user_data
