from fastapi import FastAPI, Request, Response, BackgroundTasks
from sqlmodel import SQLModel, create_engine
from models.student_model import StudentCreate
from routes.student_route import router as student_router
from routes.student_route import public_router as student_public_router
from routes.course_route import router as course_router
from contextlib import asynccontextmanager
from config import get_settings

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handlers=[logging.FileHandler("app.log")],
)
logger = logging.getLogger(__name__)


def create_table(database_client):
    SQLModel.metadata.create_all(database_client)


@asynccontextmanager
async def fastapi_life_span(app):
    settings = get_settings()
    database_client = create_engine(str(settings.database_url), echo=False)
    app.state.engine = database_client
    create_table(database_client)
    app.state.config = {"appname": "student information"}
    yield
    database_client.dispose()
    logger.info("application stopped")


app = FastAPI(lifespan=fastapi_life_span)

app.include_router(student_public_router)
app.include_router(student_router)
app.include_router(course_router)


@app.middleware("http")
def get_logs(request: Request, call_next) -> Response:
    logger.info(f"{request.method} - {request.url}")
    response = call_next(request)
    return response


@app.get("/health")
# @limiter.limit("4/minute")
def get_health(request: Request):
    # logger.info(f"{request.method} - {request.url}")
    # print("Server is running")
    return "Server is running"


@app.get("/hello")
# @limiter.limit("2/minute")
def get_hello(request: Request):
    try:
        # logger.info("hello from fastapi")
        # logger.info(f"{request.method} - {request.url}")
        a = 10 / 0
        return "hello from fastapi"
    except Exception as ex:
        logger.error(ex)


import time


def send_email():
    print("start sending email....")
    time.sleep(12)
    print("email sent successfully...")


@app.post("/register")
def register(student: StudentCreate, task: BackgroundTasks):
    print("student register successfully...")
    task.add_task(send_email)
    return {"message": "student register successfully"}


# @app.on_event("startup")
# def start():
#     print("application started")

# @app.on_event("shutdown")
# def stop():
#     print("application stopped")

# from slowapi import _rate_limit_exceeded_handler, Limiter
# from slowapi.errors import RateLimitExceeded
# from slowapi.util import get_remote_address
# from slowapi.middleware import SlowAPIMiddleware

# from utilis.rate_limit import _custom_rate_limit_exceeded_handler, limiter

# app.add_exception_handler(RateLimitExceeded, _custom_rate_limit_exceeded_handler)
# app.add_middleware(SlowAPIMiddleware)

# app.state.limiter = limiter

# create_table()

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
