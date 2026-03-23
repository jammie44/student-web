# StudyHub — FastAPI + PostgreSQL + Next.js

## ⚡ IMPORTANT — Repository Structure

The `app/` folder is at the **repo root**. There is NO `backend/` subdirectory.
Render's build command runs from the repo root directly.

```
repo-root/                     ← everything lives here
├── Procfile
├── render.yaml
├── requirements.txt
├── alembic.ini
├── .env.example
├── alembic/
│   └── versions/
│       └── 0001_initial_schema.py
├── app/                       ← FastAPI application
│   ├── main.py
│   ├── core/  (config, database, security)
│   ├── models/ (User, Subscription, Chat, Message)
│   ├── routes/ (auth, users, chat, admin, billing)
│   ├── schemas/ (Pydantic models)
│   └── utils/ (AI responses, seed)
└── frontend/                  ← Next.js application
    └── app/ components/ lib/ hooks/
```

---

## Deploy to Render (Step by Step)

### Step 1 — Create PostgreSQL Database
1. Go to https://dashboard.render.com
2. Click **New** → **PostgreSQL**
3. Name: `studyhub-db`, Plan: **Free**, Region: Oregon
4. Click **Create Database** and wait ~1 minute
5. From the database page, copy the **Internal Database URL**

### Step 2 — Create Web Service
1. Render → **New** → **Web Service**
2. Connect your GitHub repo
3. Set these exactly:
   - **Root Directory:** *(leave blank — repo root)*
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt && alembic upgrade head`
   - **Start Command:** `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120`

### Step 3 — Set Environment Variables
| Key | Value |
|-----|-------|
| `DATABASE_URL` | Paste Internal DB URL from Step 1 |
| `SECRET_KEY` | Click "Generate" |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` |
| `DEBUG` | `false` |
| `FRONTEND_URL` | `*` |

### Step 4 — Deploy
Click **Create Web Service**. First deploy takes ~3 minutes.
Visit: `https://your-service.onrender.com/api/health`

---

## OR: Use render.yaml (Blueprint — 1 click)
1. Push repo to GitHub
2. Render → **New** → **Blueprint** → connect repo
3. Render reads render.yaml automatically
4. Add `OPENAI_API_KEY` if needed after creation

---

## After First Deploy — Make Yourself Admin
Go to Render → PostgreSQL → **Query** tab:
```sql
UPDATE users SET is_admin = true WHERE email = 'your@email.com';
```

---

## Local Development

```bash
# Backend (from repo root)
cp .env.example .env          # Edit .env
pip install -r requirements.txt
python -m app.utils.seed       # Creates demo users
uvicorn app.main:app --reload  # http://localhost:8000/api/docs

# Frontend (separate terminal)
cd frontend
cp .env.local.example .env.local
npm install
npm run dev                    # http://localhost:3000
```

Demo credentials: `demo@studyhub.com` / `Demo1234`
Admin credentials: `admin@studyhub.com` / `Admin123`
