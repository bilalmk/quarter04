from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, Identity, VARCHAR


class Students(SQLModel, table=True):
    # __tablename__ = "student"
    id: int | None = Field(
        default=None, sa_column=Column(Integer, Identity(), primary_key=True)
    )
    name: str = Field(sa_column=Column(VARCHAR(255), nullable=False))
    email: str = Field(sa_column=Column(VARCHAR(255), nullable=False, unique=True))
    roll_number: int = Field(sa_column=Column(Integer, nullable=False, unique=True))
    phone_number: str = Field(sa_column=Column(VARCHAR(15), nullable=True))


class StudentCreate(SQLModel):
    name: str
    email: str
    roll_number: int
    phone_number: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Bilal",
                    "email": "bilalmk@gmail.com",
                    "roll_number": 1,
                    "phone_number": "1",
                }
            ]
        }
    }


class StudentUpdate(SQLModel):
    name: str
    email: str
    roll_number: int
    phone_number: str | None = None


class StudentUpdateField(SQLModel):
    name: str | None = None
    email: str | None = None
    roll_number: int | None = None
    phone_number: str | None = None
