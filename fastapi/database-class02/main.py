from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import create_engine, Session, SQLModel, select, Field
from sqlalchemy.exc import IntegrityError

app = FastAPI()

database_url = "postgresql://neondb_owner:npg_Epj6LHRgFaY0@ep-plain-breeze-a178ieg2-pooler.ap-southeast-1.aws.neon.tech/giaic_student?sslmode=require"
database_client = create_engine(database_url, echo=True)


class Students(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    roll_number: int
    phone_number: str


# def create_table():
#     SQLModel.metadata.create_all(database_client)

# create_table()


def get_config():
    print("config function")
    return {"app_name": "student system", "version": 1}


def get_session():
    with Session(database_client) as session:
        yield session


@app.get("/student")
def get_student_list(session=Depends(get_session)):
    result = session.exec(select(Students)).all()
    return result


@app.get("/student/{student_id}")
def get_student(student_id: int, session=Depends(get_session)):
    result = session.get(Students, student_id)
    if not result:
        raise HTTPException(status_code=404, detail="student not found")
    return result


@app.post("/student")
def post_student(student: Students, session=Depends(get_session)):
    try:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student
    except IntegrityError as ex:
        return {"detail": "roll number or email is duplicate"}


@app.put("/student/{student_id}")
def put_student(student_id: int, student: Students, session=Depends(get_session)):
    try:
        
        db_student = session.get(Students, student_id)
        if not db_student:
            raise HTTPException(status_code=404, detail="student not found")
        
        data_student = student.model_dump(exclude_unset=True)
        
        for key, value in data_student.items():
            setattr(db_student, key, value)
        # if student.name:
        #     db_student.name = student.name
            
        # if student.email:
        #     db_student.email = student.email
            
        # if student.phone_number:
        #     db_student.phone_number = student.phone_number
            
        # if student.roll_number:
        #     db_student.roll_number = student.roll_number
    
        session.add(db_student)
        session.commit()
        session.refresh(db_student)
        return db_student
    except IntegrityError as ex:
        return {"detail": "roll number or email is duplicate"}
