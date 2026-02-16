from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Identity, Integer, VARCHAR, Text


class Course(SQLModel, table=True):
    id: int | None = Field(
        default=None, sa_column=Column(Integer, Identity(), primary_key=True)
    )
    course_name: str = Field(sa_column=Column(VARCHAR(255), nullable=False))
    course_detail: str | None = None


class CourseCreate(SQLModel):
    course_name: str
    course_detail: str
