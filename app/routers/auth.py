from fastapi import (
    APIRouter,
    Depends
)

from utils.jwt_auth import create_token
from utils.authorization_utils import validate_auth_user, get_current_auth_user
from utils.get_tokens import get_access_token, get_refresh_token
from schemas.user import UserSchema
from schemas.auth import TokenInfo



router = APIRouter()




@router.post('/login')
async def user_login(
        user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
    }

    return TokenInfo(
        access_token=get_access_token(user),
        refresh_token=get_refresh_token(user),
    )


@router.get('/me')
async def self_info(
        user: UserSchema = Depends(get_current_auth_user)
):
    return {
        'full_name': user.full_name,
        'email': user.email
    }