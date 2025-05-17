from sqlalchemy import select
from fastapi import APIRouter, HTTPException, status

from schemas.user import *
from models.user import *
from utils.jwt_auth import *
from session import SessionDep

router = APIRouter()


@router.post('/create')
async def create_sender(data: UserSchema, session: SessionDep):
    new_sender = User(
        full_name=data.full_name,
        email=data.email,
        password=hash_password(data.password)
    )

    session.add(new_sender)
    await session.commit()
    await session.refresh(new_sender)
    return new_sender


@router.get('/read')
async def read_sender(session: SessionDep):
    result = await session.execute(select(User))

    sender = result.scalars().all()

    if sender:
        return sender

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="You don't have senders"
    )