from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, delete, asc, desc
from typing import List, Literal

from core.session import SessionDep
from models.user_inputs import Form, FormField, FormSubmission, FormSubmissionField
from schemas.forms import (
    CreateFormSchema,
    CreateFormFieldSchema,
    SubmitFormSchema,
    SubmissionResponseSchema,
    FormResponseSchema,
    FormFieldResponseSchema,
    SubmissionUpdateSchema,
)
from utils.authorization_utils import check_access_and_get_user
from schemas.user import UserSchema

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_form(
    data: CreateFormSchema,
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user)
):
    form = Form(name=data.name, user_id=user.id)
    session.add(form)
    await session.commit()
    await session.refresh(form)
    return {"form_id": form.id}


@router.get("/", response_model=List[FormResponseSchema])
async def get_forms(
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user)
):
    query = await session.execute(select(Form).where(Form.user_id == user.id))
    forms = query.scalars().all()
    return forms


@router.get("/{form_id}/fields", response_model=List[FormFieldResponseSchema])
async def get_fields(
    form_id: int,
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user)
):
    form = await session.get(Form, form_id)
    if not form or form.user_id != user.id:
        raise HTTPException(status_code=404, detail="Form not found or not yours")

    query = await session.execute(select(FormField).where(FormField.form_id == form_id))
    fields = query.scalars().all()
    return fields


@router.post("/{form_id}/fields", status_code=status.HTTP_201_CREATED)
async def add_fields_to_form(
    form_id: int,
    fields: List[CreateFormFieldSchema],
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user)
):
    form = await session.get(Form, form_id)
    if not form or form.user_id != user.id:
        raise HTTPException(status_code=404, detail="Form not found or not yours")

    for field in fields:
        if not field.label.strip():
            continue
        session.add(FormField(label=field.label.strip(), form_id=form_id))

    await session.commit()
    return {"detail": "Fields added"}


@router.delete("/{form_id}/fields/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field(
    form_id: int,
    field_id: int,
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user)
):
    form = await session.get(Form, form_id)
    if not form or form.user_id != user.id:
        raise HTTPException(status_code=404, detail="Form not found or not yours")

    field = await session.get(FormField, field_id)
    if not field or field.form_id != form_id:
        raise HTTPException(status_code=404, detail="Field not found or does not belong to this form")

    await session.execute(delete(FormSubmissionField).where(FormSubmissionField.field_id == field_id))
    await session.delete(field)
    await session.commit()
    return


@router.post("/{form_id}/submit", status_code=status.HTTP_201_CREATED)
async def submit_form(
    form_id: int,
    data: SubmitFormSchema,
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user)
):
    form = await session.get(Form, form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")

    submission = FormSubmission(form_id=form_id, user_id=user.id)
    session.add(submission)
    await session.flush()

    for field_id_str, value in data.values.items():
        try:
            field_id = int(field_id_str)
        except ValueError:
            continue
        session.add(FormSubmissionField(
            submission_id=submission.id,
            field_id=field_id,
            value=value.strip() if isinstance(value, str) else value
        ))

    await session.commit()
    return {"submission_id": submission.id}


@router.get("/{form_id}/submissions", response_model=List[SubmissionResponseSchema])
async def get_submissions(
    form_id: int,
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user),
    order_by: Literal["created_at", "submission_id"] = Query("created_at"),
    order_dir: Literal["asc", "desc"] = Query("desc")
):
    form = await session.get(Form, form_id)
    if not form or form.user_id != user.id:
        raise HTTPException(status_code=404, detail="Form not found or not yours")

    # Determine ordering column and direction
    order_column = {
        "created_at": FormSubmission.created_at,
        "submission_id": FormSubmission.id,
    }[order_by]

    order_func = asc if order_dir == "asc" else desc

    query = await session.execute(
        select(FormSubmission)
        .where(FormSubmission.form_id == form_id)
        .order_by(order_func(order_column))
    )
    submissions = query.scalars().all()

    result = []
    for submission in submissions:
        values = {
            str(value.field_id): value.value
            for value in submission.values
        }
        result.append({
            "submission_id": submission.id,
            "created_at": submission.created_at,
            "values": values
        })

    return result


@router.put("/{form_id}/submissions/{submission_id}", response_model=dict)
async def update_submission(
    form_id: int,
    submission_id: int,
    submission_update: SubmissionUpdateSchema,
    session: SessionDep,
    user=Depends(check_access_and_get_user),
):
    form = await session.get(Form, form_id)
    if not form or form.user_id != user.id:
        raise HTTPException(status_code=404, detail="Form not found or access denied")

    submission = await session.get(FormSubmission, submission_id)
    if not submission or submission.form_id != form_id:
        raise HTTPException(status_code=404, detail="Submission not found")

    for field_id_str, new_value in submission_update.values.items():
        try:
            field_id = int(field_id_str)
        except ValueError:
            continue

        result = await session.execute(
            select(FormSubmissionField)
            .where(FormSubmissionField.submission_id == submission_id)
            .where(FormSubmissionField.field_id == field_id)
        )
        submission_field = result.scalars().first()

        if submission_field:
            submission_field.value = new_value
        else:
            new_field = FormSubmissionField(
                submission_id=submission_id,
                field_id=field_id,
                value=new_value,
            )
            session.add(new_field)

    await session.commit()
    await session.refresh(submission)

    return {"detail": "Submission updated successfully"}


@router.delete("/{form_id}/submissions/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_submission(
    form_id: int,
    submission_id: int,
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user)
):
    form = await session.get(Form, form_id)
    if not form or form.user_id != user.id:
        raise HTTPException(status_code=404, detail="Form not found or access denied")

    submission = await session.get(FormSubmission, submission_id)
    if not submission or submission.form_id != form_id:
        raise HTTPException(status_code=404, detail="Submission not found or does not belong to this form")

    await session.execute(delete(FormSubmissionField).where(FormSubmissionField.submission_id == submission_id))
    await session.delete(submission)
    await session.commit()

    return
