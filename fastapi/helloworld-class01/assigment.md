# Build a simple TODO CRUD API (in-memory) with validations

## Objective
Create a FastAPI app that manages TODO items using only in-memory storage (no database, no files). Implement full CRUD, meaningful validations,Error handling and clear error responses.

## Deliverables
- `main.py` (or similar) with the FastAPI app.
- In-memory data store (list/dict) with auto-incrementing integer IDs.
- Pydantic models for request/response shapes and validation.


## Required endpoints
- `GET /` : return a small health message.
- `POST /todos` : create a todo; return 201 with the created item (including generated `id`).
- `GET /todos` : list all todos.
- `GET /todos/{todo_id}` : return a single todo; 404 if not found.
- `PUT /todos/{todo_id}` : replace an existing todo; 404 if not found.
- `PATCH /todos/{todo_id}` : partial update (any subset of fields); 404 if not found.
- `DELETE /todos/{todo_id}` : delete; return 204 or a success message; 404 if not found.
- Bonus: `PATCH /todos/{todo_id}/toggle` to flip the `completed` status.

## Data model & validation rules
- `id`: int, auto-generated, unique.
- `title`: required, trimmed, non-empty, max 100 characters.
- `description`: optional, max 500 characters.
- `due_date`: optional ISO 8601 datetime string; if provided, it must be today or in the future.
- `priority`: optional int 1-5, default 3.
- `completed`: bool, default `false`.
- Reject requests that violate validation with proper error messages.

## Behavior expectations
- IDs should start at 1 and increment per new todo; ensure update/delete only affects the matching ID.
- Keep state in memory; restarting the server resets the data.
- Use HTTP status codes correctly (201 for create, 200 for reads/updates, 204 for delete, 400/422 for validation, 404 for missing records).
- Responses should always be JSON and include the current todo representation when applicable.


## Exception handling requirements
- Use `HTTPException` with meaningful `detail` messages for 404s and bad input you catch manually (e.g., past `due_date`).
- Ensure unhandled errors are not exposed; return a simple JSON error message and status 500 for unexpected failures.

## Testing manually
- Run locally: `uv run uvicorn main:app --reload` (or your chosen filename).