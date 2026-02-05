from fastapi import FastAPI, Depends
from database.db import get_session
from models.student_model import (
    StudentCreate,
    StudentUpdate,
    StudentUpdateField,
    Students,
)
from services.student_service import (
    create_student,
    edit_student,
    edit_student_field,
    get_student_by_id,
    get_students,
    remove_student,
)

app = FastAPI()

# def create_table():
#     SQLModel.metadata.create_all(database_client)

# create_table()


@app.get("/student")
def get_student_list(session=Depends(get_session)):
    result = get_students(session)
    return result


@app.get("/student/{student_id}")
def get_student(student_id: int, session=Depends(get_session)):
    result = get_student_by_id(student_id, session)
    return result


@app.post("/student")
def post_student(student: StudentCreate, session=Depends(get_session)):
    result = create_student(student, session)
    return result


@app.put("/student/{student_id}")
def put_student(student_id: int, student: StudentUpdate, session=Depends(get_session)):
    result = edit_student(student_id, student, session)
    return result


@app.patch("/student/{student_id}")
def patch_student(
    student_id: int, student: StudentUpdateField, session=Depends(get_session)
):
    result = edit_student_field(student_id, student, session)
    return result


@app.delete("/student/{student_id}")
def delete_student(student_id: int, session=Depends(get_session)):
    result = remove_student(student_id, session)
    return result
