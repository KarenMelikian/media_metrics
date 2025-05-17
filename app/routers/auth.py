from fastapi import (
    APIRouter,
    Depends
)

from utils.jwt_auth import create_token
from utils.authorization_utils import validate_auth_user, get_current_auth_user
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

    token = create_token(jwt_payload)

    return TokenInfo(
        access_token=token,
        token_type='Bearer'
    )

@router.get('/me')
async def self_info(
        user: UserSchema = Depends(get_current_auth_user)
):
    return {
        'full_name': user.full_name,
        'email': user.email
    }