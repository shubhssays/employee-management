# Employee Management SaaS

A lightweight multi-tenant SaaS for **work tracking**, **attendance**, and **leave management** — built with FastAPI, PostgreSQL, and SQLAlchemy (async).

## Quick Start

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker + Docker Compose (for local PostgreSQL)

### 1. Clone and set up the environment

```bash
# Install dependencies
uv sync --all-extras

# Copy environment template
cp .env.example .env
# Edit .env with your local values
```

### 2. Start PostgreSQL (Docker)

```bash
docker compose up -d db
```

### 3. Apply migrations

```bash
uv run alembic upgrade head
```

### 4. Start the development server

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit:
- **API docs:** http://localhost:8000/api/v1/docs
- **Health check:** http://localhost:8000/api/v1/health

---

## Project Structure

```
employee-management/
├── app/
│   ├── main.py              # FastAPI application factory
│   ├── core/                # Config, security, dependencies, logging, exceptions
│   ├── db/                  # Database engine, session, base model
│   ├── shared/              # Cross-module schemas and utilities
│   └── modules/             # Business domain modules
│       ├── organization/
│       ├── auth/
│       ├── employees/
│       ├── work_tracker/
│       ├── attendance/
│       ├── leave/
│       └── dashboard/
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── security/
├── alembic/                 # Database migrations
├── docs/                    # Architecture and product documentation
└── scripts/                 # Development utilities
```

## Module Dependency Order

```
Organization → Auth → Employees → Work Tracker
                                → Attendance ← Leave
                                              ↓
                                          Dashboard
```

## Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=app --cov-report=term-missing

# Specific module
uv run pytest tests/integration/test_health.py -v
```

## Database Migrations

```bash
# Create a new migration after changing a model
uv run alembic revision --autogenerate -m "describe_what_changed"

# Apply all pending migrations
uv run alembic upgrade head

# Roll back one migration
uv run alembic downgrade -1

# Check current state
uv run alembic current
```

## Adding a New Module

1. Create `app/modules/<module_name>/` with: `__init__.py`, `models.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`, `exceptions.py`
2. Import the ORM model in `app/db/base.py` (for Alembic discovery)
3. Register the router in `app/api/v1/router.py`
4. Write migrations: `uv run alembic revision --autogenerate -m "add_<module_name>_tables"`

## Architecture Documentation

- [Product Specification](docs/product-spec.md)
- [Technical Blueprint](docs/technical-blueprint.md)
