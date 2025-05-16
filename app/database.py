from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


engine = create_async_engine(
    url=settings.DATABASE_URL,
    # echo=True,
    pool_size=10,
    max_overflow=15
)


class Base(DeclarativeBase):
    pass