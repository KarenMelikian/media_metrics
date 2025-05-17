import bcrypt
import jwt
from datetime import datetime
from config import settings

def create_token(payload: dict) -> str:
    to_encode = payload.copy()
    to_encode.update(
        exp=datetime.utcnow() + settings.JWT_ACCESS_TOKEN_LIFETIME,
        iat=datetime.utcnow()
    )

    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode()
    )