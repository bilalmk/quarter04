from fastapi import FastAPI, Request, Response
from sqlmodel import SQLModel
from routes.student_route import router as student_router
from routes.student_route import public_router as student_public_router
from routes.course_route import router as course_router
from fastapi.responses import JSONResponse
from database.db import database_client

app = FastAPI()
app.include_router(student_public_router)
app.include_router(student_router)
app.include_router(course_router)


# @app.middleware("http")
# async def test_middleware(request: Request, call_next) -> Response:
#     api_key = request.headers.get("X-API-KEY")
#     if api_key is None:
#         return JSONResponse(status_code=401, content={"detail": "API key is missing"})

#     if api_key != "123":
#         return JSONResponse(status_code=401, content={"detail": "API key is invalid"})

#     response: Response = await call_next(request)
#     response.headers["app_information"] = "Student System"
#     return response


@app.get("/health")
def get_health():
    return "Server is running"


def create_table():
    SQLModel.metadata.create_all(database_client)


#create_table()