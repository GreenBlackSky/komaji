"""
Note logic stuff.
"""


from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .utils.exceptions import LogicException
from .utils.models import NoteModel, UserModel
from .utils.database import get_session
from .user import authorized_user

router = APIRouter()


class NoteRequest(BaseModel):
    text:str


@router.post("/create_note")
async def create_note(
    note_request: NoteRequest,
    user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Create new note."""
    note = NoteModel(text=note_request.text, user_id=user.id)
    session: AsyncSession
    async with async_session() as session:
        session.add(note)
        await session.commit()

    return {
        "status": "OK",
        "note": note.to_dict(),
    }


@router.get("/get_notes")
async def get_notes(
    user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Get users notes."""
    query = select(NoteModel).where(NoteModel.user_id == user.id)
    session: AsyncSession
    async with async_session() as session:
        notes = await session.execute(query)
    return {
        "status": "OK",
        "notes": [note.to_dict() for (note,) in notes.all()],
    }


@router.put("/edit_note/{note_id}")
async def edit_note(
    note_id: int,
    note_request: NoteModel,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Edit note."""
    session: AsyncSession
    async with async_session() as session:
        note: NoteModel = await session.get(NoteModel, note_id)
        if note is None:
            raise LogicException(f"no such note id: {note_id}")
        if note.user_id != current_user.id:
            raise LogicException(f"editing private note: {note_id}")
        note.text = note_request.text
        await session.commit()
    return {"status": "OK", "user": note.to_dict()}


@router.delete("/delete_note{note_id}")
async def delete_note(
    note_id: int,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Delete note."""
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            note: NoteModel = await session.get(
                NoteModel,
                note_id,
            )
            if note is None:
                raise LogicException(f"no such note: {note_id}")
            if note.user_id != current_user.id:
                raise LogicException(f"editing private note: {note_id}")
            await session.delete(note)

    return {"status": "OK", "note": note.to_dict()}