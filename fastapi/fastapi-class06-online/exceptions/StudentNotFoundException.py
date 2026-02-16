from fastapi import HTTPException, status


class StudentNotFoundException(HTTPException):
    def __init__(self, status_code=status.HTTP_404_NOT_FOUND, detail="student not found"):
        super().__init__(detail=detail, status_code=status_code)
