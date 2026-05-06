# KR4 FastAPI

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Check functionality

- GET /health
- GET /errors/a
- GET /errors/b/1
- POST /users/validate
- POST /users

## Database and migrations

1. Copy .env.example to .env and set DATABASE_URL if needed.
2. Apply the initial migration, seed data, then upgrade to head:

```bash
alembic upgrade 20250506_0001
python -m app.seed_initial
alembic upgrade head
```

## Full migration run

```bash
alembic upgrade head
```

## Tests

```bash
pytest -q
```
