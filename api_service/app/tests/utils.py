"""Some test utils."""

from contextlib import contextmanager
from dataclasses import dataclass
import datetime as dt

from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..main import app

from ..utils.models import Base, UserModel
from ..user import authorized_user


engine = create_async_engine(
    "sqlite+aiosqlite:///./test.db", connect_args={"check_same_thread": False}
)
db_models = {"users": UserModel}
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


@dataclass
class TestCase:
    db_before: dict[str, list]
    user: UserModel | None
    request_data: dict
    response_data: tuple[dict, int]
    db_after: dict[str, list]


def compare_with_skip(val_1, val_2, skipped: set):
    if type(val_1) != type(val_2):
        return False

    if isinstance(val_1, dict):
        keys_1 = set(val_1.keys()) - skipped
        keys_2 = set(val_2.keys()) - skipped
        if keys_1 != keys_2:
            return False

        for key in keys_1:
            if not compare_with_skip(val_1[key], val_2[key], skipped):
                return False

    elif isinstance(val_1, list | tuple):
        if not all(
            compare_with_skip(elem_1, elem_2, skipped)
            for elem_1, elem_2 in zip(val_1, val_2)
        ):
            return False

    elif val_1 != val_2:
        return False

    return True


async def prepare_db(**values):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    to_add = []
    for table_name, objects in values.items():
        for object_data in objects:
            obj = db_models[table_name](**object_data)
            if "event_time" in object_data:
                obj.event_time = dt.datetime.fromtimestamp(obj.event_time)
            to_add.append(obj)

    async with async_session() as session:
        async with session.begin():
            session.add_all(to_add)


async def get_db():
    result = {}
    async with async_session() as session:
        for table_name, model in db_models.items():
            rows = await session.execute(select(model))
            result[table_name] = [
                entity.to_dict() for entity in rows.scalars()
            ]
    return result


@contextmanager
def set_current_user(app: FastAPI, user: UserModel | None):
    if user:
        app.dependency_overrides[authorized_user] = lambda: user
    try:
        yield app
    finally:
        app.dependency_overrides.pop(authorized_user, None)


async def base_test(path, case: TestCase):
    response_data, result_code = case.response_data
    with set_current_user(app, case.user):
        await prepare_db(**case.db_before)
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(path, json=case.request_data)
        assert response.status_code == result_code, response.text
        data = response.json()
        assert compare_with_skip(
            data, response_data, {"access_token"}
        ), f"{data} vs. {response_data}"
        db = await get_db()
        assert db == case.db_after, f"{db} vs. {case.db_after}"
