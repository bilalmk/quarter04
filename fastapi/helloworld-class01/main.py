from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class StudentOut(BaseModel):
    roll_number: str
    name: str
    email: EmailStr | None = None


class Student(BaseModel):
    roll_number: str
    name: str = Field(min_length=1, max_length=10)
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "roll_number": "1",
                    "name": "Bilal",
                    "email": "bilalmk@gmail.com",
                    "password": "123",
                }
            ]
        }
    }


student_db = {}


@app.post("/student")
def insert_student(student: Student) -> str:
    student_db[student.roll_number] = student
    return "record created"


@app.get("/student")
def get_student():
    return student_db


@app.get("/student/{roll_number}", response_model=StudentOut)
def get_student_by_rollnumber(roll_number: str) -> StudentOut:
    try:
        return student_db[roll_number]
    except Exception as ex:
        raise HTTPException(status_code=200, detail="invalid roll number")


@app.put("/student/{roll_number}")
def update_student(roll_number, std: Student):
    student_db[roll_number] = std
    return "student updated"


@app.delete("/student/{roll_number}")
def delete_student(roll_number):
    student_db.pop(roll_number)
    return "student deleted"


# http://localhost:8000/student

# http://localhost:8000/student/create
# http://localhost:8000/student/update
# http://localhost:8000/student/delete
