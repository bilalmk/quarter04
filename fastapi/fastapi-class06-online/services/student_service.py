from datetime import timedelta

from fastapi import HTTPException
from sqlmodel import Session, select
from exceptions.StudentDuplicateException import StudentDuplicateException
from exceptions.StudentNotFoundException import StudentNotFoundException
from models.student_model import (
    StudentLogin,
    StudentRead,
    StudentUpdate,
    Students,
    StudentUpdateField,
    StudentCreate,
)
from sqlalchemy.exc import IntegrityError


from repository.student_repo import (
    delete_student,
    get_student_email,
    get_student_login,
    update_student,
    get_student,
    insert_student,
    get_student_list,
)
from utilis.hash_lib import hash_password, verify_password
from utilis.token_lib import create_token


def login_user(login_data: StudentLogin, session: Session):
    db_user = get_student_login(login_data.model_dump(), session)

    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid email address")

    if not verify_password(login_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    # user_data = StudentRead(**db_user.model_dump())

    token = create_token(
        {"email": db_user.email, "name": db_user.name, "id": db_user.id}
    )

    return {"access_token": token, "student": db_user}


def get_student_by_email(email: str, session: Session):
    result = get_student_email(email, session)
    if not result:
        raise StudentNotFoundException()
    return result


def get_students(session: Session):
    result = get_student_list(session)
    return result


def get_student_by_id(student_id: int, session: Session):
    result = get_student(student_id, session)
    if not result:
        raise StudentNotFoundException()
    return result


def create_student(student: StudentCreate, session: Session):
    try:
        student_data = Students(**student.model_dump())
        student_data.password = hash_password(student_data.password)
        student_data = insert_student(student_data, session)
        return student_data
    except IntegrityError as ex:
        raise StudentDuplicateException()


def edit_student(student_id: int, student: StudentUpdate, session: Session):
    try:
        db_student = get_student(student_id, session)
        if not db_student:
            raise StudentNotFoundException()

        data_student = student.model_dump()

        for key, value in data_student.items():
            setattr(db_student, key, value)

        db_student = update_student(db_student, session)
        return db_student
    except IntegrityError as ex:
        raise StudentDuplicateException()


def edit_student_field(student_id: int, student: StudentUpdateField, session: Session):
    try:
        db_student = get_student(student_id, session)
        if not db_student:
            raise StudentNotFoundException()

        data_student = student.model_dump(exclude_unset=True)

        for key, value in data_student.items():
            setattr(db_student, key, value)

        db_student = update_student(db_student, session)
        return db_student
    except IntegrityError as ex:
        raise StudentDuplicateException()


def remove_student(student_id, session: Session):
    try:
        db_student = get_student(student_id, session)
        if not db_student:
            raise StudentNotFoundException()
        delete_student(db_student, session)
        return f"student {db_student.name} deleted"
    except StudentNotFoundException as ex:
        raise ex
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail="Error in delete operation, please try again",
        )
