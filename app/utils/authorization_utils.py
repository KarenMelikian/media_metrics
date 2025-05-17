from fastapi import (
    Form,
    HTTPException,
    status,
    Depends
)
from sqlalchemy import select
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from session import SessionDep
from models.user import *
from utils.jwt_auth import validate_password, decode_token

http_bearer = HTTPBearer()


async def validate_auth_user(
        session: SessionDep,
        email: str = Form(),
        password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid email or password'
    )
    user_query = await session.execute(
        select(User).where(User.email==email)
    )
    user = user_query.scalars().one_or_none()
    if not user:
        raise unauthed_exc

    if validate_password(
        password=password,
        hashed_password=user.password
    ):
        return user

    raise unauthed_exc



async def get_current_auth_user(
        session: SessionDep,
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> User:
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token error'
        )
    user_id = int(payload["sub"])
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
