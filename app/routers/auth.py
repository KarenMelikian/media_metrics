from fastapi import (
    APIRouter,
    Depends
)


from utils.authorization_utils import validate_auth_user, check_access_and_get_user, check_refresh_and_get_user
from utils.get_tokens import get_access_token, get_refresh_token
from schemas.user import UserSchema
from schemas.auth import TokenInfo



router = APIRouter()




@router.post('/login')
async def user_login(
        user: UserSchema = Depends(validate_auth_user)
):
    return TokenInfo(
        access_token=get_access_token(user),
        refresh_token=get_refresh_token(user),
    )


@router.get('/me')
async def self_info(
        user: UserSchema = Depends(check_access_and_get_user)
):
    return {
        'full_name': user.full_name,
        'email': user.email
    }


@router.post('/refresh')
async def refresh_token(
        user: UserSchema = Depends(check_refresh_and_get_user)
):
    return TokenInfo(
        access_token=get_access_token(user),
        refresh_token=get_refresh_token(user),
    )