# JWT Refresh Tokens - Learning Guide

This is an educational guide explaining refresh tokens, short-lived vs long-lived tokens, and auto-refresh — with code examples based on your existing project.

---

## 1. The Problem: Why Do We Need Refresh Tokens?

Right now in your `token_lib.py`, you create a token that expires in **30 minutes**. After 30 minutes, the student is logged out and must enter their email/password again.

**Two bad options without refresh tokens:**
- Make the token last 30 days → **Dangerous**. If someone steals it, they have access for 30 days.
- Keep it at 30 minutes → **Annoying**. Student has to login again every 30 minutes.

**Refresh tokens solve this** by splitting the job into two tokens.

---

## 2. Short-Lived vs Long-Lived Tokens

| | Access Token (Short-Lived) | Refresh Token (Long-Lived) |
|---|---|---|
| **Purpose** | Access protected APIs | Get a new access token |
| **Lifetime** | 15-30 minutes | 7-30 days |
| **Sent with** | Every API request | Only the `/refresh` endpoint |
| **If stolen** | Attacker has 15-30 min of access | More dangerous, but sent rarely |
| **Contains** | User info (email, id, name) | Minimal info (just user id + type) |

**The idea:** The access token is used constantly but dies fast. The refresh token lives long but is only sent to ONE specific endpoint, reducing exposure.

---

## 3. The Complete Flow

```
LOGIN:
  Student sends email + password
       ↓
  Server verifies credentials
       ↓
  Server returns BOTH:
    - access_token  (expires: 30 min)
    - refresh_token (expires: 7 days)

USING APIs:
  Student sends access_token with every request
       ↓
  Server validates token → returns data

WHEN ACCESS TOKEN EXPIRES (after 30 min):
  Student's request fails with 401
       ↓
  Frontend automatically sends refresh_token to /refresh endpoint
       ↓
  Server validates refresh_token
       ↓
  Server returns NEW access_token + NEW refresh_token
       ↓
  Frontend retries the original request with new access_token

WHEN REFRESH TOKEN EXPIRES (after 7 days):
  /refresh endpoint also returns 401
       ↓
  Student must login again with email + password
```

---

## 4. Code Examples (Based on Your Project)

### Step A: Add config setting

In your `config.py`, add one new field:

```python
class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7        # ← NEW

    model_config = SettingsConfigDict(env_file=".env")
```

And in your `.env`:
```
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Step B: Update token_lib.py

Your current `create_token` function works great. You just need to add a **"type" claim** inside the token payload so the server can tell access tokens apart from refresh tokens.

```python
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from config import get_settings

settings = get_settings()

# Create ACCESS token (short-lived, 30 min)
def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {
        "email": data["email"],
        "name": data["name"],
        "id": data["id"],
        "type": "access",            # ← This is how we distinguish tokens
        "exp": expire
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


# Create REFRESH token (long-lived, 7 days)
def create_refresh_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    to_encode = {
        "id": data["id"],            # ← Only minimal info needed
        "type": "refresh",           # ← Marked as refresh token
        "exp": expire
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


# Decode and validate token
def decode_token(token: str, expected_type: str = "access") -> Optional[dict]:
    """
    Decodes a JWT token and checks its type.
    expected_type: "access" or "refresh"
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        # IMPORTANT: Check token type!
        # This prevents someone from using a refresh token as an access token
        if payload.get("type") != expected_type:
            return None

        return payload
    except JWTError:
        return None
```

**Why the `type` claim matters:** Without it, someone could take a refresh token and use it to access protected APIs directly. The `type` check prevents this.

### Step C: Update the Token schema

In your `student_model.py`:

```python
class Token(BaseModel):
    access_token: str
    refresh_token: str          # ← NEW
    token_type: str = "bearer"  # ← NEW (tells frontend to use "Bearer" in headers)
    student: StudentRead
```

### Step D: Update login to return both tokens

In your `student_service.py`, the `login_user` function would change to:

```python
from utilis.token_lib import create_access_token, create_refresh_token

async def login_user(student_login: StudentLogin, session: AsyncSession):
    student = await get_student_login(student_login, session)

    if student is None:
        raise HTTPException(status_code=400, detail="Invalid email address")

    if not verify_password(student_login.password, student.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    student_read = StudentRead.model_validate(student)

    token_data = {
        "email": student.email,
        "name": student.name,
        "id": student.id
    }

    access_token = create_access_token(token_data)    # 30 min
    refresh_token = create_refresh_token(token_data)   # 7 days

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,       # ← NOW returning both
        student=student_read
    )
```

### Step E: Create the refresh endpoint (Auto-Refresh)

This is the key new endpoint. Add this to your `student_route.py`:

```python
from pydantic import BaseModel
from utilis.token_lib import decode_token, create_access_token, create_refresh_token

# Schema for the refresh request
class RefreshRequest(BaseModel):
    refresh_token: str

# Schema for the refresh response (no student data needed)
class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@student_router.post("/refresh", response_model=RefreshResponse)
async def refresh_tokens(request: RefreshRequest, session: AsyncSession = Depends(get_session)):
    """
    Takes a valid refresh token → Returns new access + refresh tokens.
    This is what the frontend calls when the access token expires.
    """

    # 1. Decode the refresh token (note: expected_type="refresh")
    payload = decode_token(request.refresh_token, expected_type="refresh")

    if payload is None:
        # Refresh token is invalid or expired → student must login again
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token. Please login again.")

    # 2. Get fresh student data from database
    #    (in case student was deleted or updated since token was issued)
    student = await get_student(payload["id"], session)

    if student is None:
        raise HTTPException(status_code=401, detail="Student no longer exists")

    # 3. Generate NEW token pair
    token_data = {
        "email": student.email,
        "name": student.name,
        "id": student.id
    }

    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)   # ← Also rotate refresh token!

    return RefreshResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )
```

**Why rotate the refresh token too?** Each time `/refresh` is called, you issue a **new** refresh token and the old one naturally expires. This limits how long any single token is valid.

---

## 5. How the Frontend Handles Auto-Refresh

The "auto" part happens on the **frontend/client side**. Here's the logic:

```
Frontend makes API call with access_token
       ↓
If response is 401 (Unauthorized):
       ↓
  Call POST /student/refresh with refresh_token
       ↓
  If refresh succeeds:
    → Save new tokens
    → Retry the original request
       ↓
  If refresh also fails (401):
    → Redirect to login page
```

In JavaScript/React, this is typically done with an **Axios interceptor**:

```javascript
// Simplified example of auto-refresh on frontend
axios.interceptors.response.use(
  (response) => response,  // success: pass through

  async (error) => {
    if (error.response.status === 401 && !error.config._retry) {
      error.config._retry = true;

      // Try to refresh
      const res = await axios.post("/student/refresh", {
        refresh_token: localStorage.getItem("refresh_token")
      });

      // Save new tokens
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);

      // Retry original request with new access token
      error.config.headers["Authorization"] = `Bearer ${res.data.access_token}`;
      return axios(error.config);
    }

    return Promise.reject(error);
  }
);
```

---

## 6. Summary / Cheat Sheet

```
LOGIN  →  returns access_token (30min) + refresh_token (7days)
    │
    ▼
USE access_token for all API calls (in Authorization header)
    │
    ▼ (after 30 min, access_token expires)
    │
CALL /refresh with refresh_token
    │
    ▼
GET new access_token + new refresh_token
    │
    ▼ (after 7 days, refresh_token expires)
    │
MUST LOGIN AGAIN with email + password
```

**Files you need to modify:**
1. `config.py` → Add `refresh_token_expire_days`
2. `.env` → Add `REFRESH_TOKEN_EXPIRE_DAYS=7`
3. `utilis/token_lib.py` → Split into `create_access_token` + `create_refresh_token`, add type checking
4. `models/student_model.py` → Add `refresh_token` field to `Token` schema
5. `services/student_service.py` → Return both tokens on login
6. `routes/student_route.py` → Add `POST /refresh` endpoint
