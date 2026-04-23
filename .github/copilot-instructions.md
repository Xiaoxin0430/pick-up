# Project Guidelines

## Architecture
- This workspace is a note app with separated backend and frontend.
- Backend runtime source of truth is the root-level Python app:
  - `main.py`: FastAPI app bootstrap and router mounting.
  - `routers/`: API endpoints only (request parsing, response shaping).
  - `crud/`: database access and persistence logic.
  - `models/`: SQLAlchemy ORM models.
  - `schemas/`: Pydantic request/response models.
  - `config/`: database/session setup.
  - `utils/`: shared helpers (response/security).
- Frontend is in `项目物料/03-前端项目代码/xwzx-note/` (Vue 3 + Vite + Vant).

## Build and Run
- Python version: 3.10+ recommended.
- Backend install:
  - `pip install -r 代码/toutiao_backend/requirements.txt`
- Backend run (from workspace root):
  - `uvicorn main:app --reload`
- Frontend install/run (from `项目物料/03-前端项目代码/xwzx-note/`):
  - `npm install`
  - `npm run dev`
  - `npm run build`
- There is no formal automated test suite in this workspace right now.
- For backend API smoke testing, use `test_main.http`.

## Conventions
- Keep FastAPI endpoint handlers in `routers/` thin; move DB/business logic to `crud/`.
- Use async database access patterns with `AsyncSession` and `await` consistently.
- Keep request/response contracts in `schemas/`, not inline in routers.
- Response payloads should follow the project shape:
  - `{"code": 200, "message": "...", "data": ...}`
- For password handling, use helpers in `utils/security.py`; never store plain text passwords.

## Environment and Pitfalls
- Database URL is loaded from `./static/.env` via `config/db_config.py`.
- Ensure `ASYNC_DATABASE_URL` exists and uses async driver format (for example, `mysql+aiomysql://...`).
- The workspace contains another similar backend tree under `代码/toutiao_backend/`; prefer editing root-level backend files unless explicitly targeting that copy.
- Keep frontend API base URL aligned with backend port/settings in `项目物料/03-前端项目代码/xwzx-note/src/config/api.js`.
