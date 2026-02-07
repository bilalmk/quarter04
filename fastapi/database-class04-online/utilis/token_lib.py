from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from config import get_settings

settings = get_settings()

def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        return None


# token = create_token({"email": "bilalmk@gmail.com", "id": 1}, timedelta(seconds=40))
# print(token)
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJpbGFsbWtAZ21haWwuY29tIiwiaWQiOjEsImV4cCI6MTc3MDM5Nzk2NX0.38p_D2kF0sLlDaqIH7uy6C_B34FgIupQv61_7idDI6k"
# print(decode_token(token))
