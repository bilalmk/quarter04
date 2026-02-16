from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from database.db import get_session
from services.student_service import get_student_by_email
from utilis.token_lib import decode_token

oauth = OAuth2PasswordBearer(tokenUrl="/student/login")


def get_authorization(token=Depends(oauth), session=Depends(get_session)):
    # print("authorization function")
    # token = request.headers.get("authorization")
    # print(f"\n\n token={token}\n\n")
    exception = HTTPException(status_code=403, detail="invalid credentials")

    # if token is None:
    #     raise exception
    # token = token[7:]

    payload = decode_token(token)

    if payload is None:
        raise exception

    email = payload.get("email")
    if email is None:
        raise exception

    authorize_student = get_student_by_email(email, session)
    return authorize_student


def verify_self(student_id: int = 0, authorize_student=Depends(get_authorization)):
    if authorize_student.role == "admin":
        return authorize_student

    if student_id > 0 and student_id != authorize_student.id:
        raise HTTPException(status_code=403, detail="You can only access your own data")
    return authorize_student
