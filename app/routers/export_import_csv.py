import csv
from io import StringIO
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from schemas.user import UserSchema
from models.user_inputs import FormSubmission, FormSubmissionField, FormField, Form
from utils.authorization_utils import check_access_and_get_user
from core.session import SessionDep

router = APIRouter()





@router.get("/export")
async def export_submissions(
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user)
):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["submission_id", "form_id", "created_at", "field_label", "value"])

    stmt = (
        select(FormSubmission)
        .options(joinedload(FormSubmission.values).joinedload(FormSubmissionField.submission))
        .where(FormSubmission.user_id == user.id)
    )
    result = await session.execute(stmt)
    submissions = result.unique().scalars().all()

    for submission in submissions:
        for val in submission.values:
            field = await session.get(FormField, val.field_id)
            label = field.label if field else "Unknown"
            writer.writerow([
                submission.id,
                submission.form_id,
                submission.created_at.isoformat(),
                label,
                val.value
            ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=submissions.csv"
    })



@router.post("/import")
async def import_submissions(
    session: SessionDep,
    user: UserSchema = Depends(check_access_and_get_user),
    file: UploadFile = File(...)
):
    contents = await file.read()
    decoded = contents.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    submissions_map = {}

    for row in reader:
        sid = row["submission_id"]
        if sid not in submissions_map:
            submissions_map[sid] = {
                "form_id": int(row["form_id"]),
                "created_at": row["created_at"],
                "values": []
            }
        submissions_map[sid]["values"].append({
            "label": row["field_label"],
            "value": row["value"]
        })

    for sid, data in submissions_map.items():
        submission = FormSubmission(
            form_id=data["form_id"],
            user_id=user.id,
            created_at=data["created_at"]
        )
        session.add(submission)
        await session.flush()

        for item in data["values"]:
            field = await session.execute(
                select(FormField).where(FormField.label == item["label"], FormField.form_id == data["form_id"])
            )
            field_obj = field.scalar()
            if not field_obj:
                raise HTTPException(status_code=400, detail=f"Field label '{item['label']}' not found in form {data['form_id']}.")

            submission_value = FormSubmissionField(
                submission_id=submission.id,
                field_id=field_obj.id,
                value=item["value"]
            )
            session.add(submission_value)

    await session.commit()
    return {"detail": "Submissions imported successfully"}
