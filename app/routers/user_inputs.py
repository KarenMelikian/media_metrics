from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete, update
from typing import List

from schemas.user_inputs import UserInputFieldCreateSchema, UserInputFieldReadSchema
from schemas.user import UserSchema
from models.user_inputs import UserInputField
from core.session import SessionDep
from utils.authorization_utils import check_access_and_get_user

router = APIRouter()


from fastapi import (
    APIRouter
)





router = APIRouter()



@router.post('/create')
async def create_labels(
        data: UserInputFieldCreateSchema,
        session: SessionDep,
        user: UserSchema = Depends(check_access_and_get_user)
):

    new_user_field = UserInputField(
        user_id=user.id,
        label=data.label,
        value=data.value
    )

    session.add(new_user_field)
    await session.commit()
    await session.refresh(new_user_field)
    return new_user_field


@router.get('/read', response_model=List[UserInputFieldReadSchema])
async def show_labels(
        session: SessionDep,
        user: UserSchema = Depends(check_access_and_get_user)
):
    result = await session.execute(
        select(UserInputField).where(UserInputField.user_id == user.id)
    )
    all_data = result.scalars().all()
    return all_data




@router.get('/read/{field_id}', response_model=UserInputFieldReadSchema)
async def show_label(
        field_id: int,
        session: SessionDep,
        user: UserSchema = Depends(check_access_and_get_user)
):
    result = await session.execute(
        select(UserInputField)
        .where(UserInputField.user_id == user.id, UserInputField.id==field_id)
    )
    field_data = result.scalars().one_or_none()
    if not field_data:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'UserField by this ID({field_id}) not found'
        )
    return field_data



@router.delete('/delete/{field_id}')
async def delete_label(
        field_id: int,
        session: SessionDep,
        user: UserSchema = Depends(check_access_and_get_user)
):
    result = await session.execute(
        delete(UserInputField)
        .where(UserInputField.id==field_id)
    )
    if result.rowcount == 0:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'UserField by this ID({field_id}) not found'
        )

    await session.commit()
    return {'status': "The User's field was successfully deleted"}





@router.patch('/update/{field_id}')
async def update_label(
        field_id: int,
        data: UserInputFieldCreateSchema,
        session: SessionDep,
        user: UserSchema = Depends(check_access_and_get_user)
):
    update_data = data.dict(exclude_unset=True)
    await session.execute(
        update(UserInputField)
        .where(UserInputField.id == field_id)
        .values(**update_data)
    )

    await session.commit()
    return {'status': "The User's field was successfully updated"}
