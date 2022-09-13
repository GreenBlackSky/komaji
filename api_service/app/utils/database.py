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
engine = create_async_engine(connection_string, echo=True)


def get_session():
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
