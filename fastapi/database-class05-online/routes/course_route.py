from fastapi import Depends, APIRouter

from database.db import get_session
from models.course_model import Course, CourseCreate
from utilis.deps import get_authorization
from utilis.token_lib import decode_token

router = APIRouter(prefix="/course", dependencies=[Depends(get_authorization)])

@router.get("")
def get_courses(session=Depends(get_session)):
    return ["python", "nextjs"]


@router.get("/{course_id}")
def get_course(
    course_id: int, session=Depends(get_session)
):
    return "python"


@router.post("")
def post_course(course: CourseCreate, session=Depends(get_session)):
    return "course created"


@router.put("/{course_id}")
def put_course(course_id: int, course: CourseCreate, session=Depends(get_session)):
    return "course updated"


@router.delete("/{course_id}")
def delete_course(course_id: int, session=Depends(get_session)):
    return "course deleted"
