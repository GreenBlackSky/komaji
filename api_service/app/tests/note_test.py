"""Notes tests."""

import pytest

from .utils import async_session, base_test, TestCase
from .conftest import one_user_db, simple_user

from ..main import app
from ..utils.database import get_session


app.dependency_overrides[get_session] = lambda: async_session
pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "case",
    []
)
async def test_create_note(case: TestCase):
    await base_test("/create_note", "POST", case)


@pytest.mark.parametrize(
    "case",
    []
)
async def test_get_notes(case: TestCase):
    await base_test("/get_notes", "GET", case)


@pytest.mark.parametrize(
    "case,note_id",
    []
)
async def test_edit_note(case: TestCase, note_id: int):
    await base_test(f"/edit_note/{note_id}", "PUT", case)


@pytest.mark.parametrize(
    "case,note_id",
    []
)
async def test_delete_note(case: TestCase, note_id: int):
    await base_test(f"/delete_note{note_id}", "DELETE", case)
