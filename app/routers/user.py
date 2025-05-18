from sqlalchemy import select
from fastapi import APIRouter, HTTPException, status

from models.user import *
from core.session import SessionDep

router = APIRouter()



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