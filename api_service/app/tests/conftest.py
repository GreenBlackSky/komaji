import datetime as dt

import pytest

from ..utils.models import UserModel


@pytest.fixture
def anyio_backend():
    return "asyncio"


def full_user_data():
    return {
        "id": 1,
        "name": "TestGuy",
        "password_hash": "dcf7fb88d38b9cbc0719c4d47af0b9ca",
    }


def simple_user():
    return UserModel(**full_user_data())


def one_user_db():
    return {
        "users": [full_user_data()],
    }


def new_account_data():
    return {"id": 2, "user_id": 1, "name": "TestAccount"}
