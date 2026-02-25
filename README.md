# 🏋️ Gym Performance SaaS API

A production-ready REST API for tracking gym workouts and performance analytics. Built with FastAPI and PostgreSQL.

## 🔗 Live API
**Base URL:** https://gym-fastapi-production.up.railway.app

**Interactive Docs:** https://gym-fastapi-production.up.railway.app/docs

## 🛠️ Tech Stack
- **FastAPI** — Python web framework
- **PostgreSQL** — Production database
- **SQLAlchemy** — ORM
- **JWT** — Authentication (access + refresh tokens)
- **Railway** — Cloud deployment

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /register | Create new account | ❌ |
| POST | /login | Login and get JWT token | ❌ |
| GET | /me | Get current user | ✅ |
| POST | /refresh | Refresh access token | ❌ |
| POST | /logout | Logout and invalidate token | ✅ |

### Workouts
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /workouts | Log a new workout | ✅ |
| GET | /workouts | Get all your workouts | ✅ |
| GET | /workouts/{id} | Get single workout | ✅ |
| DELETE | /workouts/{id} | Delete a workout | ✅ |
| GET | /workouts/analytics | Get performance analytics | ✅ |

## 📊 Analytics Response
```json
{
    "total_workouts": 3,
    "total_volume_kg": 17560.0,
    "most_trained_exercise": "Bench Press",
    "personal_records": {
        "Bench Press": 80.0,
        "Squat": 100.0
    }
}
```

## 🚀 Run Locally
```bash
git clone https://github.com/deepinder-gill/GYM-FASTAPI
cd GYM-FASTAPI/app
pip install -r requirements.txt
uvicorn main:app --reload
```

## 👤 Author
**Deepinder Singh Gill** — [GitHub](https://github.com/deepinder-gill)
