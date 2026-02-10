from dotenv import load_dotenv
import os
from sqlmodel import create_engine, Session

load_dotenv()

database_url = os.getenv("DATABASE_URL")
database_client = create_engine(str(database_url), echo=False)


def get_session():
    with Session(database_client) as session:
        yield session
