# Expense Tracker API

A REST API built with **FastAPI** for tracking personal expenses, with user accounts and JWT-based authentication. Each user can only see and manage their own expenses.

Built as a learning project to practice backend fundamentals: databases, password security, JWT authentication, and full CRUD operations.

Project brief: [roadmap.sh/projects/expense-tracker-api](https://roadmap.sh/projects/expense-tracker-api)

## Features

- Sign up and log in (passwords hashed with Argon2, never stored in plain text)
- JWT-based authentication — protected endpoints require a valid token
- Add, view, update, and delete expenses
- Each expense is tied to its owner — users can only access their own data
- Filter expenses by: past week, past month, last 3 months, or a custom date range

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — Python web framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM / database toolkit
- [SQLite](https://www.sqlite.org/) — lightweight file-based database
- [pwdlib](https://frankie567.github.io/pwdlib/) (Argon2) — password hashing
- [PyJWT](https://pyjwt.readthedocs.io/) — JSON Web Token creation and verification

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/expense-tracker-api.git
cd expense-tracker-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your environment variables

Copy the example env file and fill in your own secret key:

```bash
cp .env.example .env
```

Then open `.env` and replace the placeholder with your own random string, e.g.:

```
SECRET_KEY=some-long-random-string-only-you-know
```

This key is used to sign and verify JWTs — it should never be committed to GitHub (`.env` is already excluded via `.gitignore`).

### 4. Run the server

```bash
uvicorn main:app --reload
```

### 5. Try it out

Open your browser at:

```
http://127.0.0.1:8000/docs
```

This interactive page lets you test every endpoint, including authenticating with a token via the "Authorize" button.

## Endpoints

| Method | Path | Auth required? | Description |
|---|---|---|---|
| GET | `/` | No | Welcome message |
| POST | `/signup` | No | Create a new user account |
| POST | `/login` | No | Log in, returns a JWT access token |
| GET | `/profile` | Yes | Returns the logged-in user's username |
| POST | `/expenses` | Yes | Add a new expense |
| GET | `/expenses` | Yes | List your expenses, with optional `filter` |
| GET | `/expenses/{id}` | Yes | Get one of your expenses by ID |
| PUT | `/expenses/{id}` | Yes | Update one of your expenses |
| DELETE | `/expenses/{id}` | Yes | Delete one of your expenses |

### Filtering expenses

`GET /expenses` accepts an optional `filter` query parameter:

- `?filter=week` — expenses from the past 7 days
- `?filter=month` — expenses from the past 30 days
- `?filter=3months` — expenses from the past 90 days
- `?filter=custom&start_date=2026-01-01&end_date=2026-06-01` — a custom date range

### Example: Sign up

**Request:** `POST /signup`

```json
{
  "username": "samiullah",
  "password": "yourpassword"
}
```

### Example: Log in

**Request:** `POST /login`

```json
{
  "username": "samiullah",
  "password": "yourpassword"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Use this token in the `Authorization` header (`Bearer <token>`) for every request to a protected endpoint.

### Example: Add an expense

**Request:** `POST /expenses` (requires a valid token)

```json
{
  "title": "Groceries run",
  "amount": 45.99,
  "category": "Groceries",
  "date": "2026-10-01"
}
```

## What I Learned

- Why temporary (in-memory) storage isn't enough, and how to use a real database (SQLite + SQLAlchemy)
- Why passwords should never be stored directly — hashing with Argon2
- What a JWT is, how it's structured, and why it's signed but not encrypted
- How to protect endpoints so only authenticated users can access them
- How to scope data per-user, so one user can never see or modify another's data
- Building date-based filters using `timedelta`

## Known Limitations / Possible Next Steps

- No token refresh mechanism — tokens simply expire after 30 minutes and the user must log in again
- No input validation beyond basic type checking (e.g. no check for duplicate usernames at signup, no minimum password length)
- Uses SQLite, which is fine for learning but a real production app would likely use PostgreSQL or similar
