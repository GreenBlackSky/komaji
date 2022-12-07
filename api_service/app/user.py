"""
User logic stuff.

This module contains methods to create new user or
to get access to existing one.
"""

from hashlib import md5

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .utils.exceptions import LogicException
from .utils.models import UserModel
from .utils.database import get_session


router = APIRouter()


async def authorized_user(
    authorize: AuthJWT = Depends(),
    async_session: sessionmaker = Depends(get_session),
) -> UserModel:
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    async with async_session() as session:
        return await session.get(UserModel, user_id)


class UserRequest(BaseModel):
    name: str
    password: str


@router.post("/register")
async def register(
    user_data: UserRequest,
    authorize: AuthJWT = Depends(),
    async_session: sessionmaker = Depends(get_session),
):
    """Register new user."""
    if authorize.get_jwt_subject():
        raise LogicException("already authorized")

    session: AsyncSession
    async with async_session() as session:
        query = await session.execute(
            select(UserModel).where(UserModel.name == user_data.name)
        )

        if query.first():
            raise LogicException("user exists")

        user = UserModel(
            name=user_data.name,
            password_hash=md5(user_data.password.encode()).hexdigest(),
        )
        session.add(user)
        await session.commit()
        user_dict = user.to_dict()

    return {
        "access_token": authorize.create_access_token(subject=user.id),
        "status": "OK",
        "user": user_dict,
    }


@router.post("/login")
async def login(
    user_data: UserRequest,
    authorize: AuthJWT = Depends(),
    async_session: sessionmaker = Depends(get_session),
):
    """Log in user."""
    session: AsyncSession
    async with async_session() as session:
        user: UserModel | None = (
            (
                await session.execute(
                    select(UserModel).where(UserModel.name == user_data.name)
                )
            )
            .scalars()
            .first()
        )

    if not user:
        raise LogicException("no such user")

    if user.password_hash != md5(user_data.password.encode()).hexdigest():
        raise LogicException("wrong password")

    return {
        "status": "OK",
        "user": user.to_dict(),
        "access_token": authorize.create_access_token(subject=user.id),
    }


@router.get("/user_data")
async def get_user_data(user: UserModel = Depends(authorized_user)):
    return {"status": "OK", "user": user.to_dict()}


class EditUserRequest(BaseModel):
    name: str
    old_pass: str
    new_pass: str


@router.put("/edit_user")
async def edit_user(
    user_data: EditUserRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Edit user."""
    session: AsyncSession
    async with async_session() as session:
        if user_data.name != current_user.name:
            query = await session.execute(
                select(UserModel).where(UserModel.name == user_data.name)
            )
            if query.first():
                raise LogicException("user exists")

        current_user.name = user_data.name

        got_old_pass = user_data.old_pass is not None
        got_new_pass = user_data.new_pass is not None
        if got_new_pass != got_old_pass:
            raise LogicException(
                "new password must be provided with an old password"
            )

        if got_old_pass and got_new_pass:
            old_hash = md5(user_data.old_pass.encode()).hexdigest()
            if old_hash != current_user.password_hash:
                raise LogicException("wrong password")
            new_hash = md5(user_data.new_pass.encode()).hexdigest()
            current_user.password_hash = new_hash

        await session.commit()

    return {"status": "OK", "user": current_user.to_dict()}


@router.post("/logout")
async def logout(Authorize: AuthJWT = Depends()):
    """Log out user."""
    Authorize.jwt_required()

    return {"status": "OK"}
