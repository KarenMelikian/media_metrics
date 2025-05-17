from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
