from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)


from utils.authorization_utils import validate_auth_user, check_access_and_get_user, check_refresh_and_get_user
from utils.get_tokens import get_access_token, get_refresh_token
from utils.jwt_auth import hash_password
from models.user import User
from schemas.user import UserSchema
from schemas.auth import TokenInfo
from core.session import SessionDep


router = APIRouter()



@router.post('/register')
async def create_sender(data: UserSchema, session: SessionDep):
    new_user = User(
        full_name=data.full_name,
        email=data.email,
        password=hash_password(data.password)
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail={"user_id": new_user.id}
    )





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