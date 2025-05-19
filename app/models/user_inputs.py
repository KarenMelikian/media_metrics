from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from core.database import Base


class Form(Base):
    __tablename__ = "forms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(56), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    fields = relationship("FormField", back_populates="form", cascade="all, delete")
    submissions = relationship("FormSubmission", back_populates="form")


class FormField(Base):
    __tablename__ = "form_fields"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(56), nullable=False)
    form_id: Mapped[int] = mapped_column(ForeignKey("forms.id"), nullable=False)

    form = relationship("Form", back_populates="fields")


class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    form_id: Mapped[int] = mapped_column(ForeignKey("forms.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    form = relationship("Form", back_populates="submissions")
    values = relationship("FormSubmissionField", back_populates="submission", lazy="selectin", cascade="all, delete")


class FormSubmissionField(Base):
    __tablename__ = "form_submission_fields"

    id: Mapped[int] = mapped_column(primary_key=True)
    submission_id: Mapped[int] = mapped_column(ForeignKey("form_submissions.id"), nullable=False)
    field_id: Mapped[int] = mapped_column(ForeignKey("form_fields.id"), nullable=False)
    value: Mapped[str] = mapped_column(String(128))

    submission = relationship("FormSubmission", back_populates="values")
