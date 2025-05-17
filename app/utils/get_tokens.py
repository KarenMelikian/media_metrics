from datetime import timedelta

from .jwt_auth import create_token
from config import settings
from schemas.user import UserSchema


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_timedelta: timedelta
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)

    return create_token(
        payload=jwt_payload,
        expire_timedelta=expire_timedelta,
    )


def get_access_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "full_name": user.full_name,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=settings.JWT_ACCESS_TOKEN_LIFETIME,
    )


def get_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": str(user.id),
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=settings.JWT_REFRESH_TOKEN_LIFETIME,
    )