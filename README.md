# Books API

A small REST API for managing books, built with FastAPI and SQLModel and backed by SQLite.

The code is split into layers so each one has a single job:

| File | Responsibility |
|---|---|
| `src/books_api/main.py` | Creates the app, sets up tables on startup, maps errors to HTTP responses |
| `src/books_api/router.py` | HTTP routes and dependency wiring |
| `src/books_api/service.py` | Business rules |
| `src/books_api/repository.py` | Database queries |
| `src/books_api/models.py` | Table and request schemas |
| `src/books_api/database.py` | Engine and session setup |
| `src/books_api/exceptions.py` | Domain errors |

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/harshtandon6062/books-api.git
cd books-api
uv sync
```

## Run

Run from the project root:

```bash
uv run uvicorn books_api.main:app --reload
```

The API runs at <http://127.0.0.1:8000>, with interactive docs at <http://127.0.0.1:8000/docs>. A `books.db` SQLite file is created in the directory you start the server from.

## Endpoints

| Method | Path | Description | Success |
|---|---|---|---|
| `POST` | `/books` | Create a book | `201` |
| `GET` | `/books?offset=0&limit=10` | List books (`limit` is 1 to 100) | `200` |
| `GET` | `/books/{book_id}` | Get one book | `200` |
| `PATCH` | `/books/{book_id}` | Update only the fields you send | `200` |
| `DELETE` | `/books/{book_id}` | Delete a book | `204` |

Errors: `404` if the book doesn't exist, `409` for a duplicate book, and `422` for invalid input.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Dune", "author": "Frank Herbert", "year": 1965}'
```

## Tests

Run from the project root:

```bash
uv run pytest
```
