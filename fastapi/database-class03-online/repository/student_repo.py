from sqlmodel import Session, select
from database.db import get_session
from models.student_model import Students
from fastapi import Depends


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
