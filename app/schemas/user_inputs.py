from datetime import datetime

from pydantic import BaseModel


class UserInputFieldCreate(BaseModel):
    label: str
    value: str


class UserInputFieldRead(UserInputFieldCreate):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True