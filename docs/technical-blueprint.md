# Employee Management SaaS — Professional FastAPI Technical Blueprint

**Version:** 1.0  
**Status:** Architecture Definition — Approved for Implementation  
**Product Spec Reference:** [product-spec.md](file:///Users/shubhs/Desktop/shubhs/Developer/github/personal_projects/employee-management/docs/product-spec.md)  
**Last Updated:** 2026-08-31  
**Audience:** Principal Engineer, Senior FastAPI Developer, AI Coding Agent

> This document is the single authoritative technical blueprint for implementing the Employee Management SaaS MVP using Python, FastAPI, and PostgreSQL. It does not contain implementation code. It is designed to be handed directly to a senior FastAPI developer or AI coding agent to execute in a controlled sequence.

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Architecture](#3-architecture)
4. [Proposed Project Structure](#4-proposed-project-structure)
5. [Module Architecture](#5-module-architecture)
6. [Multi-Tenant SaaS Architecture](#6-multi-tenant-saas-architecture)
7. [Authentication & Authorization](#7-authentication--authorization)
8. [PostgreSQL Database Architecture](#8-postgresql-database-architecture)
9. [Database Entity Overview](#9-database-entity-overview)
10. [API Architecture](#10-api-architecture)
11. [API Documentation Structure](#11-api-documentation-structure)
12. [API Request/Response Design](#12-api-requestresponse-design)
13. [Error Handling Strategy](#13-error-handling-strategy)
14. [Service & Repository Architecture](#14-service--repository-architecture)
15. [Cross-Module Dependencies](#15-cross-module-dependencies)
16. [Background Jobs](#16-background-jobs)
17. [Configuration Management](#17-configuration-management)
18. [Logging & Observability](#18-logging--observability)
19. [Security Architecture](#19-security-architecture)
20. [Testing Architecture](#20-testing-architecture)
21. [API Versioning & Backward Compatibility](#21-api-versioning--backward-compatibility)
22. [Migration Strategy](#22-migration-strategy)
23. [Development Workflow](#23-development-workflow)
24. [MVP vs Future Architecture](#24-mvp-vs-future-architecture)
25. [Production Readiness Checklist](#25-production-readiness-checklist)
26. [Recommended Implementation Sequence](#26-recommended-implementation-sequence)
27. [Final Architecture Summary](#27-final-architecture-summary)

---

# 1. Project Overview

## 1.1 Project Purpose

**Employee Management SaaS** is a lightweight, multi-tenant web application that gives small and medium-sized companies operational visibility into their workforce — specifically around **daily work tracking**, **attendance**, and **leave management** — without the overhead of a full HRMS platform.

## 1.2 Problem Being Solved

Growing teams between 10–500 employees face three tightly coupled pain points:

1. **Who worked on what?** — Work attribution is scattered across chat, email, and verbal updates.
2. **Who is present or absent today?** — Attendance is tracked in spreadsheets or not at all.
3. **How much leave does an employee have?** — Leave balances are manually maintained and error-prone.

This product eliminates those three pain points in one cohesive tool, purpose-built for the SMB operational context.

## 1.3 Target Users

| Role | Description |
|------|-------------|
| **Organization Admin** | Creates the organization; configures leave policy; manages employees |
| **Manager** | Oversees a team; approves leave; reviews work and attendance |
| **Employee** | Logs work; checks in/out; requests leave; views own records |

## 1.4 SaaS Nature

- Each **organization** is a fully isolated tenant.
- All data is scoped to an organization — no cross-tenant access is possible.
- The platform is shared infrastructure (shared database, shared application) with logical tenant isolation.
- Billing and subscription management is **explicitly deferred** to Post-MVP.

## 1.5 Core MVP Capabilities

1. Organization registration (self-service onboarding)
2. Employee management (create, profile, manager assignment, deactivation)
3. Role-based access control (Admin / Manager / Employee — three fixed roles)
4. Daily work entry logging and review
5. Daily attendance check-in / check-out with automatic absence marking
6. Leave policy configuration and automatic leave allocation
7. Leave request workflow (submit → approve / reject)
8. Manager direct grant of leave
9. Leave status reflected automatically in attendance records
10. Role-scoped dashboard summaries

## 1.6 Future Extensibility

The MVP architecture is intentionally designed so the following can be added without rewriting the foundation:

- Carry-forward of leave balances at year end
- Holiday calendar
- Shift management
- Payroll integration hooks
- Bulk employee import
- Enterprise SSO (SAML/OIDC)
- Advanced analytics and reporting
- Email/Slack/Webhook notification integrations

## 1.7 Architecture Philosophy

**Modular Monolith first.** The system is structured as a single deployable FastAPI application organized into clear, bounded domain modules. Each module owns its own models, repositories, services, and schemas. Modules communicate through explicit service calls — never through direct database cross-joins across module boundaries.

This approach:
- Enables a small team to ship quickly
- Keeps the codebase navigable without microservices overhead
- Makes it straightforward to extract individual modules into services later if needed

## 1.8 MVP Scope Boundaries

**In scope:** Organization, Auth, Employee, Work Tracker, Attendance, Leave, Dashboard  
**Out of scope:** Payroll, Recruitment, Performance Management, Appraisals, Biometrics, GPS, AI, Integrations, Advanced Billing, Overtime, Shifts, Holiday Calendar, Carry-Forward Leave, Complex Analytics

---

# 2. Technology Stack

## 2.1 MVP Dependencies

| Technology | Role | Why |
|-----------|------|-----|
| **Python 3.11+** | Runtime | Mature async support; vast ecosystem; team productivity |
| **FastAPI** | Web framework | Automatic OpenAPI docs; async-native; Pydantic integration; high performance |
| **Pydantic v2** | Data validation & serialization | First-class FastAPI integration; strict type enforcement; powerful validators |
| **SQLAlchemy 2.x** | ORM & query builder | Battle-tested; async support; migrations via Alembic; avoids raw SQL for most queries |
| **Alembic** | Database migrations | Tight SQLAlchemy integration; incremental schema change management |
| **PostgreSQL 15+** | Primary database | ACID compliance; rich constraints; UUID support; excellent concurrency; JSON support for flexible fields |
| **psycopg3 (asyncpg)** | Async PostgreSQL driver | Native async; required for SQLAlchemy 2.x async mode |
| **python-jose / PyJWT** | JWT generation & validation | Industry-standard JWT handling; access and refresh token management |
| **passlib + bcrypt** | Password hashing | bcrypt is the gold standard; passlib abstracts the hashing interface cleanly |
| **python-multipart** | Form data parsing | Required for FastAPI OAuth2 form-based flows |
| **python-dotenv / pydantic-settings** | Configuration management | Pydantic Settings reads from environment variables with type enforcement |
| **httpx** | Async HTTP client | For any outbound HTTP calls (e.g., email service); also used in tests |
| **structlog** | Structured logging | JSON-structured logs that work with any log aggregation platform |
| **pytest + pytest-asyncio** | Test runner | Async test support for FastAPI; integrates cleanly with SQLAlchemy async |
| **uvicorn** | ASGI server | Production-grade ASGI server; used for both local dev and deployment |

## 2.2 Future / Optional Dependencies

| Technology | Role | When to Introduce |
|-----------|------|-------------------|
| **Celery + Redis** | Background task queue | When scheduled jobs (leave allocation, absence marking) outgrow FastAPI `BackgroundTasks` |
| **APScheduler** | In-process cron scheduler | Intermediate step before Celery; useful for simple scheduled tasks |
| **SendGrid / Resend / SMTP** | Transactional email | Needed for invite emails and password reset (MVP must have email delivery; SDK choice is implementation-level) |
| **Redis** | Caching / rate limiting | Post-MVP for caching dashboard summaries and rate-limiting APIs |
| **Sentry** | Error monitoring | Post-MVP for production error tracking |
| **Prometheus + Grafana** | Metrics & dashboards | Post-MVP observability |
| **Datadog / OpenTelemetry** | Distributed tracing | Post-MVP when multiple services are introduced |
| **Docker / docker-compose** | Containerization | Dev environment parity; production deployment |
| **Nginx** | Reverse proxy | Production deployment in front of uvicorn |

---

# 3. Architecture

## 3.1 Architectural Pattern: Modular Monolith

The application is a single FastAPI process with a clearly partitioned internal structure. Each business domain is a self-contained **module** with its own router, schemas, services, and repositories. Modules do not reach across each other's repository layers.

## 3.2 Layer Definitions

### Application Layer (Entry Point)
- FastAPI application factory
- Registers all routers
- Configures middleware (CORS, logging, request ID injection)
- Configures exception handlers
- Initializes database connection pool
- Loads configuration

### API Layer (Routers)
- FastAPI `APIRouter` instances, one per module
- Responsible for HTTP protocol concerns only: extracting request data, calling services, returning responses
- Must not contain business logic
- Must not contain direct database calls
- Must not contain cross-module imports below the service layer

### Schema Layer (Pydantic Models)
- Request schemas: validated input from clients
- Response schemas: serialized output to clients
- Defined per module
- Shared schemas (e.g., pagination envelope, error response) live in `app/shared/schemas/`

### Service Layer (Business Logic)
- One service class per domain concept (e.g., `LeaveService`, `AttendanceService`)
- Orchestrates repositories and enforces business rules
- Handles cross-module coordination through service-to-service calls (not repo-to-repo)
- Services are injected into routers via FastAPI dependency injection

### Repository Layer (Data Access)
- One repository class per aggregate root or major entity
- Responsible for all SQL/ORM queries
- Returns ORM model instances or typed result objects
- Completely isolated from HTTP concerns
- Accepts a database session injected by the service

### Domain Model Layer (ORM Models)
- SQLAlchemy ORM models
- Define table structure, column types, constraints, and relationships
- Owned strictly by their module

### Database Layer
- PostgreSQL database
- Accessed only through SQLAlchemy async sessions
- Connection pool managed by the application factory

### Shared / Common Layer
- Shared utilities: request ID, pagination helpers, base exception classes, common Pydantic types
- Not tied to any business domain

### Configuration Layer
- Pydantic Settings model loading from environment variables
- Separation of dev, staging, and production configurations
- Secrets never hardcoded

### Authentication / Authorization Boundary
- FastAPI dependencies (`Depends`) extract and validate JWT from every protected route
- The current authenticated user (with tenant ID and role) is injected into every protected router as a dependency
- Authorization checks happen in the service layer, not the router

### Background Job Boundary
- For MVP: FastAPI `BackgroundTasks` for lightweight async tasks (sending emails, triggering leave→attendance updates)
- Scheduled jobs (absence marking at end of day, periodic leave allocation): an in-process scheduler (APScheduler) wired at startup in MVP; migrated to Celery when scale demands

## 3.3 Module Communication Rules

- **Allowed:** Service A calls Service B's public method
- **Allowed:** Module A reads an entity owned by Module B through Module B's service
- **Not allowed:** Module A's repository directly queries Module B's tables
- **Not allowed:** Circular service dependencies
- **Not allowed:** Business logic in routers
- **Not allowed:** ORM model imports across module boundaries (use service return types / DTOs)

## 3.4 What Lives in a Module

| Belongs in Module | Does Not Belong in Module |
|---|---|
| Module's ORM models | Another module's ORM models |
| Module's Pydantic schemas | Shared schemas |
| Module's service(s) | Cross-module database joins |
| Module's repository/ies | Global middleware |
| Module's router | Application factory |
| Module's exceptions | Global exception handler |
| Module's constants | Infrastructure config |

## 3.5 What Lives in Shared Infrastructure

- Base exception classes
- Pagination request/response schemas
- Standard error response schema
- JWT dependency (current user extraction)
- Database session factory / dependency
- Request ID middleware
- Common date/time utilities
- Tenant isolation enforcement utilities

---

# 4. Proposed Project Structure

```text
employee-management/
├── app/
│   ├── main.py                          # Application factory; registers routers, middleware, exception handlers
│   ├── core/
│   │   ├── config.py                    # Pydantic Settings; all environment variables typed here
│   │   ├── security.py                  # JWT creation, validation, password hashing utilities
│   │   ├── dependencies.py              # Shared FastAPI Depends: get_db, get_current_user, require_admin, require_manager
│   │   ├── exceptions.py                # Base application exception classes
│   │   └── logging.py                   # structlog configuration and request ID injection
│   │
│   ├── db/
│   │   ├── base.py                      # SQLAlchemy declarative base; imports all models for Alembic discovery
│   │   ├── session.py                   # Async engine, sessionmaker, get_db dependency
│   │   └── utils.py                     # Transaction helpers, soft-delete filters
│   │
│   ├── shared/
│   │   ├── schemas/
│   │   │   ├── pagination.py            # PaginatedResponse, PageParams schemas
│   │   │   ├── errors.py                # Standard ErrorResponse, ErrorDetail schemas
│   │   │   └── base.py                  # Base response model (timestamps, IDs)
│   │   └── utils/
│   │       ├── datetime_utils.py        # Timezone-aware date helpers
│   │       └── pagination_utils.py      # Offset/limit helpers
│   │
│   └── modules/
│       ├── organization/
│       │   ├── router.py                # /api/v1/organizations/*
│       │   ├── service.py               # OrganizationService
│       │   ├── repository.py            # OrganizationRepository
│       │   ├── models.py                # Organization ORM model
│       │   ├── schemas.py               # Request/response schemas
│       │   └── exceptions.py            # OrganizationAlreadyExistsError, etc.
│       │
│       ├── auth/
│       │   ├── router.py                # /api/v1/auth/*
│       │   ├── service.py               # AuthService
│       │   ├── repository.py            # UserRepository, RefreshTokenRepository, PasswordResetRepository
│       │   ├── models.py                # User, RefreshToken, PasswordResetToken ORM models
│       │   ├── schemas.py               # LoginRequest, TokenResponse, PasswordResetRequest, etc.
│       │   └── exceptions.py            # InvalidCredentialsError, TokenExpiredError, etc.
│       │
│       ├── employees/
│       │   ├── router.py                # /api/v1/employees/*
│       │   ├── service.py               # EmployeeService
│       │   ├── repository.py            # EmployeeRepository
│       │   ├── models.py                # Employee ORM model
│       │   ├── schemas.py               # EmployeeCreate, EmployeeResponse, EmployeeUpdate, etc.
│       │   └── exceptions.py            # EmployeeNotFoundError, CannotDeactivateSoleAdminError, etc.
│       │
│       ├── work_tracker/
│       │   ├── router.py                # /api/v1/work-entries/*
│       │   ├── service.py               # WorkEntryService
│       │   ├── repository.py            # WorkEntryRepository
│       │   ├── models.py                # WorkEntry ORM model
│       │   ├── schemas.py               # WorkEntryCreate, WorkEntryResponse, WorkEntryUpdate, etc.
│       │   └── exceptions.py            # WorkEntryLockedError, WorkEntryNotFoundError, etc.
│       │
│       ├── attendance/
│       │   ├── router.py                # /api/v1/attendance/*
│       │   ├── service.py               # AttendanceService
│       │   ├── repository.py            # AttendanceRepository
│       │   ├── models.py                # AttendanceRecord ORM model
│       │   ├── schemas.py               # CheckInResponse, AttendanceRecordResponse, ManualCorrectionRequest, etc.
│       │   └── exceptions.py            # AlreadyCheckedInError, AlreadyCheckedOutError, etc.
│       │
│       ├── leave/
│       │   ├── router.py                # /api/v1/leave/*
│       │   ├── service.py               # LeaveService
│       │   ├── repository.py            # LeaveTypeRepository, LeavePolicyRepository, LeaveBalanceRepository, LeaveRecordRepository
│       │   ├── models.py                # LeaveType, LeavePolicyRule, LeaveBalance, LeaveRecord ORM models
│       │   ├── schemas.py               # LeaveRequestCreate, LeaveGrantRequest, LeaveBalanceResponse, etc.
│       │   └── exceptions.py            # InsufficientLeaveBalanceError, OverlappingLeaveError, etc.
│       │
│       └── dashboard/
│           ├── router.py                # /api/v1/dashboard/*
│           ├── service.py               # DashboardService
│           ├── schemas.py               # EmployeeDashboard, ManagerDashboard, AdminDashboard response schemas
│           └── exceptions.py            # (minimal — dashboard is read-only)
│
├── tests/
│   ├── conftest.py                      # Test database setup, fixtures, authenticated client factory
│   ├── unit/
│   │   ├── services/                    # Service layer unit tests (mocked repositories)
│   │   └── utils/                       # Utility function tests
│   ├── integration/
│   │   ├── test_organization.py
│   │   ├── test_auth.py
│   │   ├── test_employees.py
│   │   ├── test_work_tracker.py
│   │   ├── test_attendance.py
│   │   ├── test_leave.py
│   │   └── test_dashboard.py
│   ├── e2e/
│   │   └── test_leave_workflow.py       # Full workflow: request → approve → attendance updated
│   └── security/
│       └── test_tenant_isolation.py    # Verify no cross-tenant data access
│
├── alembic/
│   ├── env.py                           # Alembic environment; imports Base from app/db/base.py
│   ├── script.py.mako
│   └── versions/                        # Auto-generated migration files
│
├── docs/
│   ├── product-spec.md                  # Product specification (source of truth)
│   └── technical-blueprint.md           # This document
│
├── scripts/
│   └── seed_dev_data.py                 # Local dev data seeding script
│
├── .env.example                         # Example environment variables (no secrets)
├── pyproject.toml                       # Project metadata and dependencies
├── alembic.ini
└── README.md
```

### Directory Responsibility Summary

| Directory | Responsibility | MVP-Critical |
|-----------|---------------|:---:|
| `app/main.py` | Application factory; wires everything together | ✅ |
| `app/core/` | Security, configuration, shared dependencies, logging | ✅ |
| `app/db/` | Database session, engine, base model | ✅ |
| `app/shared/` | Reusable schemas, utilities shared across modules | ✅ |
| `app/modules/` | All business domain modules | ✅ |
| `tests/` | All test types (unit, integration, e2e, security) | ✅ |
| `alembic/` | Schema migration management | ✅ |
| `docs/` | Architecture and product documentation | ✅ |
| `scripts/` | Development utilities (seeding, admin tasks) | Helpful |

---

# 5. Module Architecture

## 5.1 Module Table

| Module | Responsibility | MVP? | Dependencies | Key Entities | Priority |
|--------|---------------|:----:|-------------|-------------|:--------:|
| **Organization** | Tenant foundation; org lifecycle; org settings | ✅ | None | Organization | 1 — First |
| **Auth** | User identity; login; tokens; password lifecycle | ✅ | Organization | User, RefreshToken, PasswordResetToken | 2 |
| **Employees** | Employee profiles; roles; manager assignments; deactivation | ✅ | Organization, Auth | Employee | 3 |
| **Work Tracker** | Daily work entry logging and review | ✅ | Organization, Employees | WorkEntry | 4 |
| **Attendance** | Daily check-in/out; absence marking; manual correction | ✅ | Organization, Employees, Leave | AttendanceRecord | 4 |
| **Leave** | Policy; balance; request workflow; grants; allocation | ✅ | Organization, Employees, Attendance | LeaveType, LeavePolicyRule, LeaveBalance, LeaveRecord | 5 |
| **Dashboard** | Role-scoped summary views; read-only aggregation | ✅ | All other modules | None (read-only) | 6 — Last |

## 5.2 Module Detail: Organization

- **Purpose:** Creates and maintains the tenant. Bootstrap entry point for the entire SaaS.
- **APIs:** Register org, Get org settings, Update org settings
- **Service responsibilities:** Validate name uniqueness globally; create org atomically with Admin user+employee
- **Repository:** `OrganizationRepository` — find by name, find by ID, create, update
- **Future extension:** Billing hooks, multiple admins, org suspension

## 5.3 Module Detail: Auth

- **Purpose:** Manages authentication credentials and session lifecycle.
- **APIs:** Login, Logout, Refresh token, Request password reset, Confirm password reset
- **Service responsibilities:** Credential validation; token issuance; token revocation; password hashing; reset token lifecycle
- **Repositories:** `UserRepository` (find by email, update status), `RefreshTokenRepository` (create, revoke, find), `PasswordResetTokenRepository` (create, find, mark used)
- **Cross-module action:** On employee deactivation, `AuthService.revoke_all_tokens(user_id)` is called

## 5.4 Module Detail: Employees

- **Purpose:** Canonical registry of who belongs to the organization.
- **APIs:** Create employee, Get employee, Update employee, Assign manager, Deactivate employee, List employees
- **Service responsibilities:** Email uniqueness per org; manager validity; self-referencing prevention; deactivation cascade (calls AuthService)
- **Repository:** `EmployeeRepository` — find by ID, find by manager, list by org, update status, update manager
- **Future extension:** Self-service edits, CSV import, department hierarchy

## 5.5 Module Detail: Work Tracker

- **Purpose:** Daily work log — what did each employee work on?
- **APIs:** Create work entry, Get work entry, Update work entry, List my entries, List team entries (manager), List employee entries (admin)
- **Service responsibilities:** Date validation (no future dates); 24-hour lock enforcement; employee active check; scope enforcement
- **Repository:** `WorkEntryRepository` — find by employee + date range, find by ID, create, update
- **Future extension:** Project tagging, time tracking, approval workflow

## 5.6 Module Detail: Attendance

- **Purpose:** Tracks presence per employee per calendar day.
- **APIs:** Check in, Check out, View own attendance, View team attendance (manager), View all attendance (admin), Manual correction
- **Service responsibilities:** One record per employee per date enforcement; timezone-aware day boundary calculation; status state machine; manual override audit trail
- **Repository:** `AttendanceRepository` — find by employee + date, find by org + date, create, update status
- **Cross-module write:** `AttendanceService.mark_leave_for_dates(employee_id, dates, leave_record_id)` is called by LeaveService
- **Scheduled job:** End-of-day job marks all employees without a check-in as ABSENT

## 5.7 Module Detail: Leave

- **Purpose:** Full leave lifecycle — policy, balance, request, approval, direct grant, auto-allocation.
- **APIs:** Configure leave types, Configure policy rules, Get my balance, Request leave, Cancel leave request, View team requests (manager), Approve/reject request (manager), Grant leave directly (manager), View all balances (admin)
- **Service responsibilities:** Balance deduction/restoration; overlap detection; automatic allocation per policy; date range calculation excluding weekends; triggering attendance updates
- **Repositories:** `LeaveTypeRepository`, `LeavePolicyRepository`, `LeaveBalanceRepository`, `LeaveRecordRepository`
- **Cross-module write:** On approval/grant, calls `AttendanceService.mark_leave_for_dates()`
- **Scheduled job:** Periodic allocation runner evaluates all active employees against policy rules

## 5.8 Module Detail: Dashboard

- **Purpose:** Role-scoped read-only summaries for immediate operational visibility.
- **APIs:** Employee dashboard, Manager dashboard, Admin dashboard
- **Service responsibilities:** Fan-out reads to Employee, Work Tracker, Attendance, Leave services; assemble into role-specific response
- **No repository:** Dashboard reads through other modules' services — never directly queries their tables
- **Future extension:** Charting data endpoints, analytics

---

# 6. Multi-Tenant SaaS Architecture

## 6.1 Tenant Concept

A **Tenant** is an **Organization**. Every piece of data in the system belongs to exactly one organization. There is no global data (except the `organizations` table itself, which is platform-level).

## 6.2 Tenant Identification

- On organization registration, the organization receives a UUID primary key (`organization_id`).
- When a user authenticates, their JWT payload includes `organization_id`.
- On every API request, the authenticated user's `organization_id` is extracted from the JWT and enforced at the service layer before any query is executed.

## 6.3 User → Tenant Relationship

- Each `User` record contains an `organization_id` foreign key.
- Each `Employee` record contains an `organization_id` foreign key.
- A user in MVP belongs to exactly one organization. They cannot be shared across organizations.

## 6.4 Tenant Isolation

**MVP approach: Shared database, shared schema, row-level isolation.**

Every table that contains tenant data includes an `organization_id` column. Every query that reads or writes tenant data must include a `WHERE organization_id = :current_tenant_id` clause. This is enforced at the **repository layer** — all repository methods receive the `organization_id` as a required parameter and include it in every query.

**What this means in practice:**
- No repository method may query tenant-scoped data without an `organization_id` argument.
- Cross-tenant queries are architecturally impossible at the repository level.
- This must be enforced through code review, and verified by the tenant isolation test suite.

## 6.5 Tenant-Aware Authorization

The current user dependency (`get_current_user`) provides:
```
CurrentUser:
  user_id: UUID
  organization_id: UUID
  employee_id: UUID
  role: Role (ADMIN | MANAGER | EMPLOYEE)
```

Every service method receives this object and uses `organization_id` to scope all repository calls. Services also validate that any ID provided in a request (employee ID, leave record ID, etc.) belongs to the same organization before acting on it.

## 6.6 Super-Admin / System-Level Access

MVP does not include a platform super-admin. The organization Admin role is the highest privilege within a single tenant. Future platform-level admin access (e.g., for support or billing) would require a separate authentication mechanism and is explicitly deferred.

## 6.7 Cross-Tenant Access Prevention

- JWT `organization_id` is validated on every request.
- All repository queries include `organization_id` in their WHERE clause.
- A dedicated security test suite (`tests/security/test_tenant_isolation.py`) verifies that authenticated users from Organization A cannot retrieve data from Organization B.
- If a resource ID is provided that exists in a different organization, the response is **404 Not Found** (not 403 — to avoid confirming the existence of data in other organizations).

## 6.8 Possible Future Evolution

| Evolution | When to Introduce |
|-----------|------------------|
| Row-Level Security (PostgreSQL RLS) | If the application scales to a team where developer mistakes in the repository layer are a real risk; RLS provides a database-enforced safety net |
| Schema-per-tenant | Only if a large enterprise customer demands strict data isolation beyond logical row-level separation; introduces significant operational complexity |
| Separate database per tenant | Not recommended unless contractual/compliance requirements explicitly demand it |

---

# 7. Authentication & Authorization

## 7.1 Authentication — Who Are You?

Authentication answers: is this a valid user, and which organization do they belong to?

### Registration Flow (Organization Admin)
1. Unauthenticated user submits: org name, their name, email, password
2. System creates Organization, User (Admin role), Employee
3. System returns: access token + basic user info

### Employee Login Flow
1. User submits email + password
2. System validates: email exists, password matches hash, user is active
3. System returns: access token (short-lived), refresh token (long-lived)
4. JWT payload: `{ user_id, organization_id, employee_id, role, exp }`

### Token Strategy
- **Access token:** JWT; signed with HS256 (RS256 in post-MVP); 15-minute expiry; stateless
- **Refresh token:** Opaque random token; stored in `refresh_tokens` table; 7-day expiry; single-use rotation in MVP (new login revokes existing)
- **Password reset token:** Opaque random token; stored in `password_reset_tokens` table; 1-hour expiry; single-use

### Session Termination
- Explicit logout: refresh token revoked
- Deactivation: all refresh tokens revoked for the user
- Password reset: all refresh tokens revoked for the user

## 7.2 Authorization — What Are You Allowed To Do?

Authorization answers: given who you are, what data can you act on?

### Role-Based Access Control (RBAC)

Three roles, fixed in MVP:

| Role | Scope |
|------|-------|
| **ADMIN** | Full access within their organization |
| **MANAGER** | Own records + records of their direct reports only |
| **EMPLOYEE** | Own records only |

### Authorization Enforcement Model

Authorization is enforced at **two levels**:

**Level 1 — Route-level role check (FastAPI dependency)**
- `require_admin` dependency: rejects non-admin callers with 403
- `require_manager` dependency: rejects callers with Employee role with 403
- These are applied as `Depends()` on router endpoints

**Level 2 — Service-level scope check (business logic)**
- Manager scope: services verify that the target employee is actually in the requesting manager's team
- A manager requesting data about an employee in a different manager's team receives 403 (not 404 — the resource exists but they lack access)
- Admin bypass: Admin passes all scope checks within their organization

### Permission Decision Table

| Action | Dependency | Service Check |
|--------|-----------|---------------|
| Any admin-only action | `require_admin` | None needed |
| Manager views team record | `require_manager` | Verify target is in manager's team |
| Employee views own record | Authenticated | Verify target_id == current_user.employee_id |
| Leave approval | `require_manager` | Verify requester is target's manager |

### Resource-Level Authorization

When an employee, attendance record, work entry, or leave record is fetched by ID:
1. Repository fetches by ID **and** `organization_id`
2. If not found (wrong org or genuinely missing) → 404
3. If found but scope mismatch (e.g., manager requesting data of another manager's employee) → 403
4. If found and scope valid → proceed

---

# 8. PostgreSQL Database Architecture

## 8.1 Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Table names | `snake_case`, plural | `employees`, `leave_records` |
| Column names | `snake_case` | `organization_id`, `created_at` |
| Primary key column | `id` | `id UUID PRIMARY KEY` |
| Foreign key columns | `{referenced_table_singular}_id` | `employee_id`, `organization_id` |
| Index names | `ix_{table}_{column(s)}` | `ix_employees_organization_id` |
| Unique constraint names | `uq_{table}_{column(s)}` | `uq_users_email_organization_id` |
| Check constraint names | `ck_{table}_{rule}` | `ck_leave_records_end_after_start` |
| Foreign key names | `fk_{table}_{referenced_table}` | `fk_employees_organization` |

## 8.2 Primary Keys

**Use UUID v4 for all primary keys.** Rationale:
- No sequential ID leakage (security)
- Safe to generate in application layer before database insert
- Future-safe if data needs to be merged or migrated across databases
- PostgreSQL's `gen_random_uuid()` provides native support

## 8.3 Foreign Keys

- All foreign keys are declared explicitly with `REFERENCES` and appropriate `ON DELETE` behavior.
- MVP strategy: **no cascading deletes** — prefer soft deletion and status flags.
- `ON DELETE RESTRICT` on critical relationships (prevents orphaned data).

## 8.4 Timestamp Conventions

| Column | Type | Behavior |
|--------|------|----------|
| `created_at` | `TIMESTAMPTZ` | Set on INSERT, never updated; defaults to `NOW()` |
| `updated_at` | `TIMESTAMPTZ` | Set on INSERT and every UPDATE; managed by SQLAlchemy `onupdate` |
| `deleted_at` | `TIMESTAMPTZ` | Nullable; set on soft delete; NULL means active |

All timestamps are stored in UTC. Timezone conversions happen in the application layer using the organization's configured timezone.

## 8.5 Soft Deletion

MVP uses soft deletion for key entities: **Employee**, **User**, **LeaveType**.

- Records are never hard-deleted; `is_active` (boolean) or `deleted_at` (nullable timestamp) marks them as inactive.
- All repository queries for active records must include the soft-delete filter.
- A SQLAlchemy query filter utility in `app/db/utils.py` provides a reusable `active_only()` filter.

**Entities with soft delete:** `employees` (via `is_active`), `users` (via `is_active`), `leave_types` (via `is_active`).  
**Entities never deleted:** `work_entries`, `attendance_records`, `leave_records`, `organizations`.

## 8.6 Audit Fields

Every table has at minimum: `id`, `created_at`, `updated_at`.

Tables with write operations by admins/managers (e.g., manual attendance correction) add: `corrected_by` (FK to users), `correction_reason` (text).

## 8.7 Tenant ID Strategy

Every tenant-scoped table has `organization_id UUID NOT NULL REFERENCES organizations(id)`.

This column is always the **first** index and the **first** filter in every query.

## 8.8 Indexing Strategy

**Mandatory indexes (MVP):**

| Table | Index | Reason |
|-------|-------|--------|
| All tables | `organization_id` | Tenant isolation — every query filters by this |
| `users` | `(organization_id, email)` UNIQUE | Login lookup + uniqueness constraint |
| `employees` | `(organization_id, manager_id)` | Manager team queries |
| `employees` | `(organization_id, is_active)` | Filter active employees |
| `work_entries` | `(employee_id, date)` | Date-range queries per employee |
| `attendance_records` | `(employee_id, date)` UNIQUE | One record per employee per day |
| `attendance_records` | `(organization_id, date)` | Org-wide daily attendance view |
| `leave_records` | `(employee_id, status)` | Pending requests per employee |
| `leave_records` | `(organization_id, start_date, end_date)` | Date-range leave queries |
| `leave_balances` | `(employee_id, leave_type_id, leave_year)` UNIQUE | One balance per employee per type per year |
| `refresh_tokens` | `user_id` | Session lookup on every refresh |

## 8.9 Unique Constraints

- `users`: `(organization_id, email)` — email unique per organization
- `organizations`: `name` — globally unique organization names (case-insensitive; enforce via `LOWER(name)` index)
- `attendance_records`: `(employee_id, date)` — exactly one record per employee per day
- `leave_balances`: `(employee_id, leave_type_id, leave_year)` — one balance record per employee per leave type per year
- `leave_types`: `(organization_id, code)` — leave type codes unique within org

## 8.10 Referential Integrity

All foreign key constraints are enforced at the database level. The application layer does not rely solely on ORM-level relationship validation.

## 8.11 Transaction Boundaries

- Each HTTP request executes within a single database transaction (commit on success, rollback on exception), managed by the `get_db` async context manager.
- Multi-step operations (e.g., approve leave + update attendance) happen within a single transaction.
- Cross-module writes (Leave → Attendance status update) must be executed in the same transaction, not as separate requests.

## 8.12 PostgreSQL-Specific Considerations

- Use `TIMESTAMPTZ` (not `TIMESTAMP`) for all timestamp columns — timezone-aware by default.
- Use `TEXT` for variable-length strings (not `VARCHAR(n)`) except where a hard maximum is enforced by business rules.
- Use `SMALLINT` for status enums that will be stored as integers, or `TEXT` with a `CHECK` constraint for readable string enums. Prefer `TEXT` with `CHECK` for MVP readability.
- Use `gen_random_uuid()` for server-generated UUIDs where the ID doesn't need to be known before the insert.

---

# 9. Database Entity Overview

## 9.1 Entity List

| Entity | Module | Table Name |
|--------|--------|-----------|
| Organization | Organization | `organizations` |
| User | Auth | `users` |
| RefreshToken | Auth | `refresh_tokens` |
| PasswordResetToken | Auth | `password_reset_tokens` |
| Employee | Employees | `employees` |
| WorkEntry | Work Tracker | `work_entries` |
| AttendanceRecord | Attendance | `attendance_records` |
| LeaveType | Leave | `leave_types` |
| LeavePolicyRule | Leave | `leave_policy_rules` |
| LeaveBalance | Leave | `leave_balances` |
| LeaveRecord | Leave | `leave_records` |

## 9.2 Entity Details

### Organization (`organizations`)
- **Purpose:** Top-level tenant container
- **Key Fields:** `id` (UUID PK), `name` (TEXT, globally unique), `slug` (TEXT, unique), `timezone` (TEXT, IANA format), `is_active` (BOOL), `created_at`, `updated_at`
- **Relationships:** Parent of all other entities
- **Tenant ownership:** This IS the tenant — no `organization_id` column
- **Constraints:** `name` globally unique; `timezone` immutable via self-service in MVP

---

### User (`users`)
- **Purpose:** Authentication identity — login credentials and session state
- **Key Fields:** `id` (UUID PK), `organization_id` (FK), `email` (TEXT), `hashed_password` (TEXT), `is_active` (BOOL), `last_login_at` (TIMESTAMPTZ, nullable), `created_at`, `updated_at`
- **Relationships:** One-to-one with Employee; many-to-one with Organization
- **Tenant ownership:** `organization_id`
- **Constraints:** `(organization_id, email)` unique

---

### RefreshToken (`refresh_tokens`)
- **Purpose:** Tracks valid refresh tokens for session management
- **Key Fields:** `id` (UUID PK), `user_id` (FK), `token_hash` (TEXT, hashed value of token), `expires_at` (TIMESTAMPTZ), `revoked_at` (TIMESTAMPTZ, nullable), `created_at`
- **Relationships:** Many-to-one with User
- **Tenant ownership:** Implicit through User
- **Constraints:** One active (non-revoked, non-expired) token per user in MVP

---

### PasswordResetToken (`password_reset_tokens`)
- **Purpose:** Secure, time-limited tokens for password reset flow
- **Key Fields:** `id` (UUID PK), `user_id` (FK), `token_hash` (TEXT), `expires_at` (TIMESTAMPTZ), `used_at` (TIMESTAMPTZ, nullable), `created_at`
- **Relationships:** Many-to-one with User
- **Constraints:** Only one active (unused, non-expired) token per user at a time

---

### Employee (`employees`)
- **Purpose:** HR profile of a person in the organization
- **Key Fields:** `id` (UUID PK), `organization_id` (FK), `user_id` (FK, unique), `full_name` (TEXT), `email` (TEXT, mirrored from User), `role` (TEXT: ADMIN / MANAGER / EMPLOYEE), `is_active` (BOOL), `joining_date` (DATE), `manager_id` (FK → `employees.id`, nullable), `department` (TEXT, nullable), `job_title` (TEXT, nullable), `created_at`, `updated_at`
- **Relationships:** Many-to-one with Organization; one-to-one with User; self-referencing many-to-one (manager)
- **Tenant ownership:** `organization_id`
- **Constraints:** `manager_id != id` (cannot be own manager); only one Admin per org in MVP

---

### WorkEntry (`work_entries`)
- **Purpose:** Daily work log entry per employee
- **Key Fields:** `id` (UUID PK), `organization_id` (FK), `employee_id` (FK), `date` (DATE), `title` (TEXT, required), `description` (TEXT, nullable), `duration_minutes` (INTEGER, nullable, positive), `created_at`, `updated_at`
- **Relationships:** Many-to-one with Employee
- **Tenant ownership:** `organization_id`
- **Constraints:** `date <= today`; `duration_minutes > 0` if present; lock enforced at application layer (24h from `created_at`)

---

### AttendanceRecord (`attendance_records`)
- **Purpose:** One attendance status per employee per calendar day
- **Key Fields:** `id` (UUID PK), `organization_id` (FK), `employee_id` (FK), `date` (DATE), `status` (TEXT: PRESENT / ABSENT / LEAVE), `check_in_at` (TIMESTAMPTZ, nullable), `check_out_at` (TIMESTAMPTZ, nullable), `duration_minutes` (INTEGER, nullable, computed), `is_manual_override` (BOOL, default false), `override_reason` (TEXT, nullable), `corrected_by` (FK → users, nullable), `leave_record_id` (FK → leave_records, nullable), `created_at`, `updated_at`
- **Relationships:** Many-to-one with Employee; optional FK to LeaveRecord
- **Tenant ownership:** `organization_id`
- **Constraints:** `(employee_id, date)` unique; `check_out_at > check_in_at` when both present

---

### LeaveType (`leave_types`)
- **Purpose:** Category of leave (e.g., Casual, Sick, Annual)
- **Key Fields:** `id` (UUID PK), `organization_id` (FK), `name` (TEXT), `code` (TEXT, short e.g., "CL"), `description` (TEXT, nullable), `is_active` (BOOL), `created_at`, `updated_at`
- **Relationships:** Many-to-one with Organization
- **Tenant ownership:** `organization_id`
- **Constraints:** `(organization_id, code)` unique; `(organization_id, name)` unique

---

### LeavePolicyRule (`leave_policy_rules`)
- **Purpose:** How leave of a specific type is automatically allocated
- **Key Fields:** `id` (UUID PK), `organization_id` (FK), `leave_type_id` (FK), `allocation_amount` (NUMERIC, positive), `allocation_frequency` (TEXT: MONTHLY / QUARTERLY / ANNUALLY), `minimum_tenure_days` (INTEGER, default 0), `max_balance_cap` (NUMERIC, >= allocation_amount), `is_pro_rated` (BOOL), `created_at`, `updated_at`
- **Relationships:** Many-to-one with Organization; many-to-one with LeaveType
- **Tenant ownership:** `organization_id`
- **Constraints:** `(organization_id, leave_type_id)` unique; `max_balance_cap >= allocation_amount`

---

### LeaveBalance (`leave_balances`)
- **Purpose:** Current available leave days per employee per leave type per year
- **Key Fields:** `id` (UUID PK), `organization_id` (FK), `employee_id` (FK), `leave_type_id` (FK), `leave_year` (INTEGER), `balance` (NUMERIC, >= 0), `total_allocated` (NUMERIC), `total_used` (NUMERIC), `created_at`, `updated_at`
- **Relationships:** Many-to-one with Employee; many-to-one with LeaveType
- **Tenant ownership:** `organization_id`
- **Constraints:** `(employee_id, leave_type_id, leave_year)` unique; `balance >= 0`

---

### LeaveRecord (`leave_records`)
- **Purpose:** A leave event — request, approval, rejection, cancellation, or direct grant
- **Key Fields:** `id` (UUID PK), `organization_id` (FK), `employee_id` (FK), `leave_type_id` (FK), `start_date` (DATE), `end_date` (DATE), `num_days` (INTEGER, computed), `status` (TEXT: PENDING / APPROVED / REJECTED / CANCELLED / GRANTED), `reason` (TEXT, nullable), `actioned_by` (FK → users, nullable), `actioned_at` (TIMESTAMPTZ, nullable), `created_at`, `updated_at`
- **Relationships:** Many-to-one with Employee; many-to-one with LeaveType
- **Tenant ownership:** `organization_id`
- **Constraints:** `end_date >= start_date`; no overlapping PENDING/APPROVED/GRANTED records for same employee

---

# 10. API Architecture

## 10.1 Base API Path

All APIs are prefixed: `/api/v1/`

## 10.2 Versioning

Version is embedded in the URL path. The FastAPI application mounts all v1 routers under `/api/v1`. When v2 is needed, a new router prefix `/api/v2/` is introduced for the affected resources only; unchanged resources remain on v1.

## 10.3 Resource Naming

- Resources are **plural nouns**: `/employees`, `/work-entries`, `/leave-records`
- Sub-resources use nested paths: `/leave/types`, `/leave/policy-rules`, `/leave/balances`
- Actions that are not CRUD use **verb-qualified paths**: `/auth/login`, `/auth/logout`, `/attendance/check-in`, `/attendance/check-out`
- No verbs in resource paths except for actions

## 10.4 HTTP Methods

| Method | Use | Idempotent |
|--------|-----|:---:|
| `GET` | Retrieve a resource or list | ✅ |
| `POST` | Create a resource or trigger an action | ❌ |
| `PATCH` | Partial update of a resource | ✅ |
| `PUT` | Full replacement of a resource (rarely used; prefer PATCH) | ✅ |
| `DELETE` | Soft-delete (not used in MVP; records are deactivated) | ✅ |

## 10.5 Standard HTTP Status Codes

| Code | Meaning |
|------|---------|
| `200 OK` | Successful retrieval or update |
| `201 Created` | Successful resource creation |
| `204 No Content` | Successful action with no response body (e.g., logout) |
| `400 Bad Request` | Malformed request (non-validation errors) |
| `401 Unauthorized` | Missing or invalid authentication token |
| `403 Forbidden` | Authenticated but lacks permission |
| `404 Not Found` | Resource does not exist (or exists in another org) |
| `409 Conflict` | Resource already exists or state conflict |
| `422 Unprocessable Entity` | Pydantic validation error |
| `500 Internal Server Error` | Unexpected server error |

## 10.6 Pagination

All list endpoints support cursor-based pagination for consistency. For MVP, **offset-based pagination** is acceptable given expected data volumes.

**Query parameters:** `?page=1&page_size=20` (default page_size: 20, max: 100)

## 10.7 Filtering

Filter parameters are query string parameters:
- `?status=active` — filter by status
- `?date_from=2024-01-01&date_to=2024-01-31` — date range filter
- `?employee_id=<uuid>` — filter by employee (admin/manager endpoints)

## 10.8 Sorting

`?sort_by=created_at&sort_order=desc` (default: `created_at desc`)

## 10.9 Searching

`?search=<term>` — applied to the primary display field of the resource (e.g., employee name, work entry title)

## 10.10 Validation

All request body validation is handled by Pydantic. Validation errors return `422` with the standard error response format.

## 10.11 Authentication Headers

All protected endpoints require: `Authorization: Bearer <access_token>`

## 10.12 Request IDs

Every request receives a unique `X-Request-ID` header in the response. If the client sends `X-Request-ID`, it is echoed back. Otherwise, the server generates one. All log entries for a request include this ID.

---

# 11. API Documentation Structure

## Module: System

| Method | Endpoint | Purpose | Auth | Role | Priority |
|--------|---------|---------|:----:|:----:|:--------:|
| GET | `/api/v1/health` | System health check | No | Public | MVP |

---

## Module: Organization

| Method | Endpoint | Purpose | Auth | Role | Priority |
|--------|---------|---------|:----:|:----:|:--------:|
| POST | `/api/v1/organizations/register` | Register new org + admin user | No | Public | MVP |
| GET | `/api/v1/organizations/me` | Get current org settings | Yes | Admin | MVP |
| PATCH | `/api/v1/organizations/me` | Update org settings | Yes | Admin | MVP |

---

## Module: Authentication

| Method | Endpoint | Purpose | Auth | Role | Priority |
|--------|---------|---------|:----:|:----:|:--------:|
| POST | `/api/v1/auth/login` | Login with email + password | No | Public | MVP |
| POST | `/api/v1/auth/refresh` | Refresh access token | No | Valid refresh token | MVP |
| POST | `/api/v1/auth/logout` | Logout / revoke session | Yes | Any | MVP |
| GET | `/api/v1/auth/me` | Get current authenticated user | Yes | Any | MVP |
| POST | `/api/v1/auth/password-reset/request` | Request password reset email | No | Public | MVP |
| POST | `/api/v1/auth/password-reset/confirm` | Confirm password reset | No | Reset token | MVP |

---

## Module: Employees

| Method | Endpoint | Purpose | Auth | Role | Priority |
|--------|---------|---------|:----:|:----:|:--------:|
| POST | `/api/v1/employees` | Create employee | Yes | Admin | MVP |
| GET | `/api/v1/employees` | List employees | Yes | Admin / Manager | MVP |
| GET | `/api/v1/employees/{employee_id}` | Get employee profile | Yes | Admin / Manager / Self | MVP |
| PATCH | `/api/v1/employees/{employee_id}` | Update employee profile | Yes | Admin | MVP |
| POST | `/api/v1/employees/{employee_id}/manager` | Assign / change manager | Yes | Admin | MVP |
| POST | `/api/v1/employees/{employee_id}/deactivate` | Deactivate employee | Yes | Admin | MVP |

---

## Module: Work Tracker

| Method | Endpoint | Purpose | Auth | Role | Priority |
|--------|---------|---------|:----:|:----:|:--------:|
| POST | `/api/v1/work-entries` | Create work entry | Yes | Any | MVP |
| GET | `/api/v1/work-entries` | List work entries (scoped by role) | Yes | Any | MVP |
| GET | `/api/v1/work-entries/{entry_id}` | Get work entry | Yes | Any (scoped) | MVP |
| PATCH | `/api/v1/work-entries/{entry_id}` | Update work entry | Yes | Any (scoped, time-limited) | MVP |

---

## Module: Attendance

| Method | Endpoint | Purpose | Auth | Role | Priority |
|--------|---------|---------|:----:|:----:|:--------:|
| POST | `/api/v1/attendance/check-in` | Check in for today | Yes | Any | MVP |
| POST | `/api/v1/attendance/check-out` | Check out for today | Yes | Any | MVP |
| GET | `/api/v1/attendance` | List attendance records (scoped) | Yes | Any | MVP |
| GET | `/api/v1/attendance/{record_id}` | Get attendance record | Yes | Any (scoped) | MVP |
| PATCH | `/api/v1/attendance/{record_id}/correct` | Manually correct attendance | Yes | Admin / Manager | MVP |

---

## Module: Leave

| Method | Endpoint | Purpose | Auth | Role | Priority |
|--------|---------|---------|:----:|:----:|:--------:|
| POST | `/api/v1/leave/types` | Create leave type | Yes | Admin | MVP |
| GET | `/api/v1/leave/types` | List leave types | Yes | Any | MVP |
| PATCH | `/api/v1/leave/types/{type_id}` | Update leave type | Yes | Admin | MVP |
| POST | `/api/v1/leave/policy-rules` | Create / update policy rule | Yes | Admin | MVP |
| GET | `/api/v1/leave/policy-rules` | List policy rules | Yes | Admin | MVP |
| GET | `/api/v1/leave/balances` | View leave balances (scoped) | Yes | Any | MVP |
| POST | `/api/v1/leave/requests` | Submit leave request | Yes | Any | MVP |
| GET | `/api/v1/leave/requests` | List leave requests (scoped) | Yes | Any | MVP |
| GET | `/api/v1/leave/requests/{request_id}` | Get leave request | Yes | Any (scoped) | MVP |
| POST | `/api/v1/leave/requests/{request_id}/cancel` | Cancel own pending request | Yes | Any (self) | MVP |
| POST | `/api/v1/leave/requests/{request_id}/approve` | Approve leave request | Yes | Admin / Manager | MVP |
| POST | `/api/v1/leave/requests/{request_id}/reject` | Reject leave request | Yes | Admin / Manager | MVP |
| POST | `/api/v1/leave/grants` | Directly grant leave to employee | Yes | Admin / Manager | MVP |

---

## Module: Dashboard

| Method | Endpoint | Purpose | Auth | Role | Priority |
|--------|---------|---------|:----:|:----:|:--------:|
| GET | `/api/v1/dashboard` | Get role-appropriate dashboard | Yes | Any | MVP |

---

**API Surface Summary:**

| Module | API Count |
|--------|:---------:|
| System | 1 |
| Organization | 3 |
| Authentication | 6 |
| Employees | 6 |
| Work Tracker | 4 |
| Attendance | 5 |
| Leave | 13 |
| Dashboard | 1 |
| **Total** | **39** |

---

# 12. API Request/Response Design

## 12.1 Request Schema Conventions

- All request body schemas are Pydantic models
- Field names use `snake_case`
- Required fields have no default; optional fields have `None` default
- String fields are stripped of leading/trailing whitespace
- Date fields use `date` type (ISO 8601: `YYYY-MM-DD`)
- Timestamps use `datetime` type (ISO 8601 with timezone)

## 12.2 Response Schema Conventions

- All responses wrapped in a consistent envelope only for paginated lists
- Single resources are returned directly (not wrapped)
- Timestamps are returned in ISO 8601 format with UTC timezone
- Null fields are included in response (not omitted) for client predictability

## 12.3 Standard Response Structures

### Single Resource Response
```json
{
  "id": "a3f1c2d4-...",
  "organization_id": "b1c2d3e4-...",
  "full_name": "Jane Smith",
  "email": "jane@acme.com",
  "role": "EMPLOYEE",
  "is_active": true,
  "joining_date": "2024-01-15",
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T09:00:00Z"
}
```

### Paginated List Response
```json
{
  "items": [ {...}, {...} ],
  "total": 47,
  "page": 1,
  "page_size": 20,
  "pages": 3
}
```

### Token Response (Login / Refresh)
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### Leave Balance Response
```json
{
  "employee_id": "a3f1c2d4-...",
  "leave_year": 2024,
  "balances": [
    {
      "leave_type_id": "c1d2e3f4-...",
      "leave_type_name": "Casual Leave",
      "leave_type_code": "CL",
      "balance": 6.0,
      "total_allocated": 12.0,
      "total_used": 6.0
    }
  ]
}
```

## 12.4 Error Response Structure

All errors follow a consistent structure (see Section 13 for full detail):

```json
{
  "error": {
    "code": "EMPLOYEE_NOT_FOUND",
    "message": "Employee with the given ID was not found.",
    "details": null,
    "request_id": "req_7f3a2b1c..."
  }
}
```

## 12.5 Validation Error Response (422)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": [
      {
        "field": "email",
        "message": "value is not a valid email address"
      },
      {
        "field": "joining_date",
        "message": "date cannot be in the future"
      }
    ],
    "request_id": "req_7f3a2b1c..."
  }
}
```

---

# 13. Error Handling Strategy

## 13.1 Philosophy

All errors return a **consistent, machine-readable error structure** so clients can reliably parse and handle errors without inspecting human-readable messages.

## 13.2 Standard Error Response Format

```json
{
  "error": {
    "code": "SNAKE_CASE_ERROR_CODE",
    "message": "Human-readable description of the error.",
    "details": null,
    "request_id": "req_abc123"
  }
}
```

- `code`: A constant string identifying the error type. Used by clients for programmatic handling.
- `message`: A human-readable description suitable for display.
- `details`: Additional structured context (e.g., validation field errors). Null if not applicable.
- `request_id`: The request ID for tracing. Always included.

## 13.3 Error Code Registry

| HTTP Status | Error Code | Scenario |
|:-----------:|-----------|---------|
| 401 | `AUTHENTICATION_REQUIRED` | No token provided |
| 401 | `TOKEN_EXPIRED` | Access token expired |
| 401 | `TOKEN_INVALID` | Token signature invalid or malformed |
| 401 | `INVALID_CREDENTIALS` | Wrong email or password |
| 401 | `REFRESH_TOKEN_EXPIRED` | Refresh token expired or revoked |
| 403 | `ACCOUNT_DEACTIVATED` | User account is deactivated |
| 403 | `INSUFFICIENT_PERMISSIONS` | Role does not permit this action |
| 403 | `ACCESS_DENIED` | Authenticated but resource is out of scope (e.g., manager accessing another team) |
| 404 | `ORGANIZATION_NOT_FOUND` | Organization not found |
| 404 | `EMPLOYEE_NOT_FOUND` | Employee not found (or in another org) |
| 404 | `WORK_ENTRY_NOT_FOUND` | Work entry not found |
| 404 | `ATTENDANCE_RECORD_NOT_FOUND` | Attendance record not found |
| 404 | `LEAVE_TYPE_NOT_FOUND` | Leave type not found |
| 404 | `LEAVE_REQUEST_NOT_FOUND` | Leave request not found |
| 409 | `ORGANIZATION_NAME_CONFLICT` | Organization name already taken |
| 409 | `EMAIL_ALREADY_EXISTS` | Email already registered in this org |
| 409 | `EMPLOYEE_ALREADY_INACTIVE` | Attempting to deactivate an already inactive employee |
| 409 | `ALREADY_CHECKED_IN` | Employee already checked in today |
| 409 | `ALREADY_CHECKED_OUT` | Employee already checked out today |
| 409 | `OVERLAPPING_LEAVE` | Requested dates overlap with existing active leave |
| 409 | `INSUFFICIENT_LEAVE_BALANCE` | Not enough leave balance to cover the request |
| 409 | `LEAVE_REQUEST_NOT_PENDING` | Attempting to approve/reject a non-pending request |
| 422 | `VALIDATION_ERROR` | Pydantic validation failure |
| 422 | `WORK_ENTRY_LOCKED` | Work entry is past the 24-hour edit window |
| 422 | `CANNOT_DEACTIVATE_SOLE_ADMIN` | Attempted to deactivate the only admin |
| 422 | `TIMEZONE_CHANGE_NOT_SUPPORTED` | Attempted to change org timezone |
| 422 | `RESET_TOKEN_INVALID` | Password reset token invalid or already used |
| 500 | `INTERNAL_SERVER_ERROR` | Unexpected error; safe generic response |

## 13.4 Centralized Exception Handler Architecture

- All application-defined exceptions inherit from a `BaseAppException` class defined in `app/core/exceptions.py`.
- `BaseAppException` carries: `error_code`, `message`, `http_status_code`, optional `details`.
- A single FastAPI exception handler registered in `app/main.py` catches `BaseAppException` and returns the standard error JSON.
- A separate handler catches `RequestValidationError` (Pydantic) and formats it to the standard `VALIDATION_ERROR` structure.
- A catch-all handler for `Exception` logs the full traceback and returns `INTERNAL_SERVER_ERROR` with a safe message (no internal details exposed).

## 13.5 Business vs System Errors

| Type | Handling |
|------|---------|
| Business errors | Raised as specific `BaseAppException` subclasses in the service layer |
| Validation errors | Automatically caught by FastAPI / Pydantic; formatted by the global handler |
| Database constraint violations | Caught in repository; translated to appropriate business exceptions |
| Unexpected errors | Caught by catch-all; logged with full traceback; safe 500 returned |

---

# 14. Service & Repository Architecture

## 14.1 Layer Responsibilities

### API / Router
**Owns:** HTTP request/response handling  
**Responsibilities:**
- Extract path params, query params, request body from the HTTP request
- Call the appropriate service method with validated data
- Return the appropriate Pydantic response schema

**Must NOT:**
- Contain business logic (no if/else for business rules)
- Access the database directly
- Import other modules' routers

---

### Schema (Pydantic)
**Owns:** Data contract for the API surface  
**Responsibilities:**
- Define the expected shape and types of request inputs
- Define the shape of API responses
- Enforce basic syntactic validation (required fields, type coercion, format checks)

**Must NOT:**
- Contain business logic
- Reference ORM models directly
- Perform database lookups

---

### Service
**Owns:** Business logic for the domain  
**Responsibilities:**
- Enforce business rules (e.g., "an employee cannot be their own manager")
- Orchestrate one or more repository calls within a single transaction
- Coordinate cross-module actions (e.g., calling AttendanceService from LeaveService)
- Raise domain-specific exceptions when business rules are violated
- Perform authorization scope checks (e.g., verify the requesting manager owns the target employee)

**Must NOT:**
- Contain SQL queries
- Import or instantiate HTTP request/response objects
- Call another module's repository directly

---

### Repository
**Owns:** Data access logic  
**Responsibilities:**
- Execute all SQL queries through SQLAlchemy ORM
- Always include `organization_id` in all tenant-scoped queries
- Return ORM model instances or typed result objects
- Translate database constraint violations (IntegrityError) into application exceptions

**Must NOT:**
- Contain business rules
- Call other repositories across module boundaries
- Receive or return HTTP objects

---

### Model (ORM)
**Owns:** Database schema definition  
**Responsibilities:**
- Define tables, columns, types, constraints, and relationships
- Provide SQLAlchemy relationship helpers for eager loading
- Serve as the data transfer object between repositories and services

**Must NOT:**
- Contain business logic
- Reference another module's models in its class body (relationships are defined as strings to avoid circular imports)

---

### Database
**Owns:** Data persistence and integrity  
**Responsibilities:**
- Enforce constraints (unique, foreign key, check)
- Provide ACID transaction guarantees
- Execute queries efficiently via indexes

## 14.2 Request Flow

```text
Client
  ↓ HTTP Request
FastAPI Router
  ↓ Extract + validate request (Pydantic schema)
Service (dependency-injected via Depends)
  ↓ Authorization scope check (tenant + role)
  ↓ Business rule validation
Repository (injected from db session)
  ↓ ORM query with organization_id filter
PostgreSQL
  ↓ Result set
Repository
  ↓ Return ORM model(s)
Service
  ↓ (optional) cross-module service call
  ↓ Return domain result
Router
  ↓ Serialize via Pydantic response schema
Client ← HTTP Response
```

## 14.3 Where Business Logic Lives

**Lives in the Service layer:**
- Checking leave balance before approving a request
- Verifying a manager owns the employee they are acting on
- Computing number of leave days excluding weekends
- Checking if a work entry is within the 24-hour edit window
- Determining if an employee has overlapping active leave

**Does NOT live in:**
- Routers: no `if role == "ADMIN"` checks
- Repositories: no balance validation before executing a query
- ORM Models: no computed properties that enforce business rules
- Schemas: no database lookups; syntactic validation only

---

# 15. Cross-Module Dependencies

## 15.1 Dependency Graph

```text
                     ┌─────────────────────────────┐
                     │         Organization          │
                     └───────────────┬──────────────┘
                                     │ (all modules depend on org)
              ┌──────────────────────┼─────────────────────┐
              ▼                      ▼                      ▼
           Auth               Leave Policy           (config context)
              │               (org-owned)
              ▼
            User
              │
              ▼
          Employee
         /    |    \
        /     |     \
       ▼      ▼      ▼
Work       Attendance  Leave
Tracker       ▲          │
              │          │ (on approve/grant, Leave → Attendance)
              └──────────┘

Dashboard
  ◄── Employee (read)
  ◄── Work Tracker (read)
  ◄── Attendance (read)
  ◄── Leave (read)
```

## 15.2 Hard Dependencies

| Module | Depends On | Nature |
|--------|-----------|--------|
| Auth | Organization | User must have an org |
| Employees | Organization, Auth | Employee references User and Org |
| Work Tracker | Organization, Employees | Work entry references Employee and Org |
| Attendance | Organization, Employees | Record references Employee and Org |
| Leave | Organization, Employees, Attendance | Balance/record reference Employee; on approve → writes to Attendance |
| Dashboard | All modules | Read aggregation from all |

## 15.3 Cross-Module Service Calls

| Caller | Called | Method | When |
|--------|--------|--------|------|
| Organization Service | Auth Service | `create_admin_user()` | On org registration |
| Employee Service | Auth Service | `create_user()` | On employee creation |
| Employee Service | Auth Service | `revoke_all_tokens()` | On employee deactivation |
| Leave Service | Attendance Service | `mark_leave_for_dates()` | On leave approval or grant |

## 15.4 Circular Dependency Prevention

- **Rule:** Services may call services, but never in a cycle. A → B → A is forbidden.
- **Attendance Service** does not call Leave Service (Leave writes to Attendance, not vice versa).
- **Auth Service** does not call Employee Service (Employee calls Auth, not vice versa).
- **Dashboard Service** only reads from other services; it never triggers writes.
- Module dependency direction follows the graph above — always downstream, never circular.

## 15.5 Shared Entities

`organization_id` is a shared concept — every module uses it for scoping. The Organization module owns the record; other modules reference it by foreign key without importing the Organization ORM model directly.

---

# 16. Background Jobs

## 16.1 MVP Background Processing Assessment

Two types of background processing are needed for MVP:

### Type A: Event-triggered async tasks (run after an HTTP request completes)
These can use FastAPI's built-in `BackgroundTasks` for MVP.

### Type B: Scheduled/periodic tasks (run on a timer, independent of requests)
These require an in-process scheduler (APScheduler) for MVP. Migrate to Celery/Redis when scale demands.

## 16.2 Job Classification

| Job | Trigger | Type | MVP Mechanism | Future Mechanism |
|-----|---------|:----:|:-------------:|:----------------:|
| Send invite email (new employee) | HTTP request completes | Event-triggered | `BackgroundTasks` | Celery |
| Send password reset email | HTTP request completes | Event-triggered | `BackgroundTasks` | Celery |
| Mark absent employees at end-of-day | Daily schedule (org timezone) | Scheduled | APScheduler | Celery beat |
| Run leave auto-allocation | Monthly / quarterly / annual schedule | Scheduled | APScheduler | Celery beat |
| Revoke all tokens on deactivation | HTTP request (synchronous) | Synchronous | Direct service call | — |

## 16.3 End-of-Day Absence Marking (Scheduled)

- **When:** At the end of each business day (midnight in each organization's timezone, or a configurable cutoff time)
- **What:** For every active employee in every active organization that has no check-in record for today and no approved/granted leave today → create an attendance record with status = ABSENT
- **MVP approach:** APScheduler job running in the same process; queries organizations and processes each
- **Risk:** For MVP scale (few organizations), in-process is fine. At scale (hundreds of organizations), extract to a proper job queue

## 16.4 Leave Auto-Allocation (Scheduled)

- **When:** On the first day of each allocation period (monthly = 1st of month, quarterly = 1st of quarter, annually = 1st of leave year)
- **What:** For each active organization with a leave policy, for each active employee that meets the minimum tenure requirement, credit their leave balance up to the cap
- **MVP approach:** APScheduler job; runs on a simple cron
- **Data risk:** This job modifies leave balances. It must be idempotent — running it twice for the same period must not double-credit. Track allocations with a log table (future) or use the balance + period as a uniqueness anchor

## 16.5 Celery / Redis Introduction Criteria

Introduce Celery + Redis when:
- Any single scheduled job takes longer than 30 seconds to complete
- Email delivery reliability becomes a customer issue
- The number of organizations exceeds ~100 (in-process scheduler becomes a bottleneck)

---

# 17. Configuration Management

## 17.1 Configuration Approach

All configuration is managed via **Pydantic Settings** (`pydantic-settings`), which reads from environment variables and `.env` files. The settings class is a single typed model in `app/core/config.py`. No configuration is hardcoded anywhere in the application.

## 17.2 Configuration Categories

### Application
- `APP_NAME` — Application name (used in logging and OpenAPI docs)
- `APP_ENV` — Environment identifier: `development` / `staging` / `production`
- `DEBUG` — Boolean; enables debug mode in development only
- `API_V1_PREFIX` — `/api/v1`

### Database
- `DATABASE_URL` — Full PostgreSQL async connection string (e.g., `postgresql+asyncpg://user:pass@host/db`)
- `DATABASE_POOL_SIZE` — Connection pool size (default: 10)
- `DATABASE_MAX_OVERFLOW` — Max overflow connections (default: 20)
- `DATABASE_ECHO` — Boolean; log SQL queries in development only

### Authentication / Security
- `JWT_SECRET_KEY` — Secret key for JWT signing. **Must be long, random, and rotated periodically.**
- `JWT_ALGORITHM` — Signing algorithm (default: `HS256`; migrate to `RS256` in Post-MVP)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — Default: 15
- `REFRESH_TOKEN_EXPIRE_DAYS` — Default: 7
- `PASSWORD_RESET_TOKEN_EXPIRE_HOURS` — Default: 1

### Email
- `EMAIL_PROVIDER` — e.g., `smtp` / `sendgrid` / `resend`
- `EMAIL_FROM_ADDRESS` — Sender email address
- `EMAIL_FROM_NAME` — Sender name
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` — SMTP credentials (or provider API key)

### CORS
- `CORS_ALLOWED_ORIGINS` — Comma-separated list of allowed frontend origins

### Logging
- `LOG_LEVEL` — `DEBUG` / `INFO` / `WARNING` / `ERROR`
- `LOG_FORMAT` — `json` (production) / `console` (development)

### Background Jobs
- `SCHEDULER_ENABLED` — Boolean; disable in test environments
- `ABSENCE_MARK_CRON` — Cron expression for end-of-day absence marking (default: `0 23 * * *` UTC as baseline)
- `LEAVE_ALLOCATION_CRON` — Cron expression for leave allocation runner

## 17.3 Secrets Management

- In development: secrets stored in `.env` file (never committed to version control). `.env.example` documents all required variables without values.
- In production: secrets injected via environment variables from the deployment platform (e.g., AWS Secrets Manager, GCP Secret Manager, Railway/Render secret variables).
- **Never:** hardcode secrets; commit `.env` files; log secret values.

## 17.4 Environment Separation

| Setting | Development | Staging | Production |
|---------|:-----------:|:-------:|:----------:|
| `DEBUG` | `true` | `false` | `false` |
| `DATABASE_ECHO` | `true` | `false` | `false` |
| `LOG_FORMAT` | `console` | `json` | `json` |
| `CORS_ALLOWED_ORIGINS` | `*` | specific origin | specific origin |
| JWT secret rotation | Not required | Recommended | **Required** |

---

# 18. Logging & Observability

## 18.1 MVP Logging Strategy

**Tool:** `structlog` with JSON output format in production; human-readable console format in development.

**Log destination:** `stdout` in MVP (consumed by the deployment platform's log aggregation).

## 18.2 Standard Log Fields

Every log entry includes:

| Field | Value |
|-------|-------|
| `timestamp` | ISO 8601 UTC |
| `level` | `INFO` / `WARNING` / `ERROR` / `DEBUG` |
| `request_id` | Unique ID per HTTP request |
| `organization_id` | Tenant ID (when authenticated) |
| `user_id` | Authenticated user ID (when authenticated) |
| `module` | Source module name |
| `event` | Short description of the event |

## 18.3 What to Log (MVP)

### Request Lifecycle
- Incoming request: method, path, user ID, org ID, request ID
- Response: status code, duration in milliseconds
- Exceptions: full traceback at ERROR level (never exposed to clients)

### Authentication Events
- Successful login (user ID, org ID)
- Failed login attempt (email only; no password)
- Token refresh
- Logout
- Password reset requested / completed
- Account deactivated

### Business Events (INFO level)
- Employee created / deactivated
- Leave request submitted / approved / rejected / granted
- Manual attendance correction (who corrected, which record, reason)
- Leave auto-allocation run completed (org ID, number of employees processed)
- Absence marking job completed (org ID, number of records created)

### Error Events
- Database constraint violation (with error details, without exposing raw SQL to logs)
- Unexpected exceptions (full traceback)
- Email delivery failures

## 18.4 What NOT to Log (Ever)

- Passwords (plaintext or hashed)
- JWT tokens or refresh tokens
- Password reset tokens
- Any PII beyond what is strictly necessary for debugging (e.g., full addresses, personal documents)

## 18.5 Request ID Middleware

A middleware in `app/main.py` assigns a `X-Request-ID` UUID to every incoming request. This ID is:
- Added to all log entries during the request lifecycle via `structlog` context binding
- Returned in the `X-Request-ID` response header
- Included in all error responses for client-side tracing

## 18.6 Future Observability (Post-MVP)

| Capability | Tool | When |
|-----------|------|------|
| Error monitoring | Sentry | First production incidents |
| Metrics | Prometheus + Grafana | When dashboard load becomes a concern |
| Distributed tracing | OpenTelemetry | When microservices are introduced |
| Log aggregation | Datadog / Elastic | When log volume makes stdout insufficient |
| Alerting | PagerDuty / Opsgenie | When SLAs are defined |

---

# 19. Security Architecture

## 19.1 Security Checklist

### Password Security
| Item | Status |
|------|:------:|
| Passwords hashed with bcrypt (cost factor ≥ 12) | **Must-have before production** |
| Passwords never stored in plaintext | **Must-have before production** |
| Passwords never logged | **Must-have before production** |
| Minimum password length enforced (≥ 8 characters) | **Must-have before production** |
| Password reset tokens are single-use and time-limited (1 hour) | **Must-have before production** |

### Token Security
| Item | Status |
|------|:------:|
| JWT signed with strong secret (≥ 256-bit random) | **Must-have before production** |
| Access tokens short-lived (15 minutes) | **Must-have before production** |
| Refresh tokens stored as hashed values in database | **Must-have before production** |
| Refresh tokens are revocable | **Must-have before production** |
| JWT secret rotated periodically | **Can be added later** (tooling) |
| RS256 (asymmetric) JWT signing | **Can be added later** |
| MFA | **Can be added later** |

### Authentication
| Item | Status |
|------|:------:|
| All non-public endpoints require valid JWT | **Must-have before production** |
| Deactivated accounts cannot authenticate | **Must-have before production** |
| Password reset does not confirm email existence (timing-safe response) | **Must-have before production** |
| Login rate limiting | **Must-have before production** |

### Authorization
| Item | Status |
|------|:------:|
| Role-based access enforced at route level | **Must-have before production** |
| Scope-based access enforced at service level | **Must-have before production** |
| Cross-tenant resource access returns 404 (not 403) | **Must-have before production** |
| Admin cannot be deactivated if sole admin | **Must-have before production** |

### Tenant Isolation
| Item | Status |
|------|:------:|
| `organization_id` in JWT, not modifiable by client | **Must-have before production** |
| All tenant-scoped queries include `organization_id` filter | **Must-have before production** |
| Tenant isolation test suite passes | **Must-have before production** |
| Row-level security (PostgreSQL RLS) | **Can be added later** |

### Input Validation
| Item | Status |
|------|:------:|
| All inputs validated by Pydantic before service layer | **Must-have before production** |
| SQL injection prevention via ORM parameterized queries | **Must-have before production** |
| No raw string interpolation in SQL | **Must-have before production** |

### Transport Security
| Item | Status |
|------|:------:|
| HTTPS enforced in production (TLS termination at load balancer) | **Must-have before production** |
| CORS configured to allow only known frontend origins | **Must-have before production** |
| `Strict-Transport-Security` header | **Must-have before production** |
| `X-Content-Type-Options: nosniff` header | **Recommended** |
| `X-Frame-Options: DENY` header | **Recommended** |

### API Abuse
| Item | Status |
|------|:------:|
| Rate limiting on login endpoint | **Must-have before production** |
| Rate limiting on password reset endpoint | **Must-have before production** |
| General API rate limiting | **Can be added later** |
| API key / service account mechanism | **Can be added later** |

### Secrets
| Item | Status |
|------|:------:|
| No secrets in source code or version control | **Must-have before production** |
| `.env` files excluded from git | **Must-have before production** |
| Secrets injected via environment variables in production | **Must-have before production** |
| Secret rotation process defined | **Recommended** |

---

# 20. Testing Architecture

## 20.1 Testing Strategy

The testing strategy follows a **pyramid model**: many unit tests, fewer integration tests, selective end-to-end tests, dedicated security tests.

## 20.2 Test Types

### Unit Tests (`tests/unit/`)
- **Target:** Service layer (business logic)
- **Approach:** Mock all repository calls; test business logic in isolation
- **What to test:** Business rule enforcement (balance checks, scope validation, lock enforcement), edge cases, exception raising

### Integration Tests (`tests/integration/`)
- **Target:** Each module's full stack (router → service → repository → test database)
- **Approach:** Use a real PostgreSQL test database (separate from dev/prod); wrap each test in a rollback transaction
- **What to test:** Full CRUD operations, permission enforcement at the API level, correct HTTP status codes and error codes

### End-to-End Tests (`tests/e2e/`)
- **Target:** Critical cross-module workflows
- **What to test:**
  - Organization registration → employee creation → login flow
  - Leave request → manager approval → attendance updated
  - Employee deactivation → session invalidated → all records preserved

### Security Tests (`tests/security/test_tenant_isolation.py`)
- **Purpose:** Verify that no API endpoint can be used to access data from a different organization
- **Approach:** Create two organizations; authenticate as a user from Org A; attempt to access resources belonging to Org B using valid Org B IDs; verify 404 is returned for all attempts
- **This test suite must pass before every release**

### Authentication Tests
- **Target:** Auth module
- **What to test:** Login success/failure, token refresh, logout, password reset flow, deactivated account handling

## 20.3 Test Infrastructure

- **Test database:** PostgreSQL instance dedicated to testing; schema applied via Alembic before test run
- **Fixtures:** `conftest.py` provides: async test client, database session, organization factory, authenticated user factory (admin, manager, employee)
- **Isolation:** Each integration test runs within a transaction that is rolled back on completion — no test-to-test data contamination
- **Async:** All tests use `pytest-asyncio` with `asyncio_mode = "auto"`

## 20.4 Recommended Test Structure

```text
tests/
├── conftest.py                          # Shared fixtures
├── unit/
│   ├── services/
│   │   ├── test_leave_service.py        # Balance check, overlap, allocation logic
│   │   ├── test_attendance_service.py   # Status state machine, timezone handling
│   │   ├── test_employee_service.py     # Manager assignment, deactivation rules
│   │   └── test_work_entry_service.py   # Lock enforcement, scope rules
│   └── utils/
│       └── test_datetime_utils.py
├── integration/
│   ├── test_organization.py
│   ├── test_auth.py
│   ├── test_employees.py
│   ├── test_work_tracker.py
│   ├── test_attendance.py
│   ├── test_leave.py
│   └── test_dashboard.py
├── e2e/
│   ├── test_organization_onboarding.py  # Full org registration → employee login
│   ├── test_leave_workflow.py           # Submit → approve → attendance updated
│   └── test_employee_lifecycle.py      # Create → deactivate → records preserved
└── security/
    └── test_tenant_isolation.py         # Cross-org access prevention
```

## 20.5 Minimum Coverage for MVP Release

| Area | Minimum Coverage |
|------|:----------------:|
| Service layer (unit tests) | 80% |
| All API endpoints (integration tests) | 100% (every endpoint has at least one test) |
| All critical workflows (e2e tests) | 100% (all 3 workflows covered) |
| Tenant isolation (security tests) | 100% (all modules tested) |
| Happy path + top 3 error cases per endpoint | **Required** |

---

# 21. API Versioning & Backward Compatibility

## 21.1 Version Strategy

**URL-based versioning:** `/api/v1/` prefix for all MVP APIs.

The FastAPI router is structured so that all v1 routers are registered under the `/api/v1` prefix as an `APIRouter`. When v2 is needed, a separate `APIRouter` for `/api/v2` is mounted alongside v1.

## 21.2 Breaking vs Non-Breaking Changes

### Non-Breaking Changes (safe in v1)
- Adding new optional fields to request schemas
- Adding new fields to response schemas
- Adding new endpoints to existing resources
- Expanding enum values that are additive

### Breaking Changes (require v2)
- Removing or renaming existing fields from request/response schemas
- Changing the type of an existing field
- Removing endpoints
- Changing error code values or HTTP status codes for existing errors
- Changing pagination behavior (e.g., switching from offset to cursor)

## 21.3 MVP Stance

- In MVP, all APIs are v1. No v2 concern during initial development.
- A **changelog** must be maintained in `docs/api-changelog.md` from the first public release.
- Any breaking change after the first external customer onboards triggers a v2 pathway.

## 21.4 Deprecation Strategy (Post-MVP)

1. Mark the v1 endpoint as deprecated in OpenAPI docs (`deprecated=True` in FastAPI)
2. Add `Deprecation` and `Sunset` headers to responses
3. Maintain v1 for a minimum 60-day sunset window after v2 is available
4. Remove v1 only after sunset date

---

# 22. Migration Strategy

## 22.1 Migration Tool

**Alembic** manages all PostgreSQL schema changes. Alembic's `env.py` imports the SQLAlchemy `Base` from `app/db/base.py`, which imports all ORM models.

## 22.2 Migration Naming Convention

```text
<revision_id>_<yyyymmdd>_<short_description>.py
```
Example: `a3f2c1d4_20240115_create_employees_table.py`

The descriptive suffix uses underscores; it should describe the purpose of the migration, not the SQL operation.

## 22.3 Migration Ownership

- Migrations are owned by the module that owns the affected tables.
- A migration must never modify a table it does not own.
- Migrations are sequential and linear in MVP (no branches).

## 22.4 Development Workflow

1. Developer modifies ORM models in the relevant module's `models.py`
2. Developer runs `alembic revision --autogenerate -m "description"` to generate the migration
3. Developer **reviews the generated migration carefully** — autogenerate is a starting point, not a guarantee of correctness
4. Developer runs `alembic upgrade head` locally to verify the migration applies cleanly
5. Developer commits both the model change and the migration file together in one commit

## 22.5 Production Workflow

1. Migration files are committed to version control
2. On deployment, `alembic upgrade head` runs automatically before the application starts
3. Migrations are applied in order; the application starts only after migrations succeed

## 22.6 Rollback Considerations

- Alembic supports `alembic downgrade -1` for rolling back one migration
- Each migration must have a valid `downgrade()` function
- **Destructive operations (DROP TABLE, DROP COLUMN) are not executed in MVP without an explicit data backup step**
- For safety, prefer additive migrations (add new columns as nullable first; backfill; add NOT NULL constraint in a subsequent migration)

## 22.7 Data Migrations

- Data migrations (transforming existing rows) are separate from schema migrations
- Data migrations are idempotent (running twice does not corrupt data)
- Data migrations are placed in `alembic/versions/` with the naming prefix `data_` to distinguish them from schema migrations
- For large tables, data migrations are done in batches to avoid table locks

---

# 23. Development Workflow

## 23.1 Recommended Implementation Sequence

```text
Phase 1 — Project Foundation
         ↓
Phase 2 — Database Foundation & Core Infrastructure
         ↓
Phase 3 — Organization Module
         ↓
Phase 4 — Authentication Module
         ↓
Phase 5 — Employee Module
         ↓
Phase 6 — Work Tracker Module
         ↓
Phase 7 — Attendance Module
         ↓
Phase 8 — Leave Module
         ↓
Phase 9 — Dashboard Module
         ↓
Phase 10 — Cross-Module Integration Testing
          ↓
Phase 11 — Security Review & Hardening
          ↓
Phase 12 — MVP Release
```

## 23.2 Why This Order

| Reason | Explanation |
|--------|------------|
| Organization first | Every other entity has an `organization_id` FK. Without organizations, nothing can be created. |
| Auth second | Every API except registration is protected. Auth infrastructure (JWT, password hashing, dependencies) must exist before any other module's routes can be tested. |
| Employees third | Work entries, attendance records, and leave records all require a valid employee. Without Employee, the next three modules cannot be properly tested. |
| Work Tracker before Attendance | Work Tracker has no cross-module writes; it is the simplest operational module to validate the module pattern |
| Attendance before Leave | Leave writes to Attendance on approval. Attendance must be complete and stable before Leave's cross-module integration is built. |
| Leave last | Leave is the most complex module: multiple repositories, cross-module write, scheduled job, balance management. Build it last on top of a stable foundation. |
| Dashboard last | Dashboard aggregates from all other modules. It cannot be built until all other modules expose stable service interfaces. |

---

# 24. MVP vs Future Architecture

| Capability | MVP | Later | Reason |
|-----------|:---:|:-----:|--------|
| Email/password login | ✅ | | Core authentication |
| JWT access + refresh tokens | ✅ | | Standard SaaS session management |
| Three fixed roles (Admin/Manager/Employee) | ✅ | | Sufficient for MVP permission model |
| Single-database, shared schema multi-tenancy | ✅ | | Fastest safe isolation for MVP |
| Modular monolith | ✅ | | Right size for a small team; avoids microservices overhead |
| Organization registration | ✅ | | Bootstrap entry point |
| Employee management (create, update, deactivate) | ✅ | | Core HR data |
| Work entry logging | ✅ | | Core feature 1 |
| Attendance check-in/check-out | ✅ | | Core feature 2 |
| Automatic absence marking (scheduled) | ✅ | | Ensures attendance records are complete |
| Leave request + approval workflow | ✅ | | Core feature 3 |
| Manager direct grant | ✅ | | Necessary for manager discretion |
| Leave auto-allocation (policy-driven) | ✅ | | Policy fairness; differentiator |
| Leave → Attendance cross-module update | ✅ | | Data consistency |
| Role-scoped dashboards (summary only) | ✅ | | Operational visibility |
| FastAPI `BackgroundTasks` for email | ✅ | | Simple; sufficient for MVP |
| APScheduler for cron jobs | ✅ | | Simple in-process scheduler |
| structlog JSON logging | ✅ | | Production observability baseline |
| Offset pagination | ✅ | | Simple; sufficient for MVP data volumes |
| Social login (Google, GitHub) | | ✅ | Not launch-critical |
| Enterprise SSO (SAML/OIDC) | | ✅ | Enterprise feature |
| MFA | | ✅ | Security enhancement |
| Granular / custom RBAC | | ✅ | Three fixed roles sufficient for MVP |
| Multiple admins per org | | ✅ | Not required for MVP trust model |
| CSV bulk import | | ✅ | Useful but not launch-critical |
| Holiday calendar | | ✅ | Adds complexity to attendance calculations |
| Shift management | | ✅ | Different problem space |
| Carry-forward leave balance | | ✅ | Adds year-boundary complexity |
| Leave encashment | | ✅ | Requires payroll integration |
| Half-day leave | | ✅ | Adds fractional balance complexity |
| Payroll module | | ✅ | Separate, complex domain |
| Performance management | | ✅ | Out of MVP scope |
| Celery + Redis | | ✅ | When APScheduler is insufficient |
| Cursor-based pagination | | ✅ | When data volumes justify it |
| PostgreSQL Row-Level Security | | ✅ | Defense-in-depth addition |
| Redis caching | | ✅ | When dashboard queries become slow |
| Sentry error monitoring | | ✅ | First production incidents |
| Prometheus / Grafana metrics | | ✅ | Post-launch performance visibility |
| OpenTelemetry tracing | | ✅ | When microservices are introduced |
| Separate database per tenant | | ✅ | Only with strict compliance requirements |
| API rate limiting (global) | | ✅ | When abuse patterns emerge |
| Audit log | | ✅ | Compliance feature |
| Export (CSV/PDF) | | ✅ | Reporting enhancement |

---

# 25. Production Readiness Checklist

## Architecture
| Item | Priority |
|------|:--------:|
| Modular structure is maintained; no cross-module repo imports | **Required MVP** |
| Services contain all business logic; routers contain none | **Required MVP** |
| All modules can be independently understood by a new developer | **Required MVP** |
| Database session is managed per-request (not shared across requests) | **Required MVP** |

## Database
| Item | Priority |
|------|:--------:|
| All migrations applied cleanly from a fresh database | **Required MVP** |
| All tables have `organization_id` FK where applicable | **Required MVP** |
| All required indexes created | **Required MVP** |
| All unique constraints defined | **Required MVP** |
| Foreign key constraints enforced at database level | **Required MVP** |
| No raw SQL string interpolation | **Required MVP** |
| Alembic downgrade functions are valid for all migrations | **Recommended** |
| Connection pool properly configured | **Required MVP** |

## Authentication
| Item | Priority |
|------|:--------:|
| bcrypt hashing with cost factor ≥ 12 | **Required MVP** |
| JWT signed with ≥ 256-bit random secret | **Required MVP** |
| Access token expiry ≤ 15 minutes | **Required MVP** |
| Refresh token revocation functional | **Required MVP** |
| Deactivated accounts cannot authenticate | **Required MVP** |
| Password reset is single-use and 1-hour expiry | **Required MVP** |
| Password reset response is timing-safe | **Required MVP** |

## Authorization
| Item | Priority |
|------|:--------:|
| Role checks on all protected routes | **Required MVP** |
| Manager scope checks in all team-access services | **Required MVP** |
| Cross-org resource requests return 404 | **Required MVP** |
| Sole admin deactivation prevention | **Required MVP** |

## Tenant Isolation
| Item | Priority |
|------|:--------:|
| `organization_id` included in all tenant-scoped queries | **Required MVP** |
| Tenant isolation security test suite passes | **Required MVP** |
| JWT `organization_id` validated on every request | **Required MVP** |

## API
| Item | Priority |
|------|:--------:|
| All 39 APIs implemented and returning correct status codes | **Required MVP** |
| OpenAPI documentation generated and accurate | **Recommended** |
| Request IDs on all responses | **Required MVP** |
| Pagination on all list endpoints | **Required MVP** |

## Validation
| Item | Priority |
|------|:--------:|
| All request inputs validated by Pydantic | **Required MVP** |
| Validation errors return 422 with field-level details | **Required MVP** |

## Error Handling
| Item | Priority |
|------|:--------:|
| All errors return consistent `{ error: { code, message } }` structure | **Required MVP** |
| No internal stack traces exposed to clients | **Required MVP** |
| Database errors translated to business exceptions | **Required MVP** |

## Logging
| Item | Priority |
|------|:--------:|
| JSON structured logging in production | **Required MVP** |
| Request ID on all log entries | **Required MVP** |
| Authentication events logged | **Required MVP** |
| No passwords or tokens logged | **Required MVP** |

## Testing
| Item | Priority |
|------|:--------:|
| 80%+ service layer test coverage | **Required MVP** |
| 100% API endpoint integration test coverage | **Required MVP** |
| All 3 e2e workflows covered | **Required MVP** |
| Tenant isolation tests pass | **Required MVP** |

## Security
| Item | Priority |
|------|:--------:|
| HTTPS in production | **Required MVP** |
| CORS configured for known origins only | **Required MVP** |
| Rate limiting on login + password reset | **Required MVP** |
| Secrets not in source code | **Required MVP** |
| Security headers (`HSTS`, `X-Content-Type-Options`) | **Required MVP** |

## Performance
| Item | Priority |
|------|:--------:|
| Database connection pool configured | **Required MVP** |
| All required indexes in place | **Required MVP** |
| No N+1 query patterns in list endpoints | **Required MVP** |
| Dashboard queries do not perform full table scans | **Required MVP** |

## Deployment
| Item | Priority |
|------|:--------:|
| `alembic upgrade head` runs before app start | **Required MVP** |
| Application starts and serves health check | **Required MVP** |
| Environment variables documented in `.env.example` | **Required MVP** |
| Graceful shutdown handled | **Recommended** |

## Backup / Recovery
| Item | Priority |
|------|:--------:|
| Daily automated database backups configured | **Required MVP** |
| Backup restoration tested | **Required MVP** |
| Recovery time objective (RTO) documented | **Recommended** |

---

# 26. Recommended Implementation Sequence

## Phase 1 — Project Foundation
**Objective:** Working FastAPI application skeleton with configuration, logging, and database connection.

**Deliverables:**
- Project scaffolded per the directory structure in Section 4
- Pydantic Settings configured and loading from environment
- PostgreSQL connection pool established and verified
- structlog configured for console (dev) and JSON (prod) output
- `GET /api/v1/health` returns 200 with app status
- Alembic initialized; `env.py` configured; `alembic upgrade head` runs on empty db
- Base exception classes and global exception handlers registered

**Dependencies:** None — this is the foundation.

**Exit Criteria:** `GET /api/v1/health` returns 200; Alembic commands succeed; config loads from `.env`.

---

## Phase 2 — Organization Module
**Objective:** Multi-tenant foundation. Organizations can be registered.

**Modules involved:** Organization

**Deliverables:**
- `organizations` table and Alembic migration
- `POST /api/v1/organizations/register` — creates org + admin user + admin employee (atomically)
- `GET /api/v1/organizations/me` — returns org settings
- `PATCH /api/v1/organizations/me` — updates org name
- Integration tests for all 3 endpoints

**Dependencies:** Phase 1 complete.

**Exit Criteria:** An organization can be registered via API; integration tests pass.

---

## Phase 3 — Authentication Module
**Objective:** Users can log in and receive JWT tokens. All protected routes enforce authentication.

**Modules involved:** Auth

**Deliverables:**
- `users`, `refresh_tokens`, `password_reset_tokens` tables and migrations
- `POST /api/v1/auth/login` — returns access + refresh tokens
- `POST /api/v1/auth/refresh` — returns new access token
- `POST /api/v1/auth/logout` — revokes session
- `GET /api/v1/auth/me` — returns current user
- `POST /api/v1/auth/password-reset/request` and `/confirm`
- `get_current_user` FastAPI dependency wired and enforced on protected routes
- Auth integration tests; deactivated account test

**Dependencies:** Phase 2 (users belong to organizations).

**Exit Criteria:** Login, logout, refresh, and password reset all function correctly. Protected routes reject unauthenticated requests with 401.

---

## Phase 4 — Employee Module
**Objective:** Admin can manage the organization's employee directory.

**Modules involved:** Employees

**Deliverables:**
- `employees` table and migration
- `POST /api/v1/employees` — create employee
- `GET /api/v1/employees` — list employees (admin / manager scoped)
- `GET /api/v1/employees/{employee_id}` — get profile
- `PATCH /api/v1/employees/{employee_id}` — update profile
- `POST /api/v1/employees/{employee_id}/manager` — assign manager
- `POST /api/v1/employees/{employee_id}/deactivate` — deactivate
- Employee integration tests; deactivation cascade to auth test

**Dependencies:** Phase 3 (employees require users).

**Exit Criteria:** Admin can create, view, update, and deactivate employees. Manager scope enforced. Deactivated employee cannot log in.

---

## Phase 5 — Work Tracker Module
**Objective:** Employees can log daily work entries. Managers and admin can review team entries.

**Modules involved:** Work Tracker

**Deliverables:**
- `work_entries` table and migration
- `POST /api/v1/work-entries`
- `GET /api/v1/work-entries` (with date filter, scope filter)
- `GET /api/v1/work-entries/{entry_id}`
- `PATCH /api/v1/work-entries/{entry_id}` (24-hour lock enforced)
- Work tracker integration tests; lock enforcement test

**Dependencies:** Phase 4 (work entries require active employees).

**Exit Criteria:** Employees can create and view work entries; 24-hour lock enforced; scope rules verified.

---

## Phase 6 — Attendance Module
**Objective:** Employees can check in and out. Attendance is tracked per day. Absence marking works.

**Modules involved:** Attendance

**Deliverables:**
- `attendance_records` table and migration
- `POST /api/v1/attendance/check-in`
- `POST /api/v1/attendance/check-out`
- `GET /api/v1/attendance` (scoped by role, date filter)
- `GET /api/v1/attendance/{record_id}`
- `PATCH /api/v1/attendance/{record_id}/correct` (admin/manager manual correction)
- APScheduler end-of-day absence marking job wired
- Attendance integration tests; double check-in protection test; manual correction test

**Dependencies:** Phase 4 (attendance requires employees). Phase 6 must be complete before Phase 7 can integrate with it.

**Exit Criteria:** Check-in/check-out work correctly; absence marking job executes; manual correction creates audit trail.

---

## Phase 7 — Leave Module
**Objective:** Full leave lifecycle operational: policy, balance, requests, approvals, grants, auto-allocation.

**Modules involved:** Leave (with cross-module write to Attendance)

**Deliverables:**
- `leave_types`, `leave_policy_rules`, `leave_balances`, `leave_records` tables and migrations
- All 13 leave endpoints implemented
- Leave → Attendance cross-module write (mark LEAVE status on approval/grant)
- APScheduler leave allocation job wired
- Leave service unit tests (balance, overlap, allocation logic)
- Leave integration tests; approval workflow test; leave→attendance integration test

**Dependencies:** Phase 6 complete (Leave writes to Attendance). Phase 4 (employees, joining_date).

**Exit Criteria:** Full leave workflow operational end-to-end; attendance records correctly updated on leave approval; auto-allocation job runs and credits balances correctly.

---

## Phase 8 — Dashboard Module
**Objective:** Each role sees a relevant operational summary.

**Modules involved:** Dashboard (reads from all other modules)

**Deliverables:**
- `GET /api/v1/dashboard` — returns role-scoped dashboard data
- Dashboard integration tests for each role (employee, manager, admin)

**Dependencies:** All previous phases complete.

**Exit Criteria:** Each role receives correct, scoped dashboard data.

---

## Phase 9 — Cross-Module Integration Testing
**Objective:** End-to-end workflows validated across module boundaries.

**Deliverables:**
- E2E test: Organization registration → employee creation → login → work entry → leave request → approval → attendance updated
- E2E test: Employee deactivation → session invalidated → historical records preserved
- Tenant isolation test suite passes: no cross-org data access possible

**Dependencies:** Phases 1–8 complete.

**Exit Criteria:** All e2e tests pass; tenant isolation tests pass.

---

## Phase 10 — Security Hardening & Production Readiness
**Objective:** System meets the security and production readiness checklist in Section 25.

**Deliverables:**
- Rate limiting on login and password reset endpoints
- Security headers configured (HSTS, X-Content-Type-Options)
- CORS configured for production origin
- No secrets in source code; `.env.example` complete
- All logging correct (no sensitive data in logs)
- Production Readiness Checklist (Section 25) reviewed and all "Required MVP" items checked

**Dependencies:** Phase 9 complete.

**Exit Criteria:** All "Required MVP" items in the Production Readiness Checklist are satisfied.

---

## Phase 11 — MVP Release
**Objective:** System is deployed and the first organization can onboard.

**Deliverables:**
- Production environment provisioned (PostgreSQL, app server)
- Automated database backups configured
- `alembic upgrade head` runs on deployment
- Health check endpoint monitored
- `.env.example` handed to operations team
- MVP release confirmed

---

# 27. Final Architecture Summary

## Architecture Decision Summary

| Decision | Choice | Rationale |
|---------|--------|-----------|
| Framework | FastAPI | Async, fast, OpenAPI-native, Pydantic integration |
| ORM | SQLAlchemy 2.x async | Battle-tested; Alembic integration; async support |
| Database | PostgreSQL | ACID, constraints, UUID support, excellent concurrency |
| Architecture style | Modular monolith | Right size for MVP team; avoids premature distribution |
| Multi-tenancy | Shared DB, row-level isolation | Simplest safe approach for MVP |
| Primary key type | UUID v4 | No sequential ID exposure; application-generatable |
| Auth mechanism | JWT (access) + opaque refresh token | Industry standard; revocable refresh tokens |
| JWT signing | HS256 (MVP) → RS256 (future) | Simple now; upgradeable |
| Role model | Three fixed roles | Sufficient; avoids RBAC engine complexity |
| Error format | `{ error: { code, message, details } }` | Machine-readable; consistent |
| Logging | structlog, JSON in prod | Structured; aggregation-ready |
| Background jobs | BackgroundTasks (event) + APScheduler (cron) | Sufficient for MVP scale |
| Pagination | Offset-based | Simple; sufficient for expected data volumes |
| API versioning | URL-based (`/api/v1/`) | Explicit; widely understood |
| Migration tool | Alembic | Tight SQLAlchemy integration; industry standard |
| Test strategy | Unit + integration + e2e + security | Balanced pyramid; practical for MVP |
| Password hashing | bcrypt (cost ≥ 12) | Gold standard |
| Soft delete | `is_active` flag | Preserves historical integrity |

---

## MVP Architecture Diagram

```text
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                    │
│                                                           │
│  ┌──────────────┐  ┌────────────────────────────────┐   │
│  │  Middleware   │  │           Modules               │   │
│  │ - Request ID  │  │  ┌─────────┐  ┌────────────┐  │   │
│  │ - CORS        │  │  │  Org    │  │    Auth    │  │   │
│  │ - Logging     │  │  └─────────┘  └────────────┘  │   │
│  └──────────────┘  │  ┌─────────┐  ┌────────────┐  │   │
│                     │  │Employee │  │ Work Track │  │   │
│  ┌──────────────┐  │  └─────────┘  └────────────┘  │   │
│  │  Core         │  │  ┌─────────┐  ┌────────────┐  │   │
│  │ - Config      │  │  │Attendance│  │   Leave    │  │   │
│  │ - Security    │  │  └─────────┘  └────────────┘  │   │
│  │ - Dependencies│  │  ┌─────────┐                  │   │
│  │ - Exceptions  │  │  │Dashboard│                  │   │
│  └──────────────┘  │  └─────────┘                  │   │
│                     └────────────────────────────────┘   │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Background Jobs                     │    │
│  │  APScheduler: absence marking, leave allocation  │    │
│  │  BackgroundTasks: email delivery                 │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │   PostgreSQL    │
                   │  (shared schema │
                   │  row-level iso) │
                   └─────────────────┘
```

---

## Module Dependency Map

```text
Organization (root tenant)
        │
        ├──────────────────────────────────────────┐
        │                                          │
      Auth                                     Leave Policy
        │                                      (owned by Org,
        │                                       executed by Leave)
        ▼
      User
        │
        ▼
    Employee ◄─── ManagerAssignment (self-ref)
        │
        ├──────────────────────┬───────────────────┐
        │                      │                   │
        ▼                      ▼                   ▼
  Work Tracker            Attendance ◄────────── Leave
  (no cross-module            ▲                   │
   writes)                    └───────────────────┘
                           (Leave writes LEAVE status
                            to AttendanceRecord on
                            approve/grant)
                               │
                         Dashboard ◄──────── All modules (read only)
```

---

## API Surface Summary

| Module | Endpoints |
|--------|:---------:|
| System | 1 |
| Organization | 3 |
| Authentication | 6 |
| Employees | 6 |
| Work Tracker | 4 |
| Attendance | 5 |
| Leave | 13 |
| Dashboard | 1 |
| **Total** | **39** |

---

## Database Entity Summary

| Entity | Table | Module | Tenant-Scoped |
|--------|-------|--------|:---:|
| Organization | `organizations` | Organization | No (IS the tenant) |
| User | `users` | Auth | ✅ |
| RefreshToken | `refresh_tokens` | Auth | Implicit |
| PasswordResetToken | `password_reset_tokens` | Auth | Implicit |
| Employee | `employees` | Employees | ✅ |
| WorkEntry | `work_entries` | Work Tracker | ✅ |
| AttendanceRecord | `attendance_records` | Attendance | ✅ |
| LeaveType | `leave_types` | Leave | ✅ |
| LeavePolicyRule | `leave_policy_rules` | Leave | ✅ |
| LeaveBalance | `leave_balances` | Leave | ✅ |
| LeaveRecord | `leave_records` | Leave | ✅ |

---

## Implementation Roadmap

```text
Week 1-2:   Phase 1 (Foundation) + Phase 2 (Organization)
Week 2-3:   Phase 3 (Authentication)
Week 3-4:   Phase 4 (Employees)
Week 4:     Phase 5 (Work Tracker)
Week 5:     Phase 6 (Attendance)
Week 6-7:   Phase 7 (Leave — most complex module)
Week 7:     Phase 8 (Dashboard)
Week 8:     Phase 9 (Integration & E2E Testing)
Week 8-9:   Phase 10 (Security Hardening)
Week 9:     Phase 11 (MVP Release)
```

---

## Architecture Risks

| Risk | Severity | Mitigation |
|------|:--------:|-----------|
| **Leave → Attendance cross-module write fails mid-transaction** | High | Wrap leave approval + attendance update in a single database transaction; if attendance write fails, the leave approval rolls back |
| **APScheduler in-process job crashes the app** | Medium | Catch and log all exceptions in scheduled jobs; jobs are non-blocking; implement heartbeat logging so failures are detectable |
| **Leave auto-allocation runs twice for the same period** | Medium | Use `(employee_id, leave_type_id, leave_year, allocation_period)` uniqueness in allocation tracking; make the job idempotent |
| **End-of-day absence marking uses wrong timezone** | High | Store all dates in the organization's configured timezone; use `pytz` or `zoneinfo` for conversion; test with multiple timezones |
| **manager_id self-referencing creates query cycles** | Low | Enforce `manager_id != employee_id` at database level with a `CHECK` constraint; ORM-level validation as a second layer |
| **Tenant isolation breach via missing organization_id filter** | Critical | All repository methods require `organization_id` parameter; tenant isolation test suite runs on every CI build |
| **Refresh token theft enables long-lived session hijacking** | High | Store refresh tokens as bcrypt hashes; short-lived access tokens limit damage window; single-session enforcement (new login revokes old) |
| **Dashboard aggregation queries become slow at scale** | Low (MVP) | Monitor query times from launch; add selective caching with Redis when P95 response time exceeds 500ms |
| **Circular service dependency introduced during development** | Medium | Enforce dependency direction rule in code review; no bidirectional service calls; Dashboard is read-only |
| **No email delivery = broken invite flow** | Medium | Configure email service before first production user; implement retry for email delivery in background task |

---

> **This blueprint is complete and ready for implementation.** Hand it to a senior FastAPI developer or an AI coding agent with the instruction to implement in the sequence defined in Section 26, one phase at a time, with each phase's exit criteria verified before proceeding to the next.
