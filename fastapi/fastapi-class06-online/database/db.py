from fastapi import Request
from sqlmodel import Session

def get_session(request: Request):
    try:
        with Session(request.app.state.engine) as session:
            yield session
            session.commit()
    except Exception:
        session.rollback()
        
