from fastapi import Depends, APIRouter, HTTPException

from database.db import get_session

from services.student_service import (
    create_student,
    edit_student,
    edit_student_field,
    get_student_by_id,
    get_students,
    login_user,
    remove_student,
)

from models.student_model import (
    StudentCreate,
    StudentLogin,
    StudentRead,
    StudentUpdate,
    StudentUpdateField,
    Students,
    Token,
)
from utilis.deps import get_authorization, verify_self

router = APIRouter(prefix="/student", dependencies=[Depends(verify_self)])
public_router = APIRouter(prefix="/student")


@public_router.post("/login", response_model=Token)
def get_student_login(login_data: StudentLogin, session=Depends(get_session)):
    result = login_user(login_data, session)
    return result


@router.get("", response_model=list[StudentRead])
def get_student_list(
    session=Depends(get_session), authorize_student=Depends(verify_self)
):
    if authorize_student.role == "admin":
        result = get_students(session)
        return result
    return [authorize_student]


@router.get("/{student_id}", response_model=StudentRead)
def get_student(
    student_id: int,
    session=Depends(get_session)
):
    result = get_student_by_id(student_id, session)
    return result


@public_router.post("", response_model=StudentRead)
def post_student(student: StudentCreate, session=Depends(get_session)):
    result = create_student(student, session)
    return result


@router.put("/{student_id}", response_model=StudentRead)
def put_student(
    student_id: int,
    student: StudentUpdate,
    session=Depends(get_session)
):
    result = edit_student(student_id, student, session)
    return result


@router.patch("/{student_id}", response_model=StudentRead)
def patch_student(
    student_id: int,
    student: StudentUpdateField,
    session=Depends(get_session),
):
    result = edit_student_field(student_id, student, session)
    return result


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    session=Depends(get_session)
):
    result = remove_student(student_id, session)
    return result
