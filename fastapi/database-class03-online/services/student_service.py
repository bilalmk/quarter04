from fastapi import HTTPException
from sqlmodel import Session
from exceptions.StudentDuplicateException import StudentDuplicateException
from exceptions.StudentNotFoundException import StudentNotFoundException
from models.student_model import (
    StudentUpdate,
    Students,
    StudentUpdateField,
    StudentCreate,
)
from sqlalchemy.exc import IntegrityError


from repository.student_repo import (
    delete_student,
    update_student,
    get_student,
    insert_student,
    get_student_list,
)


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
