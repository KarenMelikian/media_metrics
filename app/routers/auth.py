from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    status,
    Depends
)
from sqlalchemy import select
from session import SessionDep
from models.user import *
from utils.jwt_auth import validate_password, create_token
from schemas.user import UserSchema
from schemas.auth import TokenInfo

router = APIRouter()


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


@router.post('/login')
async def user_login(
        user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        "sub": user.id,
        "email": user.email,
        "full_name": user.full_name,
    }

    token = create_token(jwt_payload)

    return TokenInfo(
        access_token=token,
        token_type='Bearer'
    )