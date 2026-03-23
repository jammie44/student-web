# StudyHub — Python/FastAPI + Next.js + PostgreSQL

Full-stack AI-powered academic platform.

**Stack:** FastAPI · SQLAlchemy · Alembic · PostgreSQL · Next.js 14 · Tailwind CSS

---

## Project Structure

```
studyhub/
├── Procfile                    ← Render start command
├── render.yaml                 ← Render auto-deploy config
├── backend/
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── 0001_initial_schema.py
│   └── app/
│       ├── main.py             ← FastAPI entry point
│       ├── core/
│       │   ├── config.py       ← Settings (reads .env)
│       │   ├── database.py     ← SQLAlchemy engine
│       │   └── security.py     ← JWT + bcrypt
│       ├── models/             ← SQLAlchemy ORM models
│       ├── schemas/            ← Pydantic request/response schemas
│       ├── routes/             ← FastAPI routers
│       └── utils/
│           ├── ai_responses.py ← Mock AI (swap for real API)
│           └── seed.py         ← Database seeder
└── frontend/
    ├── package.json
    ├── next.config.js
    ├── tailwind.config.js
    └── app/
        ├── layout.jsx
        ├── page.jsx            ← Root redirect
        ├── globals.css
        ├── auth/login/page.jsx
        ├── auth/register/page.jsx
        ├── dashboard/page.jsx
        └── admin/page.jsx
```

---

## ── STEP 1: Get a PostgreSQL Database on Render ──────────────────────────

1. Go to https://dashboard.render.com
2. Click **New** → **PostgreSQL**
3. Fill in:
   - Name: `studyhub-db`
   - Database: `studyhub`
   - User: `studyhub_user`
   - Region: Oregon
   - Plan: **Free**
4. Click **Create Database**
5. Wait ~1 minute. On the database page, copy the **Internal Database URL**:
   ```
   postgresql://studyhub_user:PASSWORD@oregon-postgres.render.com/studyhub
   ```

---

## ── STEP 2: Deploy to Render ─────────────────────────────────────────────

### Option A — Blueprint (1-click, recommended)
1. Push this repo to GitHub
2. Render → **New** → **Blueprint** → connect your repo
3. Render reads `render.yaml` and creates the DB + web service automatically
4. Go to the web service → **Environment** tab → no extra vars needed
   (DATABASE_URL is wired automatically from the DB)

### Option B — Manual
1. Create a **Web Service** on Render
2. Set:
   - **Build Command:** `pip install -r backend/requirements.txt && alembic -c backend/alembic.ini upgrade head`
   - **Start Command:** `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120 --chdir backend`
3. Set Environment Variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (paste Internal DB URL from Step 1) |
| `SECRET_KEY` | (click "Generate") |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` |
| `DEBUG` | `false` |
| `FRONTEND_URL` | `*` |

---

## ── STEP 3: How DATABASE_URL connects everything ────────────────────────

```
Render PostgreSQL database
        ↓ "Internal Connection String"
Set as DATABASE_URL env var on web service
        ↓
backend/app/core/config.py reads DATABASE_URL
        ↓  (also fixes postgres:// → postgresql:// automatically)
backend/app/core/database.py creates SQLAlchemy engine
        ↓
Alembic runs: alembic upgrade head  (on every deploy)
        ↓  creates all 4 tables
Your FastAPI app reads/writes PostgreSQL ✅
```

---

## ── Local Development ────────────────────────────────────────────────────

### Backend
```bash
cd backend
cp .env.example .env          # Edit .env — set SECRET_KEY
pip install -r requirements.txt

# Local SQLite (no Postgres needed):
# DATABASE_URL=sqlite:///./studyhub.db  ← already in .env.example

python -m app.utils.seed       # Create demo users
uvicorn app.main:app --reload  # http://localhost:8000
# API docs: http://localhost:8000/api/docs
```

### Frontend
```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev                    # http://localhost:3000
```

---

## ── After First Deploy: Make Yourself Admin ─────────────────────────────

Go to Render → your PostgreSQL database → **Query** tab and run:

```sql
UPDATE users SET is_admin = true WHERE email = 'your@email.com';
```

Or use psql:
```bash
psql "postgresql://studyhub_user:PASSWORD@host/studyhub"
UPDATE users SET is_admin = true WHERE email = 'your@email.com';
```

---

## ── Demo Credentials (after seeding) ───────────────────────────────────

| Role  | Email                    | Password  |
|-------|--------------------------|-----------|
| Admin | admin@studyhub.com       | Admin123  |
| User  | demo@studyhub.com        | Demo1234  |

---

## ── API Endpoints ────────────────────────────────────────────────────────

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register` | — | Register; blocks duplicate emails |
| POST | `/api/auth/login` | — | Login; tracks failed attempts; locks after 5 |
| POST | `/api/auth/logout` | — | Clears session |
| GET | `/api/auth/me` | ✓ | Current user |
| GET | `/api/users/me` | ✓ | Profile + stats |
| PATCH | `/api/users/me` | ✓ | Update name/password |
| GET | `/api/chats` | ✓ | List chats |
| POST | `/api/chats` | ✓ | Create chat |
| GET | `/api/chats/{id}/messages` | ✓ | Get messages |
| POST | `/api/chats/{id}/messages` | ✓ | Send message + AI reply |
| DELETE | `/api/chats/{id}` | ✓ | Delete chat |
| GET | `/api/admin/stats` | Admin | Platform metrics |
| GET | `/api/admin/users` | Admin | Paginated + searchable user list |
| PATCH | `/api/admin/users/{id}/toggle` | Admin | Enable/disable user |
| GET | `/api/admin/subscriptions` | Admin | Subscription list |
| GET | `/api/health` | — | Health check |
| GET | `/api/docs` | — | Swagger UI |

---

## ── Security ─────────────────────────────────────────────────────────────

- **bcrypt** (12 rounds) for all passwords
- **JWT** (7-day expiry) stateless authentication
- **Account lockout** after 5 failed logins (15 min lockout)
- **Password reset hint** after 2 failed attempts
- **CORS** locked to `FRONTEND_URL`
- **Pydantic v2** validation on all inputs
- **Parameterised queries** via SQLAlchemy (no SQL injection)
- **Admin guard** on all /admin routes

---

## ── Add Real AI ──────────────────────────────────────────────────────────

Edit `backend/app/utils/ai_responses.py` — replace `get_ai_response()`:

```python
# With OpenAI:
from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def get_ai_response(tool: str, user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS[tool]},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content
```

Then add `openai` to requirements.txt and set `OPENAI_API_KEY` on Render.
