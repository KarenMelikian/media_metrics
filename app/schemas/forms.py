from typing import Dict, List
from pydantic import BaseModel
from datetime import datetime

class CreateFormSchema(BaseModel):
    name: str


class CreateFormFieldSchema(BaseModel):
    label: str


class SubmitFormSchema(BaseModel):
    values: Dict[int, str]


class SubmissionResponseSchema(BaseModel):
    submission_id: int
    created_at: datetime
    values: Dict[str, str]


class FormFieldResponseSchema(BaseModel):
    id: int
    label: str

    class Config:
        orm_mode = True

class FormResponseSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SubmissionUpdateSchema(BaseModel):
    values: Dict[str, str]