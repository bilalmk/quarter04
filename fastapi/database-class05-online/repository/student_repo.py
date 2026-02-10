from sqlmodel import Session, select
from database.db import get_session
from models.student_model import Students
from fastapi import Depends


def get_student_login(login_data: dict, session: Session):
    student = session.exec(select(Students).where(Students.email == login_data["email"])).first()
    return student

def get_student_email(email:str, session: Session):
    student = session.exec(select(Students).where(Students.email == email)).first()
    return student

def get_student(student_id: int, session: Session):
    student = session.get(Students, student_id)
    return student


def get_student_list(session: Session):
    result = session.exec(select(Students)).all()
    return result


def insert_student(student: Students, session: Session):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def update_student(student: Students, session: Session):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


def delete_student(student: Students, session: Session):
    session.delete(student)
    session.commit()
