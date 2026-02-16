from fastapi import HTTPException, status


class StudentDuplicateException(HTTPException):
    def __init__(self, status_code=status.HTTP_409_CONFLICT, detail="roll number or email is duplicate"):
        super().__init__(detail=detail, status_code=status_code)
