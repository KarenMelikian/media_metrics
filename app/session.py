from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Annotated

from database import engine

Session = async_sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

async def get_session():
    async with Session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]