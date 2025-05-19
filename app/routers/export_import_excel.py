from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from io import BytesIO
from openpyxl import Workbook, load_workbook

from schemas.user import UserSchema
from models.user_inputs import UserInputField
from utils.authorization_utils import check_access_and_get_user
from core.session import SessionDep

router = APIRouter()




@router.get("/export/excel")
async def export_excel_fields(
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user)
):
    wb = Workbook()
    ws = wb.active
    ws.title = "User Fields"
    ws.append(["id", "label", "value"])

    fields = await session.execute(select(UserInputField).where(UserInputField.user_id == user.id))
    for field in fields.scalars():
        ws.append([field.id, field.label, field.value])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={
        "Content-Disposition": "attachment; filename=fields.xlsx"
    })


@router.post("/import/excel")
async def import_excel_fields(
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user),
    file: UploadFile = File(...)
):
    contents = await file.read()
    workbook = load_workbook(filename=BytesIO(contents))
    sheet = workbook.active

    for idx, row in enumerate(sheet.iter_rows(values_only=True)):
        if idx == 0:
            continue
        _, label, value = row
        session.add(UserInputField(label=label, value=value, user_id=user.id))

    await session.commit()
    return {"detail": "Fields imported successfully from Excel"}