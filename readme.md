# Backend Developer Intern Assignment — Primetrade.ai

## Stack
- Backend: Django + Django REST Framework
- Auth: JWT (SimpleJWT)
- Database: SQLite (dev) / PostgreSQL (prod)
- Frontend: Vanilla JS + HTML/CSS
- Docs: Swagger (drf-spectacular)

## Setup

```bash
git clone https://github.com/yourname/backend_assignment
cd backend_assignment
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Fill in SECRET_KEY
python manage.py migrate
python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/v1/auth/register/ | None | Register user |
| POST | /api/v1/auth/login/ | None | Login → JWT |
| POST | /api/v1/auth/refresh/ | Refresh token | Refresh access token |
| GET  | /api/v1/auth/me/ | Bearer | Current user |
| GET  | /api/v1/tasks/ | Bearer | List tasks |
| POST | /api/v1/tasks/ | Bearer | Create task |
| GET  | /api/v1/tasks/:id/ | Bearer | Get task |
| PATCH| /api/v1/tasks/:id/ | Bearer | Update task |
| DELETE | /api/v1/tasks/:id/ | Bearer | Delete task |

## Swagger Docs
Visit: http://localhost:8000/api/docs/

## Frontend
Open `frontend/index.html` in browser.
Make sure Django server is running on port 8000.

## Database Schema
See `schema.sql` or Django's admin at `/admin/`.