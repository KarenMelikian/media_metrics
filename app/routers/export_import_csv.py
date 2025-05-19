import csv
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from io import StringIO

from schemas.user import UserSchema
from models.user_inputs import UserInputField
from utils.authorization_utils import check_access_and_get_user
from core.session import SessionDep

router = APIRouter()




@router.get("/export")
async def export_fields(
        session: SessionDep,
        user: UserSchema = Depends(check_access_and_get_user)
):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "label", "value"])

    fields = await session.execute(select(UserInputField).where(UserInputField.user_id == user.id))
    for field in fields.scalars():
        writer.writerow([field.id, field.label, field.value])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=fields.csv"
    })


@router.post("/import")
async def import_fields(
        session: SessionDep,
        user: UserSchema = Depends(check_access_and_get_user),
    file: UploadFile = File(...)
):
    contents = await file.read()
    decoded = contents.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    for row in reader:
        new_field = UserInputField(
            label=row["label"],
            value=row["value"],
            user_id=user.id
        )
        session.add(new_field)

    await session.commit()
    return {"detail": "Fields imported successfully"}