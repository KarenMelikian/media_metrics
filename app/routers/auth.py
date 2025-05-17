from sqlalchemy import select, update, delete, literal, or_, and_
from fastapi import APIRouter, HTTPException, status, Query

from schemas.user import *
from models.user import *
from session import SessionDep

router = APIRouter()


@router.post('/create')
async def create_sender(data: UserSchema, session: SessionDep):
    new_sender = User(
        full_name=data.full_name,
        email=data.email,
        password=data.password
    )

    session.add(new_sender)
    await session.commit()
    await session.refresh(new_sender)
    return new_sender


@router.get('/read')
async def read_sender(session: SessionDep):
    result = await session.execute(select(User))

    sender = result.scalars().one_or_none()

    if sender:
        return sender

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="You don't have senders"
    )