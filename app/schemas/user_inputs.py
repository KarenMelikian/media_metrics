from datetime import datetime

from pydantic import BaseModel


class UserInputFieldCreateSchema(BaseModel):
    label: str
    value: str


class UserInputFieldReadSchema(UserInputFieldCreateSchema):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True