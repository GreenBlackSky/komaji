import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


connection_string = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    os.environ.get("POSTGRES_USER"),
    os.environ.get("POSTGRES_PASSWORD"),
    os.environ.get("POSTGRES_HOST"),
    os.environ.get("POSTGRES_PORT"),
    os.environ.get("POSTGRES_DB"),
)

_engine = None


def _init_engine():
    global _engine
    _engine = create_async_engine(connection_string, echo=True)


def get_session():
    if _engine is None:
        _init_engine()
    return sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)
