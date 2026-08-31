# Employee Management SaaS — MVP Product Specification & API Blueprint

**Version:** 1.0 — Initial Product Freeze  
**Status:** Authoritative MVP Definition  
**Last Updated:** 2026-08-31  
**Audience:** Product Owners, Backend Architects, Developers, QA

---

> This document is the single source of truth for the Employee Management SaaS MVP.  
> It defines what the product is, what it does, how modules interact, what APIs are required, and in what order they must be built.  
> No implementation code, database schemas, or framework-specific constructs appear in this document.

---

# Table of Contents

1. [Product Vision](#phase-1--product-vision)
2. [MVP Goals](#phase-2--mvp-goals)
3. [MVP Non-Goals](#phase-3--mvp-non-goals)
4. [Actors & Permissions](#phase-4--actors--permissions)
5. [Module Map](#phase-5--module-map)
6. [Global Dependency Graph](#phase-6--global-dependency-graph)
7. [Domain Concepts](#phase-7--domain-concepts)
8. [Module-by-Module Specification](#phase-8--module-by-module-specification)
9. [Critical Business Workflows](#phase-9--critical-business-workflows)
10. [Leave System Deep Analysis](#phase-10--leave-system-deep-analysis)
11. [Attendance Deep Analysis](#phase-11--attendance-deep-analysis)
12. [Work Tracker Deep Analysis](#phase-12--work-tracker-deep-analysis)
13. [Dashboard Definition](#phase-13--dashboard-definition)
14. [Cross-Module Rules](#phase-14--cross-module-rules)
15. [MVP vs Post-MVP Classification](#phase-15--mvp-vs-post-mvp-classification)
16. [Final API Catalog](#phase-16--final-api-catalog)
17. [Final Implementation Order](#phase-17--final-implementation-order)
18. [MVP Completeness Audit](#phase-18--mvp-completeness-audit)
19. [Contradiction & Gap Audit](#phase-19--contradiction--gap-audit)
20. [MVP Product Freeze](#phase-20--mvp-product-freeze)

---

# PHASE 1 — PRODUCT VISION

## 1.1 What Problem This SaaS Solves

Small and medium-sized teams struggle with employee management scattered across spreadsheets, chat messages, and ad-hoc processes. Managers lose visibility into who is working, who is absent, and how much leave each employee has taken or is entitled to. HR admins spend disproportionate time manually tracking attendance, fielding leave requests, and updating spreadsheets.

This product solves **three tightly coupled operational pain points** in one cohesive, lightweight tool:

- **Tracking what employees work on** — eliminating the guesswork of who did what.
- **Tracking when employees are present or absent** — without expensive biometric hardware.
- **Managing employee leave** — with both manager-discretion grants and automated policy-based allocations.

## 1.2 Target Customer

Small and medium-sized companies (typically 10–500 employees) that:

- Have outgrown spreadsheets but cannot justify the cost or complexity of a full HRMS.
- Need basic operational visibility, not sophisticated analytics.
- Have functional managers (not necessarily dedicated HR departments).
- Are comfortable adopting a web-based SaaS tool.

## 1.3 Primary Users

| User | Description |
|------|-------------|
| **Organization Admin** | Sets up the organization, configures leave policies, manages users and roles |
| **Manager** | Oversees a team of employees; approves leave, grants leave, reviews work and attendance |
| **Employee** | Logs daily work, checks in/out for attendance, requests leave, views own records |

## 1.4 Core Value Proposition

> "One simple tool to know who is working, when they worked, and how much leave they have — without becoming an HR system."

The product delivers:
- **Operational visibility** for managers without complex setup.
- **Self-service** for employees (request leave, log work, view own records).
- **Automated fairness** through policy-driven leave allocation.
- **Multi-tenant SaaS** so each organization gets an isolated, configurable environment.

## 1.5 Why This Is Intentionally Not a Full HRMS

A full HRMS encompasses payroll, recruitment, performance management, appraisals, benefits, compliance, and dozens of integrations. Building all of this:
- Delays time-to-market by 12–24+ months.
- Increases operational complexity beyond what a small team can maintain.
- Prices the product out of the SMB market.
- Dilutes focus — early customers want operational basics, not enterprise features.

This product launches with exactly the three capabilities that represent the first real pain point for growing teams: **work tracking, attendance, and leave**. Everything else is intentionally deferred.

---

# PHASE 2 — MVP GOALS

The following are measurable, product-level goals for the initial launch:

1. **Multi-tenant SaaS launch**: At least 3 independent organizations can onboard, configure their leave policy, and operate fully independently with no data leakage between tenants.

2. **Employee onboarding in under 5 minutes**: An admin can create an organization, invite employees, and have employees logging work within 5 minutes of setup.

3. **Daily work logging operational**: Every employee can create, view, and edit their own daily work entries without manager intervention.

4. **Attendance tracking live**: Every employee can check in and check out each day. Admins and managers can see the attendance status of their team in real time.

5. **Leave request workflow functional**: An employee can submit a leave request; a manager can approve or reject it; the leave balance is updated accordingly.

6. **Manager-granted leave functional**: A manager can directly grant leave to an employee without a formal employee request, immediately updating balance and attendance status.

7. **Automatic leave allocation functional**: An organization can configure a leave policy. The system automatically allocates leave credits to eligible employees based on that policy.

8. **Leave reflected in attendance**: When leave is approved or granted, the corresponding attendance dates are automatically updated to reflect LEAVE status, without the employee manually checking out.

9. **Role-based access enforced**: Employees can only see their own records. Managers see only their assigned team. Admins see everything in their organization.

10. **Data isolation between tenants**: No API endpoint can return data from a different organization, regardless of authentication credentials.

---

# PHASE 3 — MVP NON-GOALS

The following features are explicitly **excluded from MVP**. They must not be designed, built, or implied in the initial release.

| Non-Goal | Reason for Exclusion |
|----------|----------------------|
| **Payroll** | Separate complex domain; requires compliance, tax rules, and bank integrations |
| **Recruitment / Applicant Tracking** | Different problem space; no overlap with core MVP |
| **Performance Management** | Not needed to validate core operational tracking |
| **Employee Appraisals / Reviews** | Complex workflows; no MVP justification |
| **Task / Project Management** | Risk of becoming Jira/Asana; work tracker is deliberately simple |
| **Overtime Calculations** | Requires shift definitions, pay rules, and labor law handling |
| **Complex Shift Management** | Multiple shifts, rotation schedules — out of MVP scope |
| **GPS Attendance** | Hardware/location dependency; overcomplicates MVP |
| **Biometric Attendance** | Hardware integration; enterprise concern |
| **Face Recognition** | AI-dependent; out of scope |
| **Screenshots / Productivity Monitoring** | Privacy concerns; not appropriate for SMB trust-based culture |
| **Holiday Calendar** | Valuable but deferred — attendance MVP treats all non-leave days as workdays |
| **Weekend Configuration** | Deferred — MVP treats Saturday/Sunday as non-working days by convention; no complex shift calendar |
| **Advanced Analytics / Reporting** | MVP dashboards are summary views, not analytics platforms |
| **Enterprise SSO (SAML/OIDC)** | Enterprise feature; standard email/password + JWT is sufficient for MVP |
| **Granular / Custom RBAC** | Three fixed roles are sufficient for MVP |
| **Slack / Telegram / WhatsApp Integrations** | Nice-to-have; deferred |
| **AI Features** | No MVP justification |
| **Advanced Billing / Subscription Management** | Not needed for early customer onboarding; manual billing is acceptable initially |
| **Carry-Forward of Leave Balance** | Adds complexity to year-boundary handling; deferred to Post-MVP |
| **Leave Encashment** | Requires payroll integration; out of scope |
| **Compensatory Leave** | Complex business rules; Post-MVP |
| **Bulk Employee Import (CSV)** | Useful but not launch-critical |
| **Employee Self-Service Profile Edits** | Admin-controlled for MVP simplicity |
| **Multi-Manager / Matrix Reporting** | Each employee has exactly one manager for MVP |

---

# PHASE 4 — ACTORS & PERMISSIONS

## 4.1 Role Definitions

### Organization Admin

The Admin is the super-user within their organization. There is exactly one Admin per organization in MVP (the organization creator). Admins configure the product and have full visibility.

**Purpose:** Manage the organization setup, employees, roles, and leave policy configuration.

### Manager

A Manager oversees a specific set of employees. Managers are employees of the organization who have been elevated to the Manager role.

**Purpose:** Day-to-day oversight of team attendance, work, and leave.

### Employee

A regular staff member with no management responsibilities.

**Purpose:** Self-service — log work, record attendance, request leave, view own records.

---

## 4.2 Permission Matrix

| Action | Admin | Manager | Employee |
|--------|-------|---------|----------|
| **Organization** | | | |
| Create organization | Any unauthenticated user | ❌ | ❌ |
| View organization settings | ✅ | ❌ | ❌ |
| Update organization settings | ✅ | ❌ | ❌ |
| Configure leave policy | ✅ | ❌ | ❌ |
| **Employees** | | | |
| Create employee | ✅ | ❌ | ❌ |
| View all employees | ✅ | Own team only | Own profile only |
| Update any employee profile | ✅ | ❌ | ❌ |
| Deactivate employee | ✅ | ❌ | ❌ |
| Assign manager to employee | ✅ | ❌ | ❌ |
| View own profile | ✅ | ✅ | ✅ |
| **Work Entries** | | | |
| Create own work entry | ✅ | ✅ | ✅ |
| View own work entries | ✅ | ✅ | ✅ |
| Edit own work entry (within grace period) | ✅ | ✅ | ✅ |
| View team work entries | ✅ | Own team only | ❌ |
| View all work entries | ✅ | ❌ | ❌ |
| **Attendance** | | | |
| Check in (own) | ✅ | ✅ | ✅ |
| Check out (own) | ✅ | ✅ | ✅ |
| View own attendance | ✅ | ✅ | ✅ |
| View team attendance | ✅ | Own team only | ❌ |
| View all attendance | ✅ | ❌ | ❌ |
| Manually correct attendance | ✅ | Own team only | ❌ |
| **Leave** | | | |
| Request leave (own) | ✅ | ✅ | ✅ |
| View own leave requests | ✅ | ✅ | ✅ |
| Cancel own pending leave request | ✅ | ✅ | ✅ |
| View team leave requests | ✅ | Own team only | ❌ |
| Approve/reject team leave requests | ✅ | Own team only | ❌ |
| Grant leave directly to employee | ✅ | Own team only | ❌ |
| View leave balances (own) | ✅ | ✅ | ✅ |
| View team leave balances | ✅ | Own team only | ❌ |
| View all leave balances | ✅ | ❌ | ❌ |
| **Dashboard** | | | |
| View own dashboard | ✅ | ✅ | ✅ |
| View team dashboard | ✅ | Own team only | ❌ |
| View org-wide dashboard | ✅ | ❌ | ❌ |

---

## 4.3 Scope Enforcement Rules

- **Employee scope**: An employee can only access records that belong to themselves.
- **Manager scope**: A manager can only access records belonging to employees directly assigned to them. The manager cannot access records of employees in another manager's team.
- **Admin scope**: An admin can access all data within their own organization.
- **Cross-organization isolation**: No role in Organization A can access any data in Organization B. This is enforced at the API level on every request.

---

# PHASE 5 — MODULE MAP

## Module Overview

| Module | Core Responsibility |
|--------|---------------------|
| **SaaS / Organization** | Multi-tenant foundation; organization lifecycle and settings |
| **Authentication** | User identity, login, and session management |
| **Employee Management** | Employee profiles, roles, and manager assignments |
| **Work Tracker** | Daily work entry logging and review |
| **Attendance** | Daily check-in/check-out and absence tracking |
| **Leave** | Leave policy, leave balance, leave requests, and grants |
| **Dashboard** | Summary views per role |

---

## Module 0 — SaaS / Organization Foundation

**Purpose:** Provides the multi-tenant scaffold. Every other module depends on an Organization existing.

**MVP Scope:** Organization creation, basic settings (name, timezone), leave policy configuration (owned by this module conceptually, configured here by admin).

**Responsibilities:** Create and manage organizations; maintain organization-level configuration; enforce tenant isolation.

**Owned Concepts:** Organization, OrganizationSettings.

**Dependencies:** None (this is the root).

**Downstream Consumers:** All other modules.

**MVP Features:**
- Register a new organization
- View/update organization settings
- Configure leave policy (leave types, accrual rules)

**Post-MVP Features:**
- Billing/subscription management
- Custom branding
- Multiple admins per organization
- Organization-level audit log

**Business Rules:**
- Organization names must be unique across the platform.
- Each organization has exactly one Admin at launch (the creator).
- All data in the system is scoped to an organization.
- Leave policy belongs to the organization; employees inherit it.

**Cross-Module Interactions:**
- Provides `organization_id` scoping to every other module.
- Leave policy defined here is consumed by the Leave module.

---

## Module 1 — Authentication & Access

**Purpose:** Manages user identity, authentication credentials, and session tokens.

**MVP Scope:** Email/password registration, login, JWT-based session, password reset.

**Responsibilities:** Create user accounts; authenticate users; issue and validate tokens; link users to organizations and roles.

**Owned Concepts:** User (authentication identity), UserSession (JWT token).

**Dependencies:** Organization must exist before a user can be added to it.

**Downstream Consumers:** All modules (every API request requires authentication).

**MVP Features:**
- Admin registers themselves when creating an organization
- Invite (create) additional users (employees/managers) — initiated by Admin
- Login with email and password
- Token refresh
- Password reset (via email link)
- Logout

**Post-MVP Features:**
- Social login (Google, GitHub)
- Enterprise SSO (SAML/OIDC)
- MFA
- Login audit log

**Business Rules:**
- Email addresses are unique per organization.
- A user belongs to exactly one organization in MVP.
- JWT tokens have a defined expiry; refresh tokens extend sessions.
- Only an Admin can create new user accounts within the organization.
- A deactivated employee loses the ability to authenticate.

**Cross-Module Interactions:**
- Employee Management module creates the Employee record; Authentication module creates the User credential. These are linked but distinct concepts.
- Deactivating an employee (Employee Management) must invalidate their active sessions (Authentication).

---

## Module 2 — Employee Management

**Purpose:** Manages the human members of an organization — their profiles, roles, and reporting relationships.

**MVP Scope:** Employee profiles, role assignments, manager-to-employee assignments, and employee deactivation.

**Responsibilities:** Own the canonical record of "who is an employee of this organization"; maintain manager assignments; enforce manager-scoped access.

**Owned Concepts:** Employee, ManagerAssignment.

**Dependencies:**
- Organization (must exist)
- Authentication / User (each employee has a corresponding user account)

**Downstream Consumers:** Work Tracker, Attendance, Leave (all require a valid employee to exist).

**MVP Features:**
- Create employee (Admin only) — simultaneously creates user credential
- View employee profile (own, or by manager for their team, or by Admin for all)
- Update employee profile (Admin only)
- Assign/change manager (Admin only)
- Deactivate employee (Admin only)
- List all employees (Admin), list team employees (Manager)

**Post-MVP Features:**
- Employee self-service profile edits (limited fields)
- Bulk CSV import
- Employee documents/contracts storage
- Department/team hierarchy beyond single-level manager

**Business Rules:**
- An employee must belong to exactly one organization.
- An employee has exactly one direct manager (or no manager if not yet assigned).
- An employee cannot be their own manager.
- A Manager is also an Employee — the distinction is the role assigned.
- Deactivating an employee does not delete their historical records.
- A deactivated employee cannot log work, check in, or request leave.
- An employee with no manager assigned can still log work and attendance; they just cannot have leave approved by a manager until one is assigned (Admin can approve in this case).

**Cross-Module Interactions:**
- When an employee is created: Work Tracker, Attendance, and Leave modules become available for that employee.
- When an employee is deactivated: their active sessions are terminated; they cannot create new entries in any module; existing records remain intact.
- Leave module uses the employee's `joining_date` for leave eligibility calculations.

---

## Module 3 — Work Tracker

**Purpose:** Allows employees to log what they worked on each day. Provides managers and admins visibility into team productivity.

**MVP Scope:** Simple daily work entry — a title, description, and optional duration. No project hierarchy.

**Responsibilities:** Accept, store, and expose daily work entries per employee.

**Owned Concepts:** WorkEntry.

**Dependencies:**
- Organization (scoping)
- Employee (must exist and be active to log work)

**Downstream Consumers:** Dashboard (aggregates work entries for summary views).

**MVP Features:**
- Create a work entry (Employee, Manager, Admin — for themselves)
- View own work entries
- Edit own work entry (within a defined grace period — 24 hours after creation)
- List work entries for a date range (own)
- Manager: view team work entries for a date range
- Admin: view any employee's work entries

**Post-MVP Features:**
- Project/tag categorization
- Time tracking with start/end timestamps
- Manager editing of employee entries
- Approval workflow for timesheets
- Export to CSV

**Business Rules:**
- An employee can create multiple work entries per day.
- A work entry requires at minimum a title and date.
- Description is optional.
- Duration (in hours/minutes) is optional.
- An employee can edit their own work entry within 24 hours of creation.
- After 24 hours, work entries are locked for the employee. Only Admin can edit a locked entry.
- Work entries cannot be deleted — they can only be edited.
- A deactivated employee's work entries remain readable but no new entries can be created.

**Cross-Module Interactions:**
- Dashboard reads work entries for activity summaries.
- No direct interaction with Attendance or Leave modules.

---

## Module 4 — Attendance

**Purpose:** Tracks when employees are present, absent, or on leave on each working day.

**MVP Scope:** Daily check-in/check-out, automatic absence marking, manual correction by admin/manager, leave-driven attendance updates.

**Responsibilities:** Own the attendance record for each employee-day; determine and expose attendance status per day.

**Owned Concepts:** AttendanceRecord.

**Dependencies:**
- Organization (scoping, timezone)
- Employee (must exist)
- Leave module (approved/granted leave updates attendance status)

**Downstream Consumers:** Dashboard (attendance summaries).

**MVP Features:**
- Employee checks in (creates/opens an attendance record for today)
- Employee checks out (closes the attendance record for today)
- System marks employees absent at end of day if no check-in occurred
- Admin/Manager can manually correct an attendance record
- View own attendance history
- Manager views team attendance
- Admin views all attendance

**Post-MVP Features:**
- Holiday calendar integration
- Shift management and shift-aware attendance
- Mobile GPS check-in/check-out
- Automated absence notifications
- Biometric integration

**Cross-Module Interactions:**
- Leave module writes LEAVE status to AttendanceRecord when leave is approved or granted.
- Dashboard reads attendance status to show daily team presence.

---

## Module 5 — Leave

**Purpose:** Manages the full lifecycle of employee leave — policy configuration, balance tracking, employee requests, manager approvals, direct grants, and automatic allocations.

**MVP Scope:** Leave types, leave policy per organization, leave balance per employee per leave type, employee leave requests, manager approval/rejection, manager direct grant, automatic policy-based allocation.

**Responsibilities:** Own leave policy, leave balances, and leave records; compute balance changes on every leave event; trigger attendance updates when leave status is confirmed.

**Owned Concepts:** LeaveType, LeavePolicy, LeavePolicyRule, LeaveBalance, LeaveRecord.

**Dependencies:**
- Organization (leave policy belongs to organization)
- Employee (leave balance and records belong to employees)
- Attendance module (Leave writes to attendance on approval/grant)

**Downstream Consumers:** Attendance (status updates), Dashboard (leave summaries).

**MVP Features:**
- Admin configures leave types (e.g., Casual Leave, Sick Leave, Annual Leave)
- Admin configures leave policy rules per leave type (accrual amount, frequency, max balance)
- System automatically allocates leave credits to employees per policy
- Employee views own leave balance
- Employee submits a leave request (specifying dates, leave type, reason)
- Manager views team leave requests
- Manager approves or rejects a leave request
- Manager directly grants leave to an employee
- Admin can perform all manager leave actions for any employee
- Employee can cancel their own pending (not yet approved) leave request

**Post-MVP Features:**
- Carry-forward of unused balance at year end
- Leave encashment
- Compensatory leave
- Half-day leave
- Leave request modification (not just cancel)
- Leave approval delegation
- Manager-level leave policy overrides

**Cross-Module Interactions:**
- When leave is approved or granted: Attendance module is updated for all dates in the leave period, setting status = LEAVE.
- When leave is cancelled (if pending, before approval): no attendance change occurs.
- Dashboard reads leave balances and upcoming leave for summary views.

---

## Module 6 — Dashboard

**Purpose:** Provides role-appropriate summary views to give each user operational visibility without navigating to individual modules.

**MVP Scope:** Simple, pre-computed summary cards and lists. No chart libraries or advanced analytics.

**Responsibilities:** Aggregate data from other modules and present a role-appropriate snapshot.

**Owned Concepts:** None — the Dashboard owns no entities; it only reads from other modules.

**Dependencies:** Organization, Employee, Work Tracker, Attendance, Leave (reads from all).

**Downstream Consumers:** None.

**MVP Features:**
- Employee dashboard: today's attendance status, recent work entries, leave balance summary, upcoming approved leave
- Manager dashboard: team attendance status today, pending leave requests, team leave overview
- Admin dashboard: organization-wide attendance summary, leave policy status, employee count

**Post-MVP Features:**
- Trend charts and graphs
- Exportable reports
- Custom date-range analytics
- Automated scheduled reports

**Business Rules:**
- The Dashboard never mutates data; it only reads.
- Data shown is always scoped to the role (employee sees own data, manager sees team, admin sees org).

---

# PHASE 6 — GLOBAL DEPENDENCY GRAPH

## 6.1 Dependency Graph

```
Organization
     │
     ├──────────────────────────────────┐
     │                                  │
Authentication                    Leave Policy (configured here)
     │                                  │
     ▼                                  │
   User                                 │
     │                                  │
     ▼                                  │
  Employee ◄────── ManagerAssignment    │
     │                                  │
     ├─────────────────────┐            │
     │                     │            │
     ▼                     ▼            ▼
Work Tracker          Attendance ◄── Leave
                                        │
                                        └──► Attendance
                                             (writes status on
                                              approve/grant)

Dashboard
  ◄── Work Tracker
  ◄── Attendance
  ◄── Leave
  ◄── Employee
```

## 6.2 Dependency Analysis

### Organization → All Modules

**Why it exists:** Every entity in the system must belong to an organization. Without organization scoping, tenant isolation is impossible.

**Source of truth:** Organization module.

**Consumed by:** Every module.

**What happens when the source changes:** If an organization is deactivated (Post-MVP concept), all associated data becomes inaccessible but is not deleted.

---

### Organization → Leave Policy

**Why it exists:** Different organizations have different leave entitlements. The organization is the owner of its leave policy.

**Source of truth:** Organization module owns the policy configuration; Leave module owns the interpretation and execution of policy.

**Consumed by:** Leave module (to determine allocation amounts and frequency).

**What happens when the source changes:** If an admin modifies a leave policy, the change applies to future allocations only. Leave balances already allocated are not retroactively changed.

---

### Authentication → Employee

**Why it exists:** An employee needs a login credential (User) to access the system. The User record (auth identity) and the Employee record (HR profile) are distinct but linked. This separation allows future support for contractors or service accounts without Employee profiles.

**Source of truth:** Authentication module owns the User identity. Employee Management module owns the Employee profile.

**Consumed by:** Every module that performs authorization checks uses the User → Employee link to determine scope.

**What happens when the source changes:** If an Employee is deactivated, their User account is also deactivated. The link between User and Employee is never broken; only status changes.

---

### Employee → Work Tracker

**Why it exists:** Work entries must be attributed to a specific employee. There can be no orphaned work entries.

**Source of truth:** Employee Management owns the Employee record.

**Consumed by:** Work Tracker (to validate that the work entry author is a valid, active employee).

**What happens when the source changes:** If an employee is deactivated, existing work entries remain readable. New work entries cannot be created for a deactivated employee.

---

### Employee → Attendance

**Why it exists:** Attendance records must be attributed to a specific employee-day pair. There can be no orphaned attendance records.

**Source of truth:** Employee Management owns the Employee record.

**Consumed by:** Attendance module.

**What happens when the source changes:** If an employee is deactivated, existing attendance records remain. No new attendance records (check-in/check-out) can be created for a deactivated employee.

---

### Employee → Leave

**Why it exists:** Leave balances and records belong to employees. The employee's `joining_date` determines eligibility for automatic leave allocation.

**Source of truth:** Employee Management owns the Employee record including `joining_date`.

**Consumed by:** Leave module.

**What happens when the source changes:** If an employee's joining date is corrected (Admin action), the leave allocation logic for future automatic runs uses the corrected date. Past allocations are not retroactively changed.

---

### Leave → Attendance

**Why it exists:** When leave is approved or granted, the employee is not expected to check in on those days. Attendance must automatically reflect LEAVE status so that absence marks are not incorrectly applied.

**Source of truth:** Leave module owns the authoritative leave status. Attendance module owns the authoritative attendance record.

**Consumed by:** Attendance module.

**What happens when the source changes:** When a leave request is approved or a direct grant is issued, the Leave module instructs the Attendance module to update or create attendance records for all dates in the leave period with status = LEAVE. This is a write from Leave into Attendance.

---

### Manager → Employee Scope

**Why it exists:** Managers have access only to their own team. This scoping must be enforced by the Employee Management module, which owns the ManagerAssignment relationship.

**Source of truth:** Employee Management module owns the ManagerAssignment.

**Consumed by:** Work Tracker, Attendance, Leave (all scoped queries for managers filter by employees assigned to that manager).

**What happens when the source changes:** If an employee's manager is changed, the new manager gains access to that employee's records going forward. The previous manager loses access. Historical records remain but are only accessible to the new manager and Admin.

---

# PHASE 7 — DOMAIN CONCEPTS

## 7.1 Organization

**Purpose:** The top-level tenant in the SaaS system. Every piece of data belongs to exactly one organization.

**Important Fields/Concepts:**
- Name
- Slug/identifier (for URL or subdomain routing)
- Timezone (used for attendance day boundary calculations)
- Status (active / suspended — suspended is Post-MVP)
- Admin user reference
- Created date

**Relationships:** Parent of all other entities.

**Ownership:** Owned by SaaS/Organization module.

**Lifecycle:** Created at signup; remains active as long as the subscription is valid (billing is Post-MVP); deletion is not supported in MVP.

**Constraints:**
- Name must be unique across the platform.
- Timezone is required and immutable after creation (changing timezone has complex implications for historical attendance records — deferred to Post-MVP).

---

## 7.2 User

**Purpose:** Represents an authentication identity — the credentials used to log in.

**Important Fields/Concepts:**
- Email address (unique per organization)
- Hashed password
- Status (active / deactivated)
- Organization reference
- Linked Employee reference
- Last login timestamp

**Relationships:** One-to-one with Employee.

**Ownership:** Owned by Authentication module.

**Lifecycle:** Created when Admin creates an employee. Deactivated when employee is deactivated. Not deletable in MVP (data integrity).

**Constraints:**
- Email must be unique within the organization.
- A deactivated user cannot authenticate.

---

## 7.3 Employee

**Purpose:** The HR profile of a person within an organization. Distinct from User (authentication identity).

**Important Fields/Concepts:**
- Full name
- Email (same as User email)
- Role (Admin, Manager, Employee)
- Status (active / inactive)
- Joining date (critical for leave eligibility)
- Direct manager reference (nullable)
- Organization reference
- Department (optional, informational in MVP)
- Job title (optional, informational in MVP)

**Relationships:**
- One-to-one with User
- Many-to-one with Organization
- Many-to-one with Employee (self-referencing manager relationship)

**Ownership:** Owned by Employee Management module.

**Lifecycle:** Created by Admin. Active by default. Deactivated by Admin. Not deleted.

**Constraints:**
- An employee cannot be their own manager.
- Joining date cannot be in the future at the time of employee creation.
- An employee's role is exactly one of: Admin, Manager, Employee.
- Only one Admin per organization in MVP.

---

## 7.4 Work Entry

**Purpose:** A record of what an employee worked on during a specific day.

**Important Fields/Concepts:**
- Employee reference
- Organization reference
- Date (the date the work pertains to, not necessarily the submission date)
- Title (required, concise description of work)
- Description (optional, longer detail)
- Duration in minutes (optional)
- Created timestamp
- Last updated timestamp
- Locked flag (true if more than 24 hours have passed since creation and the entry is frozen for the employee)

**Relationships:** Many-to-one with Employee.

**Ownership:** Owned by Work Tracker module.

**Lifecycle:** Created by the employee. Editable within 24 hours. Locked after 24 hours (Admin can still edit). Not deletable.

**Constraints:**
- Title is required.
- Date is required; cannot be a future date.
- Duration, if provided, must be a positive integer (in minutes).
- Multiple work entries per employee per day are allowed.

---

## 7.5 Attendance Record

**Purpose:** Represents the attendance status of an employee for a single calendar day within their organization's timezone.

**Important Fields/Concepts:**
- Employee reference
- Organization reference
- Date (calendar date in organization's timezone)
- Status: one of `PRESENT`, `ABSENT`, `LEAVE`, `HALF_DAY` (HALF_DAY is Post-MVP)
- Check-in timestamp (nullable — null if not checked in)
- Check-out timestamp (nullable — null if not checked out)
- Duration in minutes (derived from check-in to check-out)
- Manual override flag (true if an Admin/Manager corrected this record)
- Override reason (text, required if manually overridden)
- Leave Record reference (nullable — set if status is LEAVE)

**Relationships:** Many-to-one with Employee. Optional one-to-one with LeaveRecord.

**Ownership:** Owned by Attendance module.

**Lifecycle:**
- Created automatically on first check-in of the day.
- Also created automatically by a scheduled job at end-of-day for employees who did not check in (status = ABSENT).
- Also created/updated by Leave module when leave is approved/granted (status = LEAVE).
- Cannot be deleted.

**Constraints:**
- Exactly one Attendance Record per employee per date.
- Check-out timestamp must be after check-in timestamp.
- Status is authoritative — other modules read status from this record.

---

## 7.6 Leave Type

**Purpose:** A category of leave that an organization offers (e.g., Casual Leave, Sick Leave, Annual Leave).

**Important Fields/Concepts:**
- Name (e.g., "Casual Leave")
- Code (short code, e.g., "CL")
- Description (optional)
- Organization reference
- Is active (admin can deactivate a leave type)

**Relationships:** Many-to-one with Organization. One-to-one with LeavePolicyRule (per organization).

**Ownership:** Owned by Leave module.

**Lifecycle:** Created by Admin. Deactivatable. Not deletable (historical records reference it).

**Constraints:**
- Leave type name must be unique within an organization.
- At least one leave type must exist before employees can request leave.

---

## 7.7 Leave Policy Rule

**Purpose:** Defines how leave of a given type is automatically allocated to employees within an organization.

**Important Fields/Concepts:**
- Organization reference
- Leave Type reference
- Allocation amount (number of leave days allocated per allocation cycle)
- Allocation frequency: one of `MONTHLY`, `QUARTERLY`, `ANNUALLY`
- Minimum tenure required (in days) before an employee is eligible for this leave type's allocation (e.g., must have worked 90 days before being eligible for annual leave)
- Maximum balance cap (the maximum number of days an employee can hold at one time; additional allocation is capped at this value)
- Is pro-rated on joining (boolean — if true, the first allocation is reduced proportionally based on how much of the period the employee has completed)

**Relationships:** Many-to-one with Organization; one-to-one with LeaveType.

**Ownership:** Owned by Leave module (configured via Organization Admin).

**Lifecycle:** Created and managed by Admin. Changes apply to future allocations only.

**Constraints:**
- Each organization can have at most one LeavePolicyRule per LeaveType.
- Allocation amount must be a positive number.
- Maximum balance cap must be >= allocation amount.

---

## 7.8 Leave Balance

**Purpose:** Tracks how many leave days of a given type an employee currently has available.

**Important Fields/Concepts:**
- Employee reference
- Leave Type reference
- Organization reference
- Balance (available days — integer in MVP)
- Total allocated (cumulative allocated since last reset)
- Total used (cumulative used since last reset)
- Leave year (the year this balance applies to)

**Relationships:** Many-to-one with Employee; many-to-one with LeaveType.

**Ownership:** Owned by Leave module.

**Lifecycle:** Created when an employee first receives an allocation of a leave type. Reset at the start of each leave year (carry-forward is Post-MVP — reset means balance starts from 0). Updated on every leave grant, approval, or rejection.

**Constraints:**
- Balance cannot go below 0.
- One LeaveBalance record per employee per leave type per leave year.
- A missing LeaveBalance record implies balance = 0.

---

## 7.9 Leave Record

**Purpose:** A single leave event — either an employee request awaiting decision, or a completed leave (approved or granted).

**Important Fields/Concepts:**
- Employee reference
- Organization reference
- Leave Type reference
- Start date
- End date
- Number of leave days (computed, excluding weekends)
- Status: one of `PENDING`, `APPROVED`, `REJECTED`, `CANCELLED`, `GRANTED`
  - `PENDING` — employee submitted request, awaiting manager decision
  - `APPROVED` — manager approved an employee request
  - `REJECTED` — manager rejected an employee request
  - `CANCELLED` — employee cancelled their own pending request
  - `GRANTED` — manager directly granted leave without a prior request
- Reason (optional for employee requests; optional for manager grants)
- Manager/Admin who acted on the record (nullable for PENDING)
- Action timestamp
- Created timestamp

**Relationships:** Many-to-one with Employee; many-to-one with LeaveType; may reference AttendanceRecord(s).

**Ownership:** Owned by Leave module.

**Lifecycle:** Created when an employee submits a request (status = PENDING) or when a manager grants leave directly (status = GRANTED). Terminal statuses: APPROVED, REJECTED, CANCELLED, GRANTED.

**Constraints:**
- End date must be >= start date.
- An employee cannot have two overlapping leave records that are in PENDING or APPROVED/GRANTED status simultaneously.
- Once APPROVED or GRANTED, the record is immutable in MVP (no reversal in MVP).
- REJECTED and CANCELLED records do not affect leave balance.

---

# PHASE 8 — MODULE-BY-MODULE SPECIFICATION

---

## Module 0 — SaaS / Organization Foundation

### 1. Purpose

Provides the multi-tenant foundation. Creates and maintains the top-level organizational container that all other data belongs to.

### 2. Why It Exists

Without a tenant model, the SaaS cannot isolate one organization's data from another. This module must be the first thing built.

### 3. MVP Scope

- Organization registration (self-service by the person creating the organization)
- Organization settings (name, timezone)
- Leave type and leave policy rule management (configured by Admin; owned in this module's admin scope but executed by the Leave module)

### 4. Features

---

#### Feature: Register New Organization

**Description:** A new user registers their organization on the platform. This simultaneously creates the Organization and the Admin user account.

**Actor:** Unauthenticated user (future Admin)

**Preconditions:** No existing account with this email address on the platform.

**Main Flow:**
1. User provides organization name, their name, email, and password.
2. System validates all inputs.
3. System creates the Organization record.
4. System creates the User record with Admin role, linked to the organization.
5. System creates the Employee record for the Admin.
6. System returns a JWT access token and the organization details.

**Alternate Flow:** None for MVP (no email verification step in MVP to reduce friction).

**Success Outcome:** Organization created; Admin can log in and begin adding employees.

**Failure/Validation Conditions:**
- Organization name already exists on platform → 409 Conflict.
- Email address already registered → 409 Conflict.
- Missing required fields → 422 Validation Error.
- Password does not meet minimum requirements → 422 Validation Error.

**Dependencies:** None (this is the bootstrap action).

---

#### Feature: View Organization Settings

**Description:** Admin views the current organization configuration.

**Actor:** Admin

**Preconditions:** Admin is authenticated and belongs to the organization.

**Main Flow:**
1. Admin requests organization settings.
2. System returns organization name, timezone, and creation date.

**Success Outcome:** Organization settings displayed.

**Failure Conditions:**
- Not authenticated → 401.
- Not Admin → 403.

---

#### Feature: Update Organization Settings

**Description:** Admin updates the organization name or other settings.

**Actor:** Admin

**Preconditions:** Authenticated Admin.

**Main Flow:**
1. Admin submits updated organization name.
2. System validates uniqueness of new name.
3. System updates the organization record.
4. System returns the updated settings.

**Alternate Flow:** Admin attempts to change timezone — **timezone changes are not supported in MVP** due to the risk of corrupting historical attendance day boundaries. Admin must contact support.

**Success Outcome:** Organization settings updated.

**Failure Conditions:**
- New name conflicts with an existing organization → 409.
- Timezone change attempted → 422 with explanation.

---

### 5. Business Rules

- Organization names are unique across the entire platform.
- Each organization has exactly one Admin in MVP.
- Timezone is set at creation and cannot be changed via self-service in MVP.
- All data within the system is always scoped to an organization.

### 6. Permissions

| Action | Admin | Manager | Employee |
|--------|-------|---------|----------|
| Register organization | Any unauthenticated user | ❌ | ❌ |
| View settings | ✅ | ❌ | ❌ |
| Update settings | ✅ | ❌ | ❌ |

### 7. Cross-Module Effects

- Organization creation triggers the creation of the first User and Employee record (Admin).

### 8. APIs

---

**API: Register Organization**

```
API Name:         Register Organization
Purpose:          Creates a new organization and the first Admin user simultaneously
HTTP Method:      POST
Endpoint:         /api/v1/organizations/register
Actor:            Unauthenticated user
Authentication:   None
Required Permission: None

Request:
  - organization_name: string, required, 2–100 characters, must be globally unique
  - admin_full_name: string, required
  - admin_email: string, required, valid email format
  - password: string, required, minimum 8 characters

Response (201 Created):
  - organization: { id, name, slug, timezone, created_at }
  - user: { id, email, role }
  - access_token: JWT string
  - token_type: "bearer"

Errors:
  - 409: Organization name already exists
  - 409: Email already registered
  - 422: Validation errors on any field

Side Effects:
  - Creates Organization record
  - Creates User record (role: Admin)
  - Creates Employee record for Admin

Dependencies:
  - None

Idempotency:
  - Not idempotent. Duplicate submission with same email returns 409.
```

---

**API: Get Organization Settings**

```
API Name:         Get Organization Settings
Purpose:          Returns the current organization's settings
HTTP Method:      GET
Endpoint:         /api/v1/organizations/me
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Request:
  - No body. Organization is inferred from authenticated user's JWT.

Response (200 OK):
  - id, name, slug, timezone, created_at, employee_count

Errors:
  - 401: Not authenticated
  - 403: Not Admin role

Side Effects:
  - None

Dependencies:
  - Organization must exist
```

---

**API: Update Organization Settings**

```
API Name:         Update Organization Settings
Purpose:          Updates the organization's name or other settings
HTTP Method:      PATCH
Endpoint:         /api/v1/organizations/me
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Request:
  - organization_name: string, optional, 2–100 characters, must remain globally unique

Response (200 OK):
  - Updated organization object: { id, name, slug, timezone, updated_at }

Errors:
  - 401: Not authenticated
  - 403: Not Admin role
  - 409: New organization name already exists
  - 422: Attempted to change timezone (not permitted in MVP)
  - 422: Validation errors

Side Effects:
  - None

Dependencies:
  - Organization must exist
```

---

## Module 1 — Authentication & Access

### 1. Purpose

Manages user login, session tokens, and password lifecycle.

### 2. Why It Exists

Every API in the system is protected. Authentication is the gateway through which all users enter.

### 3. MVP Scope

Email/password login; JWT access tokens; refresh tokens; password reset via email.

### 4. Features

---

#### Feature: User Login

**Description:** A registered user authenticates and receives an access token.

**Actor:** Any registered user (Admin, Manager, Employee)

**Preconditions:** User account exists and is active.

**Main Flow:**
1. User submits email and password.
2. System validates credentials.
3. System issues JWT access token (short-lived) and refresh token (long-lived).
4. System records last login timestamp.

**Alternate Flow:** User account is deactivated → 403 Forbidden with message "Account deactivated."

**Success Outcome:** Tokens returned; user can access protected APIs.

**Failure Conditions:**
- Invalid credentials → 401.
- Deactivated account → 403.

---

#### Feature: Token Refresh

**Description:** A user exchanges a valid refresh token for a new access token.

**Actor:** Any authenticated user

**Main Flow:**
1. User submits a valid refresh token.
2. System validates it is not expired and not revoked.
3. System issues a new access token.

**Failure Conditions:**
- Invalid or expired refresh token → 401.
- Revoked token (e.g., after logout or deactivation) → 401.

---

#### Feature: Logout

**Description:** A user invalidates their current session.

**Actor:** Any authenticated user

**Main Flow:**
1. User submits their access token.
2. System invalidates the refresh token associated with the session.

**Success Outcome:** Session revoked; subsequent requests with old tokens rejected.

---

#### Feature: Invite Employee (Create User Account)

**Description:** Admin creates a user account for a new employee. The employee's User and Employee records are both created.

**Actor:** Admin

**Preconditions:** Admin is authenticated; employee profile data is available.

**Main Flow:**
1. Admin submits new employee details (name, email, role, joining date, manager assignment).
2. System validates data (email uniqueness within org, role validity).
3. System creates Employee record.
4. System creates User record (status: active).
5. System sends an email to the new user with a temporary password or password-set link.
6. System returns the created employee profile.

**Failure Conditions:**
- Email already in use within this organization → 409.
- Invalid role specified → 422.
- Manager reference is invalid or not in the same org → 422.

**Note:** Password-set email is MVP. If email delivery fails, Admin can manually provide credentials (Post-MVP: resend invite).

---

#### Feature: Password Reset

**Description:** A user resets their forgotten password via email.

**Actor:** Any registered user

**Main Flow:**
1. User provides their registered email.
2. System sends a time-limited password reset link.
3. User follows the link and sets a new password.
4. System invalidates all existing refresh tokens for this user (forces re-login on all devices).

**Failure Conditions:**
- Email not found → 200 OK (no information leakage; same response whether email exists or not).
- Reset link expired → 422.
- Reset link already used → 422.

---

### 5. Business Rules

- Access tokens expire after 15 minutes (short-lived; implementation may adjust, but must be short).
- Refresh tokens expire after 7 days.
- A deactivated user's refresh tokens are immediately revoked on deactivation.
- Password reset tokens expire after 1 hour.
- Each user can have at most one active refresh token in MVP (new login revokes old refresh token).

### 6. Permissions

| Action | Admin | Manager | Employee |
|--------|-------|---------|----------|
| Login | ✅ | ✅ | ✅ |
| Refresh token | ✅ | ✅ | ✅ |
| Logout | ✅ | ✅ | ✅ |
| Request password reset | ✅ | ✅ | ✅ |
| Create user (invite employee) | ✅ | ❌ | ❌ |

### 7. Cross-Module Effects

- Creating a user (invite) also creates an Employee record (coordinated action, atomically).
- Deactivating an employee (from Employee Management) revokes all their active tokens.

### 8. APIs

---

**API: Login**

```
API Name:         Login
Purpose:          Authenticates a user and returns JWT tokens
HTTP Method:      POST
Endpoint:         /api/v1/auth/login
Actor:            Any registered user
Authentication:   None
Required Permission: None

Request:
  - email: string, required
  - password: string, required

Response (200 OK):
  - access_token: JWT string
  - refresh_token: string
  - token_type: "bearer"
  - expires_in: integer (seconds)
  - user: { id, email, role, organization_id, employee_id }

Errors:
  - 401: Invalid credentials
  - 403: Account deactivated

Side Effects:
  - Last login timestamp updated
  - Previous refresh token revoked (if any)

Dependencies:
  - User must exist and be active

Idempotency:
  - Not idempotent. Each login generates new tokens.
```

---

**API: Refresh Token**

```
API Name:         Refresh Token
Purpose:          Issues a new access token from a valid refresh token
HTTP Method:      POST
Endpoint:         /api/v1/auth/refresh
Actor:            Any authenticated user
Authentication:   Refresh token in request body
Required Permission: Valid, non-expired, non-revoked refresh token

Request:
  - refresh_token: string, required

Response (200 OK):
  - access_token: JWT string
  - expires_in: integer (seconds)

Errors:
  - 401: Invalid, expired, or revoked refresh token

Side Effects:
  - None

Idempotency:
  - Not idempotent.
```

---

**API: Logout**

```
API Name:         Logout
Purpose:          Revokes the user's current session
HTTP Method:      POST
Endpoint:         /api/v1/auth/logout
Actor:            Any authenticated user
Authentication:   Bearer JWT
Required Permission: Authenticated

Request:
  - No body required. Session identified from JWT.

Response (204 No Content)

Errors:
  - 401: Not authenticated

Side Effects:
  - Refresh token revoked
```

---

**API: Request Password Reset**

```
API Name:         Request Password Reset
Purpose:          Sends a password reset link to the user's email
HTTP Method:      POST
Endpoint:         /api/v1/auth/password-reset/request
Actor:            Any user (unauthenticated)
Authentication:   None
Required Permission: None

Request:
  - email: string, required

Response (200 OK):
  - message: "If this email is registered, a reset link has been sent."

Errors:
  - 422: Invalid email format

Side Effects:
  - Password reset token generated and stored
  - Reset email sent (if email is registered)

Idempotency:
  - New request invalidates any prior outstanding reset token for this user.
```

---

**API: Confirm Password Reset**

```
API Name:         Confirm Password Reset
Purpose:          Completes the password reset using the emailed token
HTTP Method:      POST
Endpoint:         /api/v1/auth/password-reset/confirm
Actor:            Any user (unauthenticated)
Authentication:   None
Required Permission: Valid reset token

Request:
  - token: string, required (from the reset email link)
  - new_password: string, required, minimum 8 characters

Response (200 OK):
  - message: "Password reset successfully."

Errors:
  - 422: Token expired (>1 hour old)
  - 422: Token already used
  - 422: Token invalid
  - 422: Password too short

Side Effects:
  - User's password updated
  - All active refresh tokens for this user revoked
```

---

## Module 2 — Employee Management

### 1. Purpose

Manages the human members of the organization — their profiles, roles, and manager-to-employee reporting relationships.

### 2. Why It Exists

Every other operational module (Work, Attendance, Leave) requires a valid employee to attribute records to. Employee Management is the canonical record of who belongs to the organization.

### 3. MVP Scope

Create employee, view/update profile, assign manager, deactivate employee, list employees.

### 4. Features

---

#### Feature: Create Employee

**Description:** Admin creates a new employee, simultaneously setting up their access credentials.

**Actor:** Admin

**Preconditions:** Admin is authenticated. Target email is not already used within the organization.

**Main Flow:**
1. Admin submits employee details: full name, email, role, joining date, optional department, optional job title, optional manager assignment.
2. System validates inputs (email uniqueness, valid role, valid manager reference).
3. System creates Employee record.
4. System creates User record linked to this employee.
5. System sends invite email with password-set link.
6. System returns created employee profile.

**Success Outcome:** Employee created; welcome email sent.

**Failure Conditions:**
- Email already exists in this org → 409.
- Manager reference does not exist or is in another org → 422.
- Role is invalid → 422.
- Joining date is in the future → 422.

---

#### Feature: View Employee Profile

**Description:** A user views an employee profile.

**Actor:** Admin (any employee), Manager (own team), Employee (own profile)

**Main Flow:**
1. Requester provides employee ID.
2. System validates scope (manager can only view their direct reports; employee can only view their own).
3. System returns employee profile.

**Failure Conditions:**
- Employee does not exist → 404.
- Requester does not have scope → 403.

---

#### Feature: Update Employee Profile

**Description:** Admin updates an employee's profile fields.

**Actor:** Admin

**Preconditions:** Employee exists and is active.

**Main Flow:**
1. Admin submits updated fields (name, department, job title, role, joining date correction).
2. System validates and updates the employee record.

**Alternate Flow:** Admin attempts to update email → **Not supported in MVP**.

**Failure Conditions:**
- Employee not found → 404.
- Not Admin → 403.
- Invalid role → 422.

---

#### Feature: Assign / Reassign Manager

**Description:** Admin assigns or changes an employee's direct manager.

**Actor:** Admin

**Preconditions:** Both the employee and the manager must be active members of the same organization. The new manager must have Manager or Admin role.

**Main Flow:**
1. Admin submits employee ID and new manager ID.
2. System validates both parties exist and are active.
3. System validates new manager has Manager or Admin role.
4. System updates the manager assignment.

**Failure Conditions:**
- Employee not found → 404.
- Manager not found → 404.
- Proposed manager does not have Manager or Admin role → 422.
- Employee and proposed manager are the same person → 422.

---

#### Feature: Deactivate Employee

**Description:** Admin deactivates an employee, preventing them from accessing the system.

**Actor:** Admin

**Preconditions:** Employee is currently active.

**Main Flow:**
1. Admin submits the employee ID for deactivation.
2. System sets Employee status to inactive.
3. System sets User status to deactivated.
4. System revokes all active session tokens for this user.
5. System auto-rejects all PENDING leave requests for this employee with system note.

**Success Outcome:** Employee cannot log in; all historical records remain intact.

**Failure Conditions:**
- Employee not found → 404.
- Employee already inactive → 409.
- Attempting to deactivate the sole Admin → 422.

---

#### Feature: List Employees

**Description:** Returns a list of employees based on the requester's scope.

**Actor:** Admin (all employees), Manager (own team)

**Main Flow:**
1. Requester calls list endpoint.
2. System applies scope filter.
3. System returns paginated list with basic profile info and active status.

---

### 5. Business Rules

- An employee belongs to exactly one organization.
- An employee has exactly one role: Admin, Manager, or Employee.
- An employee can have at most one direct manager.
- An employee cannot be their own manager.
- Deactivation does not delete historical records.
- A deactivated employee cannot create work entries, check in, or submit leave requests.
- Pending leave requests for a deactivated employee are automatically rejected by the system.
- The Admin employee record cannot be deactivated if they are the sole admin.

### 6. Permissions

| Action | Admin | Manager | Employee |
|--------|-------|---------|----------|
| Create employee | ✅ | ❌ | ❌ |
| View own profile | ✅ | ✅ | ✅ |
| View team profiles | N/A | Own team ✅ | ❌ |
| View all profiles | ✅ | ❌ | ❌ |
| Update any profile | ✅ | ❌ | ❌ |
| Assign manager | ✅ | ❌ | ❌ |
| Deactivate employee | ✅ | ❌ | ❌ |
| List all employees | ✅ | ❌ | ❌ |
| List team employees | ✅ | Own team ✅ | ❌ |

### 7. Cross-Module Effects

- Creating an employee → User record created; Leave balances become eligible for allocation.
- Deactivating an employee → User tokens revoked; pending leave requests auto-rejected.
- Changing manager assignment → Scope enforcement in Work, Attendance, Leave APIs shifts to new manager immediately.

### 8. APIs

---

**API: Create Employee**

```
API Name:         Create Employee
Purpose:          Creates a new employee profile and linked user account
HTTP Method:      POST
Endpoint:         /api/v1/employees
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Request:
  - full_name: string, required
  - email: string, required, unique within org
  - role: enum ("Manager" | "Employee"), required
  - joining_date: date, required, must not be in future
  - department: string, optional
  - job_title: string, optional
  - manager_id: UUID, optional

Response (201 Created):
  - employee: { id, full_name, email, role, joining_date, department, job_title, manager_id, status, created_at }

Errors:
  - 401: Not authenticated
  - 403: Not Admin
  - 409: Email already exists in this organization
  - 422: Invalid role
  - 422: joining_date is in the future
  - 422: manager_id does not exist or has invalid role

Side Effects:
  - User record created with temporary password
  - Invite email sent to new employee

Dependencies:
  - Organization must exist
  - If manager_id provided: manager must exist, be active, and have Manager or Admin role
```

---

**API: Get Own Profile**

```
API Name:         Get Own Profile
Purpose:          Returns the authenticated user's own employee profile
HTTP Method:      GET
Endpoint:         /api/v1/employees/me
Actor:            Any authenticated user
Authentication:   Bearer JWT
Required Permission: Authenticated

Response (200 OK):
  - employee: { id, full_name, email, role, joining_date, department, job_title, manager, status, created_at }

Errors:
  - 401: Not authenticated
```

---

**API: List Employees**

```
API Name:         List Employees
Purpose:          Returns a paginated list of employees visible to the requester
HTTP Method:      GET
Endpoint:         /api/v1/employees
Actor:            Admin (all), Manager (own team)
Authentication:   Bearer JWT
Required Permission: Admin or Manager

Query Parameters:
  - status: enum ("active" | "inactive" | "all"), optional, default "active"
  - page: integer, optional, default 1
  - page_size: integer, optional, default 20, max 100

Response (200 OK):
  - employees: [ { id, full_name, email, role, status, joining_date, manager_id } ]
  - total: integer
  - page: integer
  - page_size: integer

Errors:
  - 401: Not authenticated
  - 403: Employee role cannot access this endpoint
```

---

**API: Get Employee Profile**

```
API Name:         Get Employee Profile
Purpose:          Returns a single employee's profile
HTTP Method:      GET
Endpoint:         /api/v1/employees/{employee_id}
Actor:            Admin (any), Manager (own team), Employee (own only)
Authentication:   Bearer JWT
Required Permission: Role-scoped

Response (200 OK):
  - employee: { id, full_name, email, role, joining_date, department, job_title, manager, status, created_at }

Errors:
  - 401: Not authenticated
  - 403: Requester does not have scope to this employee
  - 404: Employee not found
```

---

**API: Update Employee Profile**

```
API Name:         Update Employee Profile
Purpose:          Updates an employee's profile fields
HTTP Method:      PATCH
Endpoint:         /api/v1/employees/{employee_id}
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Request (all fields optional):
  - full_name: string
  - role: enum ("Manager" | "Employee")
  - joining_date: date
  - department: string
  - job_title: string

Response (200 OK):
  - Updated employee object

Errors:
  - 401: Not authenticated
  - 403: Not Admin
  - 404: Employee not found
  - 422: Attempted email change (not supported)
  - 422: Invalid role value
```

---

**API: Assign Manager**

```
API Name:         Assign / Reassign Manager
Purpose:          Sets or changes an employee's direct manager
HTTP Method:      PATCH
Endpoint:         /api/v1/employees/{employee_id}/manager
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Request:
  - manager_id: UUID, required (or null to remove manager assignment)

Response (200 OK):
  - employee: { id, full_name, manager_id, updated_at }

Errors:
  - 401: Not authenticated
  - 403: Not Admin
  - 404: Employee not found
  - 404: manager_id not found
  - 422: Employee and manager are the same person
  - 422: Proposed manager does not have Manager or Admin role

Side Effects:
  - Manager-scoped access immediately transfers to new manager
```

---

**API: Deactivate Employee**

```
API Name:         Deactivate Employee
Purpose:          Deactivates an employee, revoking access and blocking new record creation
HTTP Method:      POST
Endpoint:         /api/v1/employees/{employee_id}/deactivate
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Response (200 OK):
  - employee: { id, full_name, status: "inactive", deactivated_at }

Errors:
  - 401: Not authenticated
  - 403: Not Admin
  - 404: Employee not found
  - 409: Employee already inactive
  - 422: Cannot deactivate the sole Admin of the organization

Side Effects:
  - User record status set to deactivated
  - All active JWT refresh tokens for this user revoked
  - All PENDING leave requests for this employee auto-rejected with system note
```

---

## Module 3 — Work Tracker

### 1. Purpose

Allows employees to log what they worked on each day, and allows managers and admins to review team work activity.

### 2. Why It Exists

Without a work log, managers have no visibility into daily output. This is the core "tracking" value proposition.

### 3. MVP Scope

Simple daily work entry with title, optional description, optional duration. No projects, no tags, no approval workflow.

### 4. Features

---

#### Feature: Create Work Entry

**Actor:** Employee, Manager, Admin (all creating for themselves)

**Main Flow:**
1. Employee submits title, date, optional description, optional duration.
2. System validates inputs (date is not in future, employee is active).
3. System creates a WorkEntry record.

**Failure Conditions:**
- Date is in the future → 422.
- Employee is deactivated → 403.
- Title missing → 422.
- Duration is negative or zero → 422.

---

#### Feature: Edit Own Work Entry

**Main Flow:**
1. Employee submits updated fields.
2. System checks if the entry is within the 24-hour edit window.
3. System updates the entry.

**Alternate Flow (Admin editing locked entry):** Admin can edit any entry regardless of the lock.

**Failure Conditions:**
- Entry is locked (>24h old) and requester is not Admin → 422 "Edit window has expired."
- Entry does not belong to requester and requester is not Admin → 403.

---

### 5. Business Rules

- An employee can create multiple work entries per day. No enforced daily limit.
- Date must not be in the future.
- Title is required; description and duration are optional.
- Duration, if provided, is stored as a positive integer in minutes.
- An employee can edit their own work entry within 24 hours of creation.
- After 24 hours, the entry is locked for the employee. Only Admin can edit a locked entry.
- Work entries are never deleted.

### 6. Permissions

| Action | Admin | Manager | Employee |
|--------|-------|---------|----------|
| Create own work entry | ✅ | ✅ | ✅ |
| View own work entries | ✅ | ✅ | ✅ |
| Edit own work entry (within 24h) | ✅ | ✅ | ✅ |
| Edit locked entry | ✅ | ❌ | ❌ |
| View team work entries | ✅ | Own team ✅ | ❌ |

### 7. Cross-Module Effects

- Work entries feed the Dashboard work activity summary.

### 8. APIs

---

**API: Create Work Entry**

```
API Name:         Create Work Entry
Purpose:          Creates a daily work entry for the authenticated employee
HTTP Method:      POST
Endpoint:         /api/v1/work-entries
Actor:            Employee, Manager, Admin
Authentication:   Bearer JWT
Required Permission: Authenticated, active employee

Request:
  - title: string, required, max 200 characters
  - date: date, required, must not be in future
  - description: string, optional, max 2000 characters
  - duration_minutes: integer, optional, must be > 0

Response (201 Created):
  - work_entry: { id, employee_id, date, title, description, duration_minutes, created_at, is_locked }

Errors:
  - 401: Not authenticated
  - 403: Employee is deactivated
  - 422: Date is in the future
  - 422: Title missing
  - 422: duration_minutes is zero or negative
```

---

**API: List My Work Entries**

```
API Name:         List My Work Entries
Purpose:          Returns the authenticated employee's work entries for a date range
HTTP Method:      GET
Endpoint:         /api/v1/work-entries/me
Actor:            Any authenticated user
Authentication:   Bearer JWT
Required Permission: Authenticated

Query Parameters:
  - start_date: date, optional, defaults to 7 days ago
  - end_date: date, optional, defaults to today
  - page: integer, optional, default 1
  - page_size: integer, optional, default 20, max 100

Response (200 OK):
  - work_entries: [ { id, date, title, description, duration_minutes, created_at, is_locked } ]
  - total: integer

Errors:
  - 401: Not authenticated
  - 422: end_date before start_date
```

---

**API: Get Work Entry**

```
API Name:         Get Work Entry
Purpose:          Returns a single work entry by ID
HTTP Method:      GET
Endpoint:         /api/v1/work-entries/{entry_id}
Actor:            Admin (any), Manager (own team), Employee (own)
Authentication:   Bearer JWT
Required Permission: Role-scoped

Response (200 OK):
  - work_entry: { id, employee_id, date, title, description, duration_minutes, created_at, updated_at, is_locked }

Errors:
  - 401: Not authenticated
  - 403: Requester does not have scope
  - 404: Not found
```

---

**API: Update Work Entry**

```
API Name:         Update Work Entry
Purpose:          Edits a work entry's title, description, or duration
HTTP Method:      PATCH
Endpoint:         /api/v1/work-entries/{entry_id}
Actor:            Employee (own, within 24h), Admin (any, no restriction)
Authentication:   Bearer JWT
Required Permission: Own entry within window, or Admin

Request (all optional):
  - title: string
  - description: string
  - duration_minutes: integer, must be > 0

Response (200 OK):
  - Updated work_entry object

Errors:
  - 401: Not authenticated
  - 403: Entry does not belong to requester
  - 403: Entry is locked (>24h) and requester is not Admin
  - 404: Entry not found
  - 422: duration_minutes is zero or negative
```

---

**API: List Team Work Entries**

```
API Name:         List Team Work Entries
Purpose:          Returns work entries for a manager's direct reports or all employees (Admin)
HTTP Method:      GET
Endpoint:         /api/v1/work-entries/team
Actor:            Manager (own team), Admin (all)
Authentication:   Bearer JWT
Required Permission: Manager or Admin

Query Parameters:
  - employee_id: UUID, optional
  - start_date: date, optional
  - end_date: date, optional
  - page: integer, optional, default 1
  - page_size: integer, optional, default 20, max 100

Response (200 OK):
  - work_entries: [ { id, employee: { id, full_name }, date, title, description, duration_minutes, is_locked } ]
  - total: integer

Errors:
  - 401: Not authenticated
  - 403: Employee role cannot access this endpoint
  - 403: Manager requesting entries for employee outside their team
  - 422: end_date before start_date
```

---

## Module 4 — Attendance

### 1. Purpose

Records when employees are present, absent, or on leave each working day.

### 2. Why It Exists

Attendance is the operational heartbeat of an organization. Managers need reliable, real-time visibility into team presence.

### 3. MVP Scope

Daily check-in/check-out, automatic absence marking, manual correction, leave-driven attendance updates.

### 4. Features

---

#### Feature: Check In

**Actor:** Employee, Manager, Admin (for themselves)

**Preconditions:** Employee is active. No existing check-in for today. Today's attendance is not LEAVE.

**Main Flow:**
1. Employee calls check-in endpoint.
2. System records check-in timestamp.
3. System creates AttendanceRecord for today with status = PRESENT.

**Failure Conditions:**
- Employee deactivated → 403.
- Already checked in today → 409.
- Status for today is LEAVE → 409.

---

#### Feature: Check Out

**Preconditions:** Employee has checked in today. No existing check-out.

**Main Flow:**
1. Employee calls check-out endpoint.
2. System records check-out timestamp and computes duration.

**Failure Conditions:**
- No check-in found for today → 422.
- Already checked out → 409.

---

#### Feature: Automatic Absence Marking

**Trigger:** Scheduled job at midnight in each organization's timezone.

**Main Flow:**
1. System identifies all active employees with no AttendanceRecord for today.
2. For each such employee, if today is a weekday (Mon–Fri): create AttendanceRecord with status = ABSENT.
3. Weekends (Sat, Sun) are skipped — no ABSENT record created.

**Idempotency:** The job checks for existing records before creating. Retries do not create duplicates. Job also back-fills for up to 3 missed days.

---

#### Feature: Manual Attendance Correction

**Actor:** Admin (any employee), Manager (own team)

**Preconditions:** Date is within the last 30 days.

**Main Flow:**
1. Admin/Manager submits employee ID, date, new status, override reason.
2. System validates scope and date window.
3. System upserts the AttendanceRecord (creates if none exists, updates if exists) with new status, manual_override flag = true, reason, and actor reference.

**Failure Conditions:**
- Date is more than 30 days ago → 422.
- Requester does not have scope → 403.
- Override reason not provided → 422.

---

### 5. Business Rules (Full detail in Phase 11)

- One AttendanceRecord per employee per calendar day.
- An employee can check in exactly once per day.
- An employee can check out exactly once per day.
- Weekends are not counted as working days; no ABSENT records for Sat/Sun.
- A leave-marked day blocks employee check-in.
- Manual overrides require a reason; limited to last 30 days.
- If an employee did not check out, the record remains PRESENT with no check-out. Not auto-closed in MVP.

### 6. Permissions

| Action | Admin | Manager | Employee |
|--------|-------|---------|----------|
| Check in (own) | ✅ | ✅ | ✅ |
| Check out (own) | ✅ | ✅ | ✅ |
| View own attendance | ✅ | ✅ | ✅ |
| View team attendance | ✅ | Own team ✅ | ❌ |
| Correct attendance | ✅ | Own team ✅ | ❌ |

### 7. Cross-Module Effects

- Leave module writes LEAVE status to AttendanceRecord on approval/grant.
- Dashboard reads attendance for daily team summary.

### 8. APIs

---

**API: Check In**

```
API Name:         Check In
Purpose:          Records the employee's check-in for today
HTTP Method:      POST
Endpoint:         /api/v1/attendance/check-in
Actor:            Employee, Manager, Admin (for themselves)
Authentication:   Bearer JWT
Required Permission: Authenticated, active employee

Request: No body. Timestamp = server time (UTC).

Response (201 Created):
  - attendance_record: { id, employee_id, date, status: "PRESENT", check_in: timestamp, check_out: null }

Errors:
  - 401: Not authenticated
  - 403: Employee is deactivated
  - 409: Already checked in today
  - 409: Today's attendance status is LEAVE

Side Effects:
  - AttendanceRecord created for today
```

---

**API: Check Out**

```
API Name:         Check Out
Purpose:          Records the employee's check-out for today
HTTP Method:      POST
Endpoint:         /api/v1/attendance/check-out
Actor:            Employee, Manager, Admin (for themselves)
Authentication:   Bearer JWT
Required Permission: Authenticated, active employee

Request: No body.

Response (200 OK):
  - attendance_record: { id, employee_id, date, status: "PRESENT", check_in, check_out, duration_minutes }

Errors:
  - 401: Not authenticated
  - 403: Employee is deactivated
  - 422: No check-in found for today
  - 409: Already checked out today

Side Effects:
  - AttendanceRecord updated with check-out time and duration
```

---

**API: Get Today's Attendance Status**

```
API Name:         Get Today's Attendance Status
Purpose:          Returns the authenticated employee's attendance record for today
HTTP Method:      GET
Endpoint:         /api/v1/attendance/today
Actor:            Any authenticated user
Authentication:   Bearer JWT
Required Permission: Authenticated

Response (200 OK):
  - attendance_record: { date, status, check_in, check_out, duration_minutes }
    or null if no record yet for today

Errors:
  - 401: Not authenticated
```

---

**API: Get My Attendance History**

```
API Name:         Get My Attendance History
Purpose:          Returns the authenticated employee's attendance records for a date range
HTTP Method:      GET
Endpoint:         /api/v1/attendance/me
Actor:            Any authenticated user
Authentication:   Bearer JWT
Required Permission: Authenticated

Query Parameters:
  - start_date: date, optional, defaults to start of current month
  - end_date: date, optional, defaults to today
  - page: integer, optional, default 1
  - page_size: integer, optional, default 31

Response (200 OK):
  - attendance_records: [ { id, date, status, check_in, check_out, duration_minutes, is_manually_overridden } ]
  - total: integer

Errors:
  - 401: Not authenticated
  - 422: end_date before start_date
```

---

**API: List Team Attendance**

```
API Name:         List Team Attendance
Purpose:          Returns attendance records for the manager's team or all employees (Admin)
HTTP Method:      GET
Endpoint:         /api/v1/attendance/team
Actor:            Manager (own team), Admin (all)
Authentication:   Bearer JWT
Required Permission: Manager or Admin

Query Parameters:
  - date: date, optional (single-day view)
  - start_date: date, optional
  - end_date: date, optional
  - employee_id: UUID, optional
  - status: enum ("PRESENT" | "ABSENT" | "LEAVE"), optional
  - page: integer, optional, default 1
  - page_size: integer, optional, default 20

Response (200 OK):
  - attendance_records: [
      { employee: { id, full_name }, date, status, check_in, check_out, duration_minutes, is_manually_overridden }
    ]
  - total: integer

Errors:
  - 401: Not authenticated
  - 403: Employee role cannot access team view
  - 403: Manager requesting data for employee outside their team
  - 422: Both single date and range provided simultaneously
  - 422: end_date before start_date
```

---

**API: Correct Attendance Record**

```
API Name:         Correct Attendance Record
Purpose:          Manually creates or updates an attendance record for a given employee and date
HTTP Method:      POST
Endpoint:         /api/v1/attendance/correct
Actor:            Admin (any), Manager (own team)
Authentication:   Bearer JWT
Required Permission: Admin or Manager (with scope)

Request:
  - employee_id: UUID, required
  - date: date, required, must be within last 30 days
  - status: enum ("PRESENT" | "ABSENT" | "LEAVE"), required
  - override_reason: string, required, max 500 characters

Response (200 OK):
  - attendance_record: { id, employee_id, date, status, is_manually_overridden, override_reason, overridden_by, overridden_at }

Errors:
  - 401: Not authenticated
  - 403: Requester does not have scope for this employee
  - 404: Employee not found
  - 422: Date is older than 30 days
  - 422: override_reason not provided

Side Effects:
  - If new status is LEAVE but no Leave Record exists: warning included in response, override proceeds
  - Leave balance is NOT automatically adjusted by this action

Notes:
  - Upserts: creates AttendanceRecord if none exists for employee+date; updates if exists
```

---

## Module 5 — Leave

### 1. Purpose

Manages the complete lifecycle of employee leave — configuration, balance tracking, requests, approvals, direct grants, and automatic allocation.

### 2. Why It Exists

Leave is the most operationally impactful module. Without it, organizations cannot manage absences, entitlements, or attendance accuracy.

### 3. MVP Scope

Leave types, policy rules, balance tracking, employee requests, manager approval/rejection, employee cancel, manager direct grant, automatic allocation job.

### 4. Features

---

#### Feature: Create Leave Type

**Actor:** Admin

**Main Flow:**
1. Admin submits leave type name, code, optional description.
2. System validates uniqueness within org.
3. System creates LeaveType record.

**Failure Conditions:** Duplicate name or code → 409.

---

#### Feature: Configure Leave Policy Rule

**Actor:** Admin

**Main Flow:**
1. Admin submits leave type ID, allocation amount, frequency, minimum tenure, max balance cap, pro-ration flag.
2. System validates and upserts LeavePolicyRule.

**Note:** Changes apply to future allocations only.

---

#### Feature: Employee Leave Request

**Actor:** Employee, Manager, Admin (for themselves)

**Preconditions:** Employee is active; sufficient balance; no overlapping pending/approved/granted leave.

**Main Flow:**
1. Employee submits leave type, start date, end date, optional reason.
2. System calculates working days (excludes weekends).
3. System checks balance and overlaps.
4. System creates LeaveRecord with status = PENDING.

**Failure Conditions:**
- Insufficient balance → 422.
- Overlapping leave → 422.
- Start date > end date → 422.
- Start date more than 7 days in the past → 422.
- Leave type not found or inactive → 422.
- No balance record exists for this leave type → 422 "No leave balance. Contact your admin."

---

#### Feature: Approve Leave Request

**Actor:** Manager (own team), Admin (any)

**Main Flow:**
1. Manager approves a PENDING request.
2. System re-validates balance.
3. System updates status to APPROVED.
4. System deducts days_count from LeaveBalance.
5. System updates AttendanceRecord for each working day in range to status = LEAVE.
   - If record already exists (employee checked in): status is overridden to LEAVE; existing check-in data preserved.
   - If no record exists: creates one with status = LEAVE.
6. Email notification sent to employee.

**Failure Conditions:**
- Not PENDING → 409.
- Manager out of scope → 403.
- Insufficient balance at time of approval → 422.

---

#### Feature: Reject Leave Request

**Actor:** Manager (own team), Admin (any)

**Main Flow:**
1. Manager rejects a PENDING request with optional reason.
2. Status → REJECTED. Balance and attendance unchanged.
3. Email notification sent to employee.

---

#### Feature: Cancel Leave Request

**Actor:** Employee (own requests only)

**Preconditions:** Request is PENDING.

**Main Flow:**
1. Employee cancels their own PENDING request.
2. Status → CANCELLED. Balance and attendance unchanged.

**Failure Conditions:** Request is not PENDING → 409.

---

#### Feature: Manager Direct Leave Grant

**Actor:** Manager (own team), Admin (any)

**Main Flow:**
1. Manager submits employee ID, leave type, start date, end date, optional reason.
2. System computes working days, checks overlap, checks balance.
3. System creates LeaveRecord with status = GRANTED.
4. System deducts days_count from LeaveBalance.
5. System updates AttendanceRecord for all working days in range to LEAVE.
6. Email notification sent to employee.

---

#### Feature: Automatic Leave Allocation

**Actor:** System (scheduled job)

**Trigger:** Start of each period based on policy frequency (1st of month / 1st of quarter / Jan 1st).

**Main Flow:**
1. Load all leave policy rules for all active organizations.
2. For each rule, for each active employee:
   a. Check tenure eligibility.
   b. Check if already allocated for this period (idempotency).
   c. Compute allocation amount (with pro-ration if first allocation and rule flag is true).
   d. Cap at max_balance_cap.
   e. Update LeaveBalance.
3. Log each allocation run per period (prevents double-allocation on retry).

---

### 5. Business Rules (Full detail in Phase 10)

- Balance cannot go below 0.
- Only PENDING requests can be cancelled, approved, or rejected.
- APPROVED and GRANTED leaves trigger attendance = LEAVE.
- REJECTED and CANCELLED leaves do not affect balance or attendance.
- Overlapping PENDING/APPROVED/GRANTED leaves cannot coexist.
- Retroactive requests limited to 7 days in the past.
- Leave year = calendar year (Jan 1 – Dec 31). Resets to 0 at year start (no carry-forward).
- Weekends excluded from leave day count.
- Automatic allocation is idempotent per period.
- Allocation does not create LeaveRecord entries; it only updates LeaveBalance.

### 6. Permissions

| Action | Admin | Manager | Employee |
|--------|-------|---------|----------|
| Create leave type | ✅ | ❌ | ❌ |
| Configure policy | ✅ | ❌ | ❌ |
| View own balance | ✅ | ✅ | ✅ |
| View team balance | ✅ | Own team ✅ | ❌ |
| Request leave (own) | ✅ | ✅ | ✅ |
| Cancel own PENDING request | ✅ | ✅ | ✅ |
| Approve/reject team leave | ✅ | Own team ✅ | ❌ |
| Grant leave (direct) | ✅ | Own team ✅ | ❌ |
| Run auto-allocation | System only | ❌ | ❌ |

### 7. Cross-Module Effects

- Leave approval/grant → Attendance updated to LEAVE for all working days.
- Leave module reads Employee joining_date for eligibility.
- Dashboard reads leave balances and pending requests.

### 8. APIs

---

**API: Create Leave Type**

```
API Name:         Create Leave Type
Purpose:          Creates a new leave category for the organization
HTTP Method:      POST
Endpoint:         /api/v1/leave/types
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Request:
  - name: string, required, unique within org
  - code: string, required, 2–10 uppercase characters, unique within org
  - description: string, optional

Response (201 Created):
  - leave_type: { id, name, code, description, is_active, created_at }

Errors:
  - 401: Not authenticated
  - 403: Not Admin
  - 409: Name or code already exists in this organization
```

---

**API: List Leave Types**

```
API Name:         List Leave Types
Purpose:          Returns all leave types for the organization
HTTP Method:      GET
Endpoint:         /api/v1/leave/types
Actor:            Any authenticated user
Authentication:   Bearer JWT
Required Permission: Authenticated

Query Parameters:
  - is_active: boolean, optional, defaults to true

Response (200 OK):
  - leave_types: [ { id, name, code, description, is_active } ]

Errors:
  - 401: Not authenticated
```

---

**API: Configure Leave Policy Rule**

```
API Name:         Configure Leave Policy Rule
Purpose:          Creates or updates the automatic allocation rule for a leave type
HTTP Method:      PUT
Endpoint:         /api/v1/leave/policy/rules/{leave_type_id}
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Request:
  - allocation_amount: integer, required, must be > 0
  - allocation_frequency: enum ("MONTHLY" | "QUARTERLY" | "ANNUALLY"), required
  - minimum_tenure_days: integer, required, >= 0
  - max_balance_cap: integer, required, >= allocation_amount
  - is_pro_rated_on_joining: boolean, required

Response (200 OK):
  - policy_rule: { leave_type_id, allocation_amount, allocation_frequency,
                   minimum_tenure_days, max_balance_cap, is_pro_rated_on_joining, updated_at }

Errors:
  - 401: Not authenticated
  - 403: Not Admin
  - 404: Leave type not found
  - 422: max_balance_cap < allocation_amount
  - 422: allocation_amount <= 0

Side Effects:
  - Changes apply to future allocation runs only
```

---

**API: Get Leave Policy**

```
API Name:         Get Leave Policy
Purpose:          Returns the organization's leave policy rules for all leave types
HTTP Method:      GET
Endpoint:         /api/v1/leave/policy
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Response (200 OK):
  - policy_rules: [
      { leave_type: { id, name, code }, allocation_amount, allocation_frequency,
        minimum_tenure_days, max_balance_cap, is_pro_rated_on_joining }
    ]

Errors:
  - 401: Not authenticated
  - 403: Not Admin
```

---

**API: Get Leave Balance**

```
API Name:         Get Leave Balance
Purpose:          Returns leave balances for an employee for the current or specified leave year
HTTP Method:      GET
Endpoint:         /api/v1/leave/balance/{employee_id}
  (Use "me" as employee_id for own balance: /api/v1/leave/balance/me)
Actor:            Admin (any), Manager (own team), Employee (own only)
Authentication:   Bearer JWT
Required Permission: Role-scoped

Query Parameters:
  - leave_year: integer, optional, defaults to current year

Response (200 OK):
  - balances: [
      { leave_type: { id, name, code }, balance, total_allocated, total_used, leave_year }
    ]
  Note: Leave types with no balance record return balance = 0.

Errors:
  - 401: Not authenticated
  - 403: Requester does not have scope
  - 404: Employee not found
```

---

**API: Submit Leave Request**

```
API Name:         Submit Leave Request
Purpose:          Creates a leave request pending manager approval
HTTP Method:      POST
Endpoint:         /api/v1/leave/requests
Actor:            Employee, Manager, Admin (for themselves)
Authentication:   Bearer JWT
Required Permission: Authenticated, active employee

Request:
  - leave_type_id: UUID, required
  - start_date: date, required
  - end_date: date, required, >= start_date
  - reason: string, optional, max 500 characters

Response (201 Created):
  - leave_request: { id, employee_id, leave_type, start_date, end_date,
                     days_count, status: "PENDING", reason, created_at }

Errors:
  - 401: Not authenticated
  - 403: Employee is deactivated
  - 404: Leave type not found or inactive
  - 422: end_date before start_date
  - 422: start_date more than 7 days in the past
  - 422: Insufficient leave balance
  - 422: No leave balance record exists for this type ("Contact your admin")
  - 422: Overlapping pending or approved/granted leave exists

Side Effects:
  - LeaveRecord created with status PENDING
```

---

**API: List My Leave Requests**

```
API Name:         List My Leave Requests
Purpose:          Returns the authenticated employee's leave requests
HTTP Method:      GET
Endpoint:         /api/v1/leave/requests/me
Actor:            Any authenticated user
Authentication:   Bearer JWT
Required Permission: Authenticated

Query Parameters:
  - status: enum, optional
  - start_date: date, optional
  - end_date: date, optional
  - page: integer, optional, default 1
  - page_size: integer, optional, default 20

Response (200 OK):
  - leave_requests: [ { id, leave_type, start_date, end_date, days_count,
                        status, reason, created_at, decided_at } ]
  - total: integer

Errors:
  - 401: Not authenticated
```

---

**API: List Team Leave Requests**

```
API Name:         List Team Leave Requests
Purpose:          Returns leave requests for the manager's team or all employees (Admin)
HTTP Method:      GET
Endpoint:         /api/v1/leave/requests/team
Actor:            Manager (own team), Admin (all)
Authentication:   Bearer JWT
Required Permission: Manager or Admin

Query Parameters:
  - employee_id: UUID, optional
  - status: enum, optional
  - start_date: date, optional
  - end_date: date, optional
  - page: integer, optional, default 1
  - page_size: integer, optional, default 20

Response (200 OK):
  - leave_requests: [
      { id, employee: { id, full_name }, leave_type, start_date, end_date,
        days_count, status, reason, created_at }
    ]
  - total: integer

Errors:
  - 401: Not authenticated
  - 403: Employee cannot access team requests
  - 403: Manager requesting for employee outside their team
```

---

**API: Approve Leave Request**

```
API Name:         Approve Leave Request
Purpose:          Approves a pending leave request
HTTP Method:      POST
Endpoint:         /api/v1/leave/requests/{request_id}/approve
Actor:            Manager (own team), Admin (any)
Authentication:   Bearer JWT
Required Permission: Manager or Admin (with scope)

Request: No body required.

Response (200 OK):
  - leave_request: { id, status: "APPROVED", decided_by, decided_at,
                     employee_id, leave_type, start_date, end_date, days_count }

Errors:
  - 401: Not authenticated
  - 403: Requester does not have scope
  - 404: Leave request not found
  - 409: Leave request is not PENDING
  - 422: Insufficient balance at time of approval

Side Effects:
  - LeaveBalance reduced by days_count
  - AttendanceRecord for each working day in range set to LEAVE
  - Email notification sent to employee
```

---

**API: Reject Leave Request**

```
API Name:         Reject Leave Request
Purpose:          Rejects a pending leave request
HTTP Method:      POST
Endpoint:         /api/v1/leave/requests/{request_id}/reject
Actor:            Manager (own team), Admin (any)
Authentication:   Bearer JWT
Required Permission: Manager or Admin (with scope)

Request:
  - reason: string, optional, max 500 characters

Response (200 OK):
  - leave_request: { id, status: "REJECTED", decided_by, decided_at, rejection_reason }

Errors:
  - 401: Not authenticated
  - 403: Requester does not have scope
  - 404: Leave request not found
  - 409: Leave request is not PENDING

Side Effects:
  - Email notification sent to employee
  - Balance and attendance NOT affected
```

---

**API: Cancel Leave Request**

```
API Name:         Cancel Leave Request
Purpose:          Cancels the employee's own pending leave request
HTTP Method:      POST
Endpoint:         /api/v1/leave/requests/{request_id}/cancel
Actor:            Employee, Manager, Admin (own requests only)
Authentication:   Bearer JWT
Required Permission: Authenticated (own request)

Request: No body required.

Response (200 OK):
  - leave_request: { id, status: "CANCELLED", cancelled_at }

Errors:
  - 401: Not authenticated
  - 403: Request does not belong to requester
  - 404: Leave request not found
  - 409: Request is not PENDING

Side Effects:
  - Balance and attendance NOT affected
```

---

**API: Grant Leave (Direct)**

```
API Name:         Grant Leave
Purpose:          Directly grants leave to an employee without a prior employee request
HTTP Method:      POST
Endpoint:         /api/v1/leave/grants
Actor:            Manager (own team), Admin (any)
Authentication:   Bearer JWT
Required Permission: Manager or Admin (with scope)

Request:
  - employee_id: UUID, required
  - leave_type_id: UUID, required
  - start_date: date, required
  - end_date: date, required, >= start_date
  - reason: string, optional, max 500 characters

Response (201 Created):
  - leave_grant: { id, employee_id, leave_type, start_date, end_date,
                   days_count, status: "GRANTED", granted_by, granted_at, reason }

Errors:
  - 401: Not authenticated
  - 403: Requester does not have scope
  - 403: Employee is deactivated
  - 404: Employee not found
  - 404: Leave type not found
  - 422: end_date before start_date
  - 422: Insufficient leave balance
  - 422: Overlapping approved/granted/pending leave exists

Side Effects:
  - LeaveBalance reduced by days_count
  - AttendanceRecord for each working day in range set to LEAVE
  - Email notification sent to employee
```

---

## Module 6 — Dashboard

### 1. Purpose

Provides role-appropriate operational summaries for immediate visibility on login.

### 2. Why It Exists

Without a dashboard, users must navigate multiple modules to understand operational status. The dashboard synthesizes the most important information for each role.

### 3. MVP Scope

Three role-specific read-only dashboards. No charts, no mutations, no date-range filtering.

### 8. APIs

---

**API: Employee Dashboard**

```
API Name:         Get Employee Dashboard
Purpose:          Returns the authenticated employee's operational summary
HTTP Method:      GET
Endpoint:         /api/v1/dashboard/me
Actor:            Any authenticated user
Authentication:   Bearer JWT
Required Permission: Authenticated

Response (200 OK):
  - today_attendance: { status, check_in, check_out } or null
  - leave_balances: [ { leave_type: { name, code }, balance } ]
  - upcoming_leave: [ { leave_type, start_date, end_date, days_count, status } ]
    (next 30 days, APPROVED/GRANTED status only)
  - pending_leave_requests: [ { id, leave_type, start_date, end_date, status: "PENDING" } ]
  - recent_work_entries: [ { date, title, duration_minutes } ] (last 5 entries)

Errors:
  - 401: Not authenticated

Notes:
  - All data computed in real time from underlying records
  - Data is always scoped to the authenticated user
```

---

**API: Manager Dashboard**

```
API Name:         Get Manager Dashboard
Purpose:          Returns team-level operational summary for a manager
HTTP Method:      GET
Endpoint:         /api/v1/dashboard/team
Actor:            Manager, Admin
Authentication:   Bearer JWT
Required Permission: Manager or Admin

Response (200 OK):
  - team_size: integer (active direct reports)
  - today_attendance_summary:
      { present_count, absent_count, on_leave_count, not_yet_checked_in_count }
  - team_attendance_today: [ { employee: { id, full_name }, status, check_in, check_out } ]
  - pending_leave_requests:
      [ { id, employee: { id, full_name }, leave_type, start_date, end_date, days_count } ]
  - employees_on_leave_this_week:
      [ { employee: { id, full_name }, leave_type, start_date, end_date } ]

Errors:
  - 401: Not authenticated
  - 403: Employee role cannot access team dashboard
```

---

**API: Admin Dashboard**

```
API Name:         Get Admin Dashboard
Purpose:          Returns organization-wide operational summary for Admin
HTTP Method:      GET
Endpoint:         /api/v1/dashboard/org
Actor:            Admin
Authentication:   Bearer JWT
Required Permission: Admin

Response (200 OK):
  - total_active_employees: integer
  - today_attendance_summary:
      { present_count, absent_count, on_leave_count, not_yet_checked_in_count }
  - leave_requests_pending_count: integer
  - leave_policy_configured: boolean

Errors:
  - 401: Not authenticated
  - 403: Not Admin
```

---

# PHASE 9 — CRITICAL BUSINESS WORKFLOWS

## 9.1 Employee Onboarding

```
1. Unauthenticated user navigates to registration
2. User provides organization name, own name, email, password
3. System creates: Organization → Admin Employee → Admin User
4. Admin logs in with credentials
5. Admin creates leave types (e.g., Annual Leave, Sick Leave)
6. Admin configures leave policy rules per leave type
7. Admin creates employees:
   a. Submits employee details (name, email, role, joining date, optional manager)
   b. System creates Employee record → User record
   c. Invite email sent to new employee
8. New employee receives invite, sets password
9. New employee logs in
10. New employee sees their dashboard
    (attendance = no record yet; leave balances = 0 until allocation runs)
```

**Outcome:** Organization is operational. Employees can check in, log work, and request leave.

---

## 9.2 Daily Work Tracking

```
1. Employee logs in (if not already)
2. Employee creates a work entry:
   - Title (required)
   - Date (defaults to today)
   - Optional description and duration
3. System saves entry
4. Employee can create multiple entries for the same day
5. Employee can edit any entry within 24 hours of creation
6. After 24 hours, entries are locked for the employee
7. Manager can view team entries anytime
8. Admin can edit any locked entry if correction is needed
```

---

## 9.3 Daily Attendance

```
1. Employee arrives and calls the check-in API
   → AttendanceRecord created: status = PRESENT, check_in = now
2. Employee works
3. Employee calls check-out API at end of day
   → AttendanceRecord updated: check_out = now, duration computed
4. Scenario: Employee forgets to check out
   → Record remains PRESENT with no check_out (open record)
   → Admin/Manager can correct via manual override
```

---

## 9.4 Automatic Absence Marking

```
Trigger: Scheduled job at midnight in each organization's timezone

For each active organization:
  For each active employee:
    If today is Saturday or Sunday → skip entirely
    Check if AttendanceRecord exists for today:
      If no record:
        → Create AttendanceRecord with status = ABSENT
      If record exists (any status):
        → No action taken

Recovery: Job back-fills for up to 3 previous days on each run to handle failures.
```

---

## 9.5 Employee Leave Request Flow

```
1. Employee checks leave balance
2. Employee submits leave request: leave type, start date, end date, optional reason
3. System validates:
   - Sufficient balance
   - No overlapping leave
   - Date not retroactively > 7 days
4. LeaveRecord created with status = PENDING
5. Manager sees request in pending leave queue (dashboard and API)
6a. Manager approves:
    - System deducts days from balance
    - System sets AttendanceRecord to LEAVE for each working day
    - Status → APPROVED
    - Employee notified by email
6b. Manager rejects:
    - Status → REJECTED
    - Balance unchanged; attendance unchanged
    - Employee notified by email
7. Employee views decision on their leave request list
```

---

## 9.6 Manager Direct Leave Grant

```
1. Manager calls Grant Leave API:
   employee ID, leave type, start date, end date, optional reason
2. System validates:
   - Manager has scope to this employee
   - Employee is active
   - Sufficient balance
   - No overlapping leave
3. System creates LeaveRecord with status = GRANTED
4. System deducts days from LeaveBalance
5. System sets AttendanceRecord for all working days in range to LEAVE
6. Email notification sent to employee
```

---

## 9.7 Automatic Leave Allocation

```
Trigger: Scheduled job runs at the beginning of each allocation period
         (monthly: 1st of month; quarterly: 1st of Jan/Apr/Jul/Oct; annually: Jan 1st)

For each active organization:
  Load leave policy rules
  For each rule:
    For each active employee in the organization:
      1. Compute tenure: today - joining_date (in days)
      2. If tenure < minimum_tenure_days → skip
      3. Check if already allocated for this period → skip if yes (idempotency)
      4. Load LeaveBalance (or treat as 0 if not exists)
      5. If balance >= max_balance_cap → skip
      6. Compute allocation:
         If is_first_allocation AND is_pro_rated_on_joining:
           allocation = floor(allocation_amount × (days_employed_in_period / total_period_days))
         Else:
           allocation = allocation_amount
      7. Cap: if balance + allocation > max_balance_cap:
           allocation = max_balance_cap - balance
      8. Update LeaveBalance (add allocation)
      9. Log this run in AllocationLog (prevents double-allocation)

Outcome: Eligible employees receive leave credits. No LeaveRecord entries created.
```

---

# PHASE 10 — LEAVE SYSTEM DEEP ANALYSIS

## 10.1 Leave Policy

An organization's admin must configure:
- **Leave Types**: At least one required before leave can be used.
- **Policy Rules per Leave Type**: Allocation amount, frequency, minimum tenure, balance cap, pro-ration.
- Policy applies uniformly to all employees. Per-employee overrides are Post-MVP.

## 10.2 Leave Balance Calculation

```
Current Balance = Total Allocated (this year) − Total Used (this year)
```

"Used" means days where a LeaveRecord with status APPROVED or GRANTED exists.

The LeaveBalance entity holds the authoritative figure. It is updated atomically on every leave event.

A missing LeaveBalance record implies balance = 0.

## 10.3 Leave Grant (Manager-Initiated)

- Manager selects employee, leave type, dates.
- System validates balance and overlap.
- LeaveRecord created with status = GRANTED.
- LeaveBalance decremented by days_count.
- AttendanceRecord updated to LEAVE for all working days in range.
- Grant is immediate and irrevocable in MVP.

## 10.4 Automatic Allocation

Allocation is a **balance credit event**, not a leave event. No LeaveRecord is created. Only LeaveBalance is updated.

**Trigger:** Scheduled job at the start of each period.

**Idempotency:** Before allocating, the system checks the AllocationLog for a record of this period (organization_id + leave_type_id + period_start + period_end). If found, the run is skipped. This prevents double-allocation on job retry.

## 10.5 Leave Deduction

Balance is deducted **only when**:
1. A leave request is **approved** (APPROVED status).
2. A manager directly **grants** leave (GRANTED status).

Balance is **not deducted** when a request is PENDING, REJECTED, or CANCELLED.

## 10.6 Cancellation

Only PENDING requests can be cancelled in MVP.

An employee cannot cancel an APPROVED or GRANTED leave. A manager wanting to undo approved leave must use manual attendance correction. Balance is NOT restored by manual attendance correction (MVP limitation — accepted).

## 10.7 Overlapping Leave

Overlap definition: two leave records overlap if:
```
new.start_date <= existing.end_date AND new.end_date >= existing.start_date
```

The system rejects any request or grant that overlaps with an existing PENDING, APPROVED, or GRANTED leave record for the same employee.

## 10.8 Insufficient Balance

If requested days exceed current balance, the system returns 422. Managers cannot override the balance restriction in MVP. This is a deliberate simplicity decision.

## 10.9 Joining Date and Eligibility

- An employee's joining date determines tenure.
- Employees below minimum_tenure_days are skipped in allocation runs.
- Pro-ration on first allocation applies only if the policy rule has `is_pro_rated_on_joining = true`.

## 10.10 Leave Year and Year Boundary

- Leave year = calendar year (January 1 to December 31).
- On January 1:
  1. Previous year LeaveBalance records are frozen (no further changes).
  2. New year LeaveBalance records initialized to 0.
  3. Annual allocation job runs (if ANNUALLY frequency), crediting the first allocation.
- Net effect: employee's January 1 balance = 0 + first allocation amount (subject to tenure and pro-ration).

## 10.11 Carry Forward

**Post-MVP.** All unused leave is forfeited at year-end. This is an accepted MVP limitation.

## 10.12 Attendance Interaction

When leave is approved or granted, for each calendar day from start_date to end_date (inclusive):

1. If the day is Saturday or Sunday → **skip** (no attendance record created or updated).
2. If an AttendanceRecord already exists for this employee-date:
   - Set status = LEAVE.
   - Set leave_record_id = this leave record.
   - Preserve existing check_in/check_out data.
3. If no AttendanceRecord exists:
   - Create one with status = LEAVE, leave_record_id = this leave record.

The absence marking job will not create ABSENT records for dates that already have any AttendanceRecord (including LEAVE).

---

# PHASE 11 — ATTENDANCE DEEP ANALYSIS

## 11.1 Check-In Definition

Check-in is the act of calling `/api/v1/attendance/check-in`. It is a digital self-declaration. No GPS, biometric, or IP validation in MVP.

## 11.2 Can an Employee Check In Twice?

No. Exactly once per calendar day. Second attempt returns 409 Conflict.

## 11.3 What Happens If They Forget to Check Out?

Record remains PRESENT with null check_out (open record). Not auto-closed in MVP. Admin or Manager can correct via the manual attendance correction API.

## 11.4 Can Employees Edit Attendance?

No. Employees cannot edit their own attendance records. Self-service attendance editing is Post-MVP. Only Admin and Manager can correct via the correction API.

## 11.5 Can a Manager Correct Attendance?

Yes. A Manager can correct attendance for their direct reports using the correction API. Requirements:
- Valid reason (required field).
- Date within the last 30 days.

## 11.6 How Is Absence Determined?

A scheduled job runs at midnight in the organization's timezone. For each active employee with no AttendanceRecord for the day, and if the day is not Saturday or Sunday, an ABSENT record is created.

## 11.7 How Does Leave Affect Attendance?

Leave approval/grant writes LEAVE status to AttendanceRecord. The absence marking job finds a record already exists (status = LEAVE) and takes no action. The LEAVE record prevents the absence mark from being applied.

## 11.8 What Happens on Weekends?

Saturday and Sunday are non-working days:
- No ABSENT records are created for Sat/Sun.
- When computing leave days, Sat/Sun are excluded.
- Employees are not expected to check in on weekends.

## 11.9 What Happens on Holidays?

**Post-MVP.** No holiday calendar in MVP. All non-weekend weekdays are working days. Public holidays will cause incorrect absence records if employees don't check in. Manual correction is the workaround for MVP.

## 11.10 Timezone Handling

Organization's configured timezone determines:
- What "today" means for check-in/check-out.
- When the absence marking job fires (midnight in org timezone).
- Which dates fall in a leave range.

All timestamps stored in UTC. Day boundaries computed by converting to org timezone.

## 11.11 Manual Override

Admin and Manager can override any attendance record using the correction API. The override:
- Upserts the record (creates if none exists).
- Sets the `is_manually_overridden` flag.
- Records who made the correction and when.
- Requires a reason (max 500 characters).
- Is limited to the last 30 days.

If status is manually set to LEAVE without an underlying LeaveRecord, the system includes a warning in the response but proceeds.

## 11.12 Absence Marking Job Idempotency

The job is idempotent: the unique constraint on (employee_id, date) prevents duplicate ABSENT records. On each run, the job also back-fills for up to 3 previous days to recover from past failures.

---

# PHASE 12 — WORK TRACKER DEEP ANALYSIS

## 12.1 What Is a Work Entry?

A record of a discrete unit of work performed on a specific date. It is a narrative log, not a time-clock record.

## 12.2 Can Multiple Entries Exist Per Day?

Yes. No enforced daily limit.

## 12.3 Can Employees Edit Old Entries?

Only within 24 hours of the `created_at` timestamp of the specific entry. After that, locked for the employee. The 24-hour window is measured per-entry, not per-day.

## 12.4 Can Managers Edit Employee Work?

No, in MVP. Admin can edit locked entries. Managers only view.

## 12.5 Who Can See Work Entries?

- Employee: own entries only.
- Manager: entries of their direct reports.
- Admin: entries of all employees in the organization.

## 12.6 Can Work Entries Be Deleted?

No. Work entries are permanent. The work log is an audit trail.

## 12.7 Is Time Duration Required?

No. Duration in minutes is optional. Many employees will not track hours; forcing duration reduces adoption.

## 12.8 Is Start/End Time Required?

No. MVP tracks only optional total duration. Start/end time tracking is Post-MVP.

## 12.9 Is a Task/Project Concept Required?

No. MVP has no project model. Adding projects would create project CRUD, employee-project assignments, and project reporting — this turns the work tracker into a project management tool. MVP stays with free-text title, description, and optional duration.

---

# PHASE 13 — DASHBOARD DEFINITION

## 13.1 Employee Dashboard

Answers: "Am I checked in? What's my leave balance? Do I have upcoming leave? What did I recently work on?"

| Metric | Source |
|--------|--------|
| Today's Attendance Status | Attendance module |
| Leave Balances (all leave types) | Leave module |
| Upcoming Leave (next 30 days, APPROVED/GRANTED) | Leave module |
| Pending Leave Requests | Leave module |
| Recent Work Entries (last 5) | Work Tracker |

## 13.2 Manager Dashboard

Answers: "Who is in today? Who is absent? Who needs leave approved? Who is going on leave this week?"

| Metric | Source |
|--------|--------|
| Team Size (active direct reports) | Employee module |
| Today's Attendance Summary | Attendance module |
| Team Attendance Today (per-employee) | Attendance module |
| Pending Leave Requests (from team) | Leave module |
| Team on Leave This Week | Leave module |

## 13.3 Admin Dashboard

Answers: "How many active employees? What is org-wide attendance? Are there pending leave requests? Is the leave policy set up?"

| Metric | Source |
|--------|--------|
| Total Active Employees | Employee module |
| Org-Wide Attendance Summary Today | Attendance module |
| Org-Wide Pending Leave Request Count | Leave module |
| Leave Policy Configured Flag | Leave module |

## 13.4 Dashboard Non-Goals (MVP)

- No charts or graphs.
- No trend analysis.
- No date-range filtering on dashboard (use module-specific APIs).
- No exportable reports.

---

# PHASE 14 — CROSS-MODULE RULES

```
RULE-01: An employee must exist and be active before work entries can be created for them.

RULE-02: An employee must exist and be active before attendance records can be created for them.

RULE-03: An employee must exist and be active before leave can be requested by or granted to them.

RULE-04: An organization must exist before any employee, work entry, attendance record,
         or leave record can be created.

RULE-05: Leave module is the source of truth for leave status.
         Attendance module reflects leave status but does not own it.

RULE-06: When leave is approved or granted, the Leave module writes LEAVE status to
         AttendanceRecord for all working days (Mon–Fri) in the leave date range.
         If an AttendanceRecord already exists, it is updated. If none exists, one is created.
         Weekend days (Sat/Sun) are skipped.

RULE-07: Deactivating an employee does not delete any historical records.
         All work entries, attendance records, and leave records remain intact and readable
         by managers and admins.

RULE-08: Deactivating an employee auto-rejects all their PENDING leave requests
         with a system-generated rejection note ("Employee deactivated").

RULE-09: A deactivated employee cannot check in, log work, or submit leave requests.

RULE-10: Managers can only access records belonging to their direct reports.
         Reassigning an employee's manager immediately transfers access scope.

RULE-11: An admin can access all records within their organization.
         An admin cannot access records in any other organization.

RULE-12: No API can return data belonging to a different organization than the
         authenticated user's organization. Every query is filtered by organization_id.

RULE-13: The organization's timezone is used for all day-boundary calculations.
         All timestamps are stored in UTC.

RULE-14: Leave balance cannot go below 0. No override or grant can reduce balance below 0.

RULE-15: Leave days are counted by excluding weekends (Saturday, Sunday).
         The system computes days_count; the requesting user provides only dates.

RULE-16: Only PENDING leave requests can be approved, rejected, or cancelled.
         Once a request reaches a terminal state (APPROVED, REJECTED, CANCELLED, GRANTED),
         it cannot be modified in MVP.

RULE-17: Absence records are not created for Saturdays and Sundays.

RULE-18: There can be at most one AttendanceRecord per employee per calendar day.
         The (employee_id, date) combination is unique.

RULE-19: Automatic leave allocation does not create LeaveRecord entries.
         It only updates LeaveBalance. Allocation is idempotent per period via AllocationLog.

RULE-20: Work entries cannot be deleted by any actor.

RULE-21: Leave records cannot be deleted by any actor.

RULE-22: Attendance records cannot be deleted by any actor.

RULE-23: Employee records cannot be deleted; only deactivated.

RULE-24: Organization records cannot be deleted in MVP.

RULE-25: Changing an employee's joining date (by Admin) affects only future allocation runs.
         Historical allocations are not retroactively adjusted.

RULE-26: Leave balance resets to 0 at the start of each leave year (January 1).
         There is no carry-forward in MVP.

RULE-27: The leave year for MVP is the calendar year (January 1 to December 31).

RULE-28: An employee cannot have two overlapping leave records in PENDING, APPROVED,
         or GRANTED status. Overlap check:
         new.start_date <= existing.end_date AND new.end_date >= existing.start_date.

RULE-29: Retroactive leave requests are limited to 7 days in the past.
         Leave requests for dates older than 7 days from today are rejected.

RULE-30: Manual attendance corrections are limited to the last 30 days.
         Both Admin and Manager are subject to this 30-day limit in MVP.
```

---

# PHASE 15 — MVP vs POST-MVP CLASSIFICATION

| Feature | MVP | Post-MVP | Reason |
|---------|-----|----------|--------|
| Organization registration | ✅ | | Core SaaS foundation |
| Organization settings (name, timezone) | ✅ | | Required at launch |
| Timezone change via self-service | | ✅ | Complex historical data implications |
| Multiple admins per org | | ✅ | One admin sufficient for MVP |
| Email/password authentication | ✅ | | Simplest auth for MVP |
| JWT + refresh token | ✅ | | Standard session management |
| Password reset via email | ✅ | | Required for usability |
| Invite email to new employees | ✅ | | Required for onboarding |
| Social login (Google, GitHub) | | ✅ | Nice-to-have |
| Enterprise SSO (SAML/OIDC) | | ✅ | Enterprise feature |
| MFA | | ✅ | Security enhancement |
| Login audit log | | ✅ | Compliance feature |
| Create employee | ✅ | | Core onboarding |
| Employee profile update (Admin) | ✅ | | Admin-only keeps it simple |
| Employee email change | | ✅ | Complex identity operation |
| Deactivate employee | ✅ | | Required for offboarding |
| Manager assignment | ✅ | | Required for scoped access |
| Bulk employee CSV import | | ✅ | Not launch-critical |
| Employee documents storage | | ✅ | Different problem space |
| Department/team hierarchy | | ✅ | Single-level manager sufficient |
| Work entry creation | ✅ | | Core value proposition |
| Work entry edit (24h window) | ✅ | | Needed for error correction |
| Work entry view (own, team) | ✅ | | Core visibility |
| Work entry locking (after 24h) | ✅ | | Data integrity |
| Work entry deletion | | ✅ | Prevented in MVP for audit |
| Project/tag categorization | | ✅ | Would create Jira |
| Start/end time tracking | | ✅ | Full timesheet feature |
| Manager editing employee entries | | ✅ | Complexity/audit concerns |
| Timesheet approval workflow | | ✅ | Out of MVP scope |
| CSV export of work entries | | ✅ | Reporting feature |
| Daily attendance check-in/out | ✅ | | Core attendance |
| Automatic absence marking | ✅ | | Required for absence visibility |
| Manual attendance correction | ✅ | | Required for error recovery |
| Attendance history view | ✅ | | Core visibility |
| Weekend as non-working days | ✅ | | Simple, universal rule |
| Holiday calendar | | ✅ | Adds complexity |
| Custom working days per org | | ✅ | Post-MVP |
| Shift management | | ✅ | Enterprise feature |
| GPS check-in | | ✅ | Hardware/location dependency |
| Biometric attendance | | ✅ | Hardware integration |
| Auto-close open attendance records | | ✅ | Requires business rule decisions |
| Leave type management | ✅ | | Required before leave can work |
| Leave policy rule configuration | ✅ | | Core leave configuration |
| Leave balance tracking | ✅ | | Required for leave to work |
| Employee leave request | ✅ | | Core leave workflow |
| Manager approve/reject leave | ✅ | | Core leave workflow |
| Manager direct leave grant | ✅ | | Explicit requirement |
| Employee cancel pending request | ✅ | | Required for basic usability |
| Cancel approved/granted leave | | ✅ | Complex reversal logic |
| Automatic leave allocation | ✅ | | Explicit requirement |
| Leave request modification | | ✅ | Cancel-and-resubmit covers MVP |
| Carry-forward of leave balance | | ✅ | Year-boundary complexity |
| Half-day leave | | ✅ | Requires UI and rule changes |
| Leave encashment | | ✅ | Requires payroll |
| Compensatory leave | | ✅ | Complex rules |
| Leave approval delegation | | ✅ | Post-MVP |
| Per-employee policy override | | ✅ | Post-MVP |
| Employee dashboard | ✅ | | Required for usability |
| Manager dashboard | ✅ | | Required for team visibility |
| Admin dashboard | ✅ | | Required for org visibility |
| Advanced analytics/charts | | ✅ | Not needed at launch |
| Exportable reports | | ✅ | Post-MVP |
| Payroll | | ✅ | Different domain |
| Recruitment/ATS | | ✅ | Different domain |
| Performance management | | ✅ | Different domain |
| Employee appraisals | | ✅ | Different domain |
| Overtime calculation | | ✅ | Labor law handling required |
| Slack/Telegram integrations | | ✅ | Nice-to-have |
| In-app notifications | | ✅ | Post-MVP |
| Email notifications on leave decision | ✅ (basic) | | Necessary for basic UX |
| Rich notification system | | ✅ | Post-MVP |
| Billing/subscription management | | ✅ | Manual billing acceptable at launch |
| Full audit log | | ✅ | Post-MVP |
| AI features | | ✅ | No MVP justification |

---

# PHASE 16 — FINAL API CATALOG

| # | Module | Method | Endpoint | Purpose | Actor | Priority | Depends On |
|---|--------|--------|----------|---------|-------|----------|------------|
| 1 | Organization | POST | /api/v1/organizations/register | Register new organization + admin | Public | P0 | None |
| 2 | Organization | GET | /api/v1/organizations/me | Get org settings | Admin | P0 | #1 |
| 3 | Organization | PATCH | /api/v1/organizations/me | Update org settings | Admin | P0 | #1 |
| 4 | Auth | POST | /api/v1/auth/login | Login | Any user | P0 | #1 |
| 5 | Auth | POST | /api/v1/auth/refresh | Refresh access token | Any user | P0 | #4 |
| 6 | Auth | POST | /api/v1/auth/logout | Logout | Any user | P0 | #4 |
| 7 | Auth | POST | /api/v1/auth/password-reset/request | Request password reset | Public | P0 | #1 |
| 8 | Auth | POST | /api/v1/auth/password-reset/confirm | Confirm password reset | Public | P0 | #7 |
| 9 | Employee | POST | /api/v1/employees | Create employee | Admin | P0 | #1, #4 |
| 10 | Employee | GET | /api/v1/employees/me | Get own profile | Any | P0 | #4 |
| 11 | Employee | GET | /api/v1/employees | List employees | Admin/Manager | P0 | #9 |
| 12 | Employee | GET | /api/v1/employees/{id} | Get employee profile | Scoped | P0 | #9 |
| 13 | Employee | PATCH | /api/v1/employees/{id} | Update employee profile | Admin | P0 | #9 |
| 14 | Employee | PATCH | /api/v1/employees/{id}/manager | Assign/change manager | Admin | P0 | #9 |
| 15 | Employee | POST | /api/v1/employees/{id}/deactivate | Deactivate employee | Admin | P0 | #9 |
| 16 | Work | POST | /api/v1/work-entries | Create work entry | Any (self) | P1 | #9 |
| 17 | Work | GET | /api/v1/work-entries/me | List own work entries | Any | P1 | #16 |
| 18 | Work | GET | /api/v1/work-entries/{id} | Get single work entry | Scoped | P1 | #16 |
| 19 | Work | PATCH | /api/v1/work-entries/{id} | Update work entry | Own (24h) / Admin | P1 | #16 |
| 20 | Work | GET | /api/v1/work-entries/team | List team work entries | Manager/Admin | P1 | #14, #16 |
| 21 | Attendance | POST | /api/v1/attendance/check-in | Check in | Any (self) | P1 | #9 |
| 22 | Attendance | POST | /api/v1/attendance/check-out | Check out | Any (self) | P1 | #21 |
| 23 | Attendance | GET | /api/v1/attendance/today | Get today's status | Any | P1 | #21 |
| 24 | Attendance | GET | /api/v1/attendance/me | Get own attendance history | Any | P1 | #21 |
| 25 | Attendance | GET | /api/v1/attendance/team | List team attendance | Manager/Admin | P1 | #14, #21 |
| 26 | Attendance | POST | /api/v1/attendance/correct | Create/correct attendance record | Admin/Manager | P1 | #9 |
| 27 | Leave | POST | /api/v1/leave/types | Create leave type | Admin | P1 | #9 |
| 28 | Leave | GET | /api/v1/leave/types | List leave types | Any | P1 | #27 |
| 29 | Leave | PUT | /api/v1/leave/policy/rules/{type_id} | Configure policy rule | Admin | P1 | #27 |
| 30 | Leave | GET | /api/v1/leave/policy | Get org leave policy | Admin | P1 | #27 |
| 31 | Leave | GET | /api/v1/leave/balance/{employee_id} | Get leave balance | Scoped | P1 | #27, #29 |
| 32 | Leave | POST | /api/v1/leave/requests | Submit leave request | Any (self) | P1 | #31 |
| 33 | Leave | GET | /api/v1/leave/requests/me | List own leave requests | Any | P1 | #32 |
| 34 | Leave | GET | /api/v1/leave/requests/team | List team leave requests | Manager/Admin | P1 | #14, #32 |
| 35 | Leave | POST | /api/v1/leave/requests/{id}/approve | Approve leave request | Manager/Admin | P1 | #32 |
| 36 | Leave | POST | /api/v1/leave/requests/{id}/reject | Reject leave request | Manager/Admin | P1 | #32 |
| 37 | Leave | POST | /api/v1/leave/requests/{id}/cancel | Cancel own pending request | Self | P1 | #32 |
| 38 | Leave | POST | /api/v1/leave/grants | Grant leave directly | Manager/Admin | P1 | #31 |
| 39 | Dashboard | GET | /api/v1/dashboard/me | Employee dashboard | Any | P2 | #16–#38 |
| 40 | Dashboard | GET | /api/v1/dashboard/team | Manager dashboard | Manager/Admin | P2 | #16–#38 |
| 41 | Dashboard | GET | /api/v1/dashboard/org | Admin dashboard | Admin | P2 | #16–#38 |

**Total MVP APIs: 41**

---

# PHASE 17 — FINAL IMPLEMENTATION ORDER

## Milestone 1 — SaaS Foundation & Authentication

**Goal:** Establish the multi-tenant backbone and authentication gateway.

**Modules/Features:** Organization registration, settings. Login, logout, token refresh, password reset.

**APIs Involved:** #1, #2, #3, #4, #5, #6, #7, #8

**Dependencies:** None.

**Completion Criteria:**
- Organization can be registered via API.
- Admin can log in, receive JWT, refresh tokens, and log out.
- Password reset flow works via email.
- All responses are scoped to the requesting organization.

**Must NOT be built yet:** Employee, work, attendance, leave features.

---

## Milestone 2 — Employee Management

**Goal:** Enable Admin to create and manage employees and control access.

**APIs Involved:** #9, #10, #11, #12, #13, #14, #15

**Dependencies:** Milestone 1 complete.

**Completion Criteria:**
- Admin can create employees with different roles.
- New employees receive invite emails.
- Manager-employee assignments work.
- Deactivation revokes access.
- Role-based scoping verified: employees cannot see other employees.

**Must NOT be built yet:** Work, attendance, leave.

---

## Milestone 3 — Work Tracker

**Goal:** Enable employees to log daily work and managers to review team activity.

**APIs Involved:** #16, #17, #18, #19, #20

**Dependencies:** Milestone 2 complete.

**Completion Criteria:**
- Employees can create multiple work entries per day.
- 24-hour edit window enforced.
- Admin can edit locked entries.
- Manager can view only their team's entries.
- Entry deletion blocked.

**Must NOT be built yet:** Attendance, leave.

---

## Milestone 4 — Attendance

**Goal:** Enable daily check-in/check-out, automatic absence marking, and team attendance visibility.

**APIs Involved:** #21, #22, #23, #24, #25, #26

**Dependencies:** Milestone 2 complete.

**Completion Criteria:**
- Employees can check in once per day.
- Check-out records duration.
- No ABSENT records created for weekends.
- Manual corrections require reason, limited to 30 days.
- Absence marking job is idempotent and back-fills up to 3 days.
- LEAVE status integration tested in Milestone 6.

---

## Milestone 5 — Leave Module

**Goal:** Enable full leave lifecycle: policy, balance, requests, approvals, grants, auto-allocation.

**APIs Involved:** #27, #28, #29, #30, #31, #32, #33, #34, #35, #36, #37, #38

**Dependencies:** Milestone 2 complete.

**Completion Criteria:**
- Admin can create leave types and configure policy rules.
- Employees can request leave with balance check.
- Manager can approve and reject leave.
- Employee can cancel pending requests.
- Manager can directly grant leave.
- Automatic allocation runs for eligible employees.
- Pro-ration on first allocation works.
- Balance cannot go below 0.
- Overlapping leave detection functional.
- Leave → Attendance cross-module write tested in Milestone 6.

---

## Milestone 6 — Cross-Module Integration

**Goal:** Wire leave approval/grant to attendance; wire deactivation to pending leave rejection; validate all 30 cross-module rules.

**Features:**
- Leave approval → Attendance LEAVE status update (APIs #35, #38 side effects)
- Leave grant → Attendance LEAVE status update (API #38 side effects)
- Employee deactivation → Pending leave auto-rejection (API #15 side effects)
- Attendance correction with LEAVE status warning behavior
- End-to-end validation of RULE-01 through RULE-30

**Dependencies:** Milestones 4 and 5 complete.

**Completion Criteria:**
- Approving a leave request creates LEAVE attendance records for all working days.
- Granting leave directly creates LEAVE attendance records.
- Deactivating an employee auto-rejects PENDING leave requests.
- All 30 cross-module rules verified end-to-end.
- Absence marking job correctly skips days with existing LEAVE records.

---

## Milestone 7 — Dashboard

**Goal:** Provide role-appropriate operational dashboards.

**APIs Involved:** #39, #40, #41

**Dependencies:** Milestones 3, 4, 5, 6 complete.

**Completion Criteria:**
- Employee dashboard shows correct attendance, balances, upcoming leave, recent work.
- Manager dashboard shows team attendance summary, pending requests.
- Admin dashboard shows org-wide stats.
- All data correctly scoped to role and organization.

---

## Milestone 8 — MVP Hardening

**Goal:** Ensure production readiness before first customer onboarding.

**Activities:**
- API error handling review: all documented error codes and messages match implementation.
- Tenant isolation audit: no API can return cross-organization data.
- Scheduled job reliability: absence marking and leave allocation jobs are idempotent with retry logic.
- Authentication security review: token expiry, revocation on deactivation, password reset single-use.
- Scope enforcement review: employee cannot access another employee's data; manager limited to their team.
- Pagination verification: all list APIs return paginated results.
- End-to-end workflow walkthrough: onboarding → work logging → attendance → leave request → approval → dashboard.

**Completion Criteria:**
- All 41 APIs functional with correct error handling.
- All 30 cross-module rules enforced.
- Scheduled jobs reliable and recoverable.
- Full end-to-end onboarding walkthrough completes without errors.

---

# PHASE 18 — MVP COMPLETENESS AUDIT

## Product

✅ **Is the MVP actually launchable?** Yes. The three core capabilities (work, attendance, leave) are fully defined.

✅ **Is the scope small enough?** Yes. No payroll, recruitment, performance management, or advanced analytics.

✅ **Are there unnecessary features?** Manual attendance correction is borderline but justified — employees WILL forget to check out, and managers need a correction path that doesn't require developer intervention.

## Architecture

✅ **Module boundaries clear?** Yes. Each module owns its entities.

✅ **Ownership clear?** Yes. See Domain Concepts (Phase 7) and Cross-Module Rules (Phase 14).

✅ **Dependencies clear?** Yes. Global Dependency Graph (Phase 6) is explicit.

✅ **Circular dependencies?** None. Leave writes to Attendance; Attendance does not write back to Leave. The dependency graph is acyclic.

## Permissions

✅ **Employees accessing another employee's data?** Blocked. All queries filter by employee scope derived from JWT.

✅ **Managers accessing outside their scope?** Blocked. All manager queries filter by ManagerAssignment.

✅ **Admins cross-organization?** Blocked. RULE-12 enforces org-level filtering on every query.

## Work

✅ **Work-entry rules unambiguous?** Yes. Multiple per day, 24h edit window, no deletion, title required.

## Attendance

✅ **Check-in/check-out rules unambiguous?** Yes. Once per day, no auto-checkout, manual correction with reason.

✅ **Absence handling defined?** Yes. Scheduled job, weekends excluded, idempotent with 3-day back-fill.

## Leave

✅ **Manager-granted leave fully defined?** Yes. See Feature: Manager Direct Leave Grant.

✅ **Automatic leave allocation fully defined?** Yes. See Feature: Automatic Leave Allocation and Phase 10.

✅ **Balances deterministic?** Yes. Balance = Total Allocated - Total Used. Updated atomically.

✅ **Leave → Attendance behavior deterministic?** Yes. See RULE-06 and Phase 10.12.

## APIs

✅ **Every MVP feature has an API?** Yes. 41 APIs cover all documented features.

✅ **Every API has an actor and permission?** Yes. All contracts include Actor and Required Permission.

✅ **Error cases documented?** Yes. All major error scenarios documented per API.

✅ **Cross-module side effects documented?** Yes. Every relevant API has a Side Effects section.

✅ **APIs ordered by dependency?** Yes. API Catalog (#1–#41) is dependency-ordered.

## SaaS

✅ **Tenant isolation at product level?** Yes. RULE-12.

✅ **Users belong to correct org?** Yes. JWT contains organization_id; all queries filter by it.

✅ **Org-level settings defined?** Yes. Organization settings include name and timezone.

## Scope

✅ **Has MVP accidentally become an HRMS?** No. Only work tracking, attendance, and leave are included.

---

# PHASE 19 — CONTRADICTION & GAP AUDIT

**Issue 1 — Gap: Leave balance initialization**

*Problem:* When is a LeaveBalance record first created for an employee?

*Resolution:* A LeaveBalance record is created on first allocation. Before any allocation, balance is effectively 0. When listing balances, the system returns 0 for leave types where no record exists. Documented in Phase 7.8 and the Get Leave Balance API.

---

**Issue 2 — Gap: Leave request when no balance record exists**

*Problem:* Employee tries to request leave but no LeaveBalance record exists.

*Resolution:* System treats missing balance record as balance = 0. The submit leave request API returns 422 with message: "No leave balance exists for this leave type. Contact your admin." Documented in API #32.

---

**Issue 3 — Contradiction: Who approves leave for employees without a manager?**

*Problem:* An employee may have no manager assigned. Who approves their leave?

*Resolution:* Admin can approve leave for any employee, including those without a manager. If an employee has no manager, their PENDING requests remain until Admin acts on them. Documented in Employee Management business rules and API #35.

---

**Issue 4 — Gap: Creating an attendance record when none exists**

*Problem:* The original correction API required an existing record ID. What if no record exists?

*Resolution:* The correction API (API #26) was redesigned to accept employee_id + date + status + reason as body parameters (upsert behavior). It creates the record if none exists, or updates it if one exists. Endpoint changed from `PATCH /api/v1/attendance/{id}/correct` to `POST /api/v1/attendance/correct`.

---

**Issue 5 — Gap: Email notification on leave decisions**

*Problem:* Leave approval/rejection/grant APIs did not mention employee notification.

*Resolution:* Side effects for APIs #35, #36, and #38 explicitly state: "Email notification sent to employee." Email delivery is best-effort; delivery failure does not fail the API request.

---

**Issue 6 — Contradiction: Automatic allocation idempotency**

*Problem:* How does the system prevent double-allocation if the job runs twice for the same period?

*Resolution:* An AllocationLog entity (internal, not API-exposed) records each completed allocation run by (organization_id, leave_type_id, period_start, period_end). The job checks this log before allocating. Documented in Phase 10.4 and RULE-19.

---

**Issue 7 — Gap: Leave balance reset sequence on January 1**

*Problem:* Balance resets to 0 and the annual allocation job also runs on January 1. Which runs first?

*Resolution:* Sequence on January 1:
1. Previous year LeaveBalance records are frozen.
2. New year LeaveBalance records initialized to 0.
3. Annual allocation job runs and adds the first credit.
Net employee balance on January 1 = allocation amount (subject to tenure and pro-ration).
Documented in Phase 10.10.

---

**Issue 8 — Gap: Dashboard data freshness**

*Problem:* Are dashboard responses cached or real-time?

*Resolution:* All dashboard data is computed in real time for MVP. No caching. "Not yet checked in" count is computed at query time as: total_active_employees - (present + absent + on_leave counts). Documented in Phase 13.

---

**Post-Audit API Count Confirmation:** 41 APIs. No duplicates. No missing APIs for documented features. Catalog is final.

---

# PHASE 20 — MVP PRODUCT FREEZE

## Included Modules

1. SaaS / Organization Foundation
2. Authentication & Access
3. Employee Management
4. Work Tracker
5. Attendance
6. Leave
7. Dashboard

---

## Included Features

**Organization:** Registration, settings view, settings update.

**Authentication:** Login, logout, token refresh, password reset (request + confirm).

**Employees:** Create, get own profile, list (scoped), get by ID, update (admin), assign manager, deactivate.

**Work Tracker:** Create entry, list own, get by ID, update own (24h window), admin edit any, list team.

**Attendance:** Check-in, check-out, today's status, history view, team view, manual correction (upsert), automatic absence marking job.

**Leave:** Leave type creation and listing, policy rule configuration, policy view, leave balance view, leave request submission, own request listing, team request listing, approval, rejection, cancellation, direct grant, automatic allocation job.

**Dashboard:** Employee, Manager, Admin dashboards.

**Cross-Module:** Leave approval/grant → attendance update. Employee deactivation → token revocation + pending leave rejection. Email notifications on leave decisions.

---

## Excluded Features

- Payroll, recruitment, performance management, appraisals
- Holiday calendar, shift management
- GPS / biometric / face-recognition attendance
- Social login, SSO, MFA
- Multiple admins per organization
- Employee email change or self-service profile edits
- Bulk employee import
- Project/tag categorization in work tracker
- Start/end time tracking in work entries
- Half-day leave
- Leave cancellation post-approval
- Carry-forward of leave balance
- Leave encashment, compensatory leave
- Advanced analytics, charts, exportable reports
- In-app notifications, Slack/Telegram integrations
- Billing/subscription management
- Full audit log

---

## Roles

| Role | Count per Org (MVP) | Access Scope |
|------|---------------------|--------------|
| Admin | 1 | Full organizational control |
| Manager | Unlimited | Direct reports only |
| Employee | Unlimited | Own records only |

---

## Core Entities

| Entity | Owner Module |
|--------|-------------|
| Organization | Organization |
| User | Authentication |
| Employee | Employee Management |
| WorkEntry | Work Tracker |
| AttendanceRecord | Attendance |
| LeaveType | Leave |
| LeavePolicyRule | Leave |
| LeaveBalance | Leave |
| LeaveRecord | Leave |

---

## Dependency Graph

```
Organization
     │
     ├── Authentication → User
     │                      │
     │                      ▼
     └──────────────────► Employee
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
         WorkTracker     Attendance ◄──── Leave
                          (LEAVE            (writes
                           status)          status)
              │               │               │
              └───────────────┴───────────────┘
                                  │
                                  ▼
                              Dashboard
                           (reads from all)
```

---

## Core Business Rules (Summary)

1. All data is organization-scoped. Cross-org access is prohibited (RULE-12).
2. Employees see only their own records; managers see only direct reports (RULE-10, RULE-11).
3. Deactivated employees retain historical records but cannot create new ones (RULE-07, RULE-09).
4. Leave balance cannot go below 0 (RULE-14).
5. Leave approval/grant writes LEAVE status to attendance for all working days (RULE-06).
6. Weekends (Sat/Sun) are non-working days: no absence marks, excluded from leave day count (RULE-15, RULE-17).
7. Leave requests can only be cancelled while PENDING (RULE-16).
8. Work entries are locked after 24 hours for employees; Admin can still edit (Domain Concept 7.4).
9. Work entries and leave records are never deleted (RULE-20, RULE-21).
10. Automatic leave allocation is idempotent per period (RULE-19).
11. Leave year is January 1 to December 31. No carry-forward (RULE-26, RULE-27).
12. Retroactive leave requests limited to 7 days; manual attendance correction limited to 30 days (RULE-29, RULE-30).

---

## API Count

**Total MVP APIs: 41**

| Module | API Count |
|--------|-----------|
| Organization | 3 |
| Authentication | 5 |
| Employee | 7 |
| Work Tracker | 5 |
| Attendance | 6 |
| Leave | 12 |
| Dashboard | 3 |
| **Total** | **41** |

---

## API Build Order

```
Phase 1 — Foundation (APIs 1–8)
  1.  POST  /api/v1/organizations/register
  2.  GET   /api/v1/organizations/me
  3.  PATCH /api/v1/organizations/me
  4.  POST  /api/v1/auth/login
  5.  POST  /api/v1/auth/refresh
  6.  POST  /api/v1/auth/logout
  7.  POST  /api/v1/auth/password-reset/request
  8.  POST  /api/v1/auth/password-reset/confirm

Phase 2 — Employees (APIs 9–15)
  9.  POST  /api/v1/employees
  10. GET   /api/v1/employees/me
  11. GET   /api/v1/employees
  12. GET   /api/v1/employees/{id}
  13. PATCH /api/v1/employees/{id}
  14. PATCH /api/v1/employees/{id}/manager
  15. POST  /api/v1/employees/{id}/deactivate

Phase 3 — Work Tracker (APIs 16–20)
  16. POST  /api/v1/work-entries
  17. GET   /api/v1/work-entries/me
  18. GET   /api/v1/work-entries/{id}
  19. PATCH /api/v1/work-entries/{id}
  20. GET   /api/v1/work-entries/team

Phase 4 — Attendance (APIs 21–26)
  21. POST  /api/v1/attendance/check-in
  22. POST  /api/v1/attendance/check-out
  23. GET   /api/v1/attendance/today
  24. GET   /api/v1/attendance/me
  25. GET   /api/v1/attendance/team
  26. POST  /api/v1/attendance/correct

Phase 5 — Leave (APIs 27–38)
  27. POST  /api/v1/leave/types
  28. GET   /api/v1/leave/types
  29. PUT   /api/v1/leave/policy/rules/{type_id}
  30. GET   /api/v1/leave/policy
  31. GET   /api/v1/leave/balance/{employee_id}
  32. POST  /api/v1/leave/requests
  33. GET   /api/v1/leave/requests/me
  34. GET   /api/v1/leave/requests/team
  35. POST  /api/v1/leave/requests/{id}/approve
  36. POST  /api/v1/leave/requests/{id}/reject
  37. POST  /api/v1/leave/requests/{id}/cancel
  38. POST  /api/v1/leave/grants

Phase 6 — Dashboard (APIs 39–41)
  39. GET   /api/v1/dashboard/me
  40. GET   /api/v1/dashboard/team
  41. GET   /api/v1/dashboard/org
```

---

## Major Cross-Module Workflows

| # | Workflow | Modules Involved |
|---|----------|-----------------|
| 1 | Employee Onboarding | Org → Auth → Employee → Leave (config) |
| 2 | Daily Work Logging | Work Tracker → Dashboard |
| 3 | Daily Attendance | Attendance → Dashboard |
| 4 | Leave Request & Approval | Leave → Attendance (status update) → Dashboard |
| 5 | Manager Direct Leave Grant | Leave → Attendance (status update) |
| 6 | Automatic Leave Allocation | Leave (scheduled job) → Leave Balance |

---

## Known MVP Limitations

1. **No holiday calendar**: Public holidays cause incorrect absence records unless manually corrected.
2. **No carry-forward**: Unused leave forfeited at year-end.
3. **One admin per org**: Cannot have multiple admins.
4. **No leave reversal**: Approved/granted leave cannot be undone in MVP.
5. **No half-day leave**: Leaves counted in full days only.
6. **Timezone is immutable**: Cannot change after organization setup.
7. **7-day retroactive limit on leave requests**: Cannot request leave for dates older than 7 days.
8. **No in-app notifications**: Employees check the system for leave decisions.
9. **No employee self-service profile edits**: Admin handles all profile changes.
10. **Open attendance records**: If an employee forgets to check out, the record stays open. Only Admin/Manager can correct.

---

## Explicit Post-MVP Backlog

1. Holiday calendar and custom non-working day configuration
2. Multiple admins per organization
3. Carry-forward of unused leave balance
4. Leave reversal / approved leave cancellation
5. Half-day leave
6. Leave request modification
7. Employee email change
8. Employee self-service profile editing
9. Bulk employee import (CSV)
10. Manager editing of employee work entries
11. Time tracking with start/end timestamps
12. Project/tag categorization for work entries
13. CSV export of work, attendance, and leave data
14. Shift management and custom working week
15. GPS check-in / mobile attendance
16. Social login, SSO, MFA
17. Per-employee leave policy overrides
18. Compensatory leave type
19. Overtime tracking
20. Rich notification system (in-app, Slack, email digests)
21. Advanced analytics and dashboards
22. Billing and subscription management
23. Full audit log with event trail
24. Department/team hierarchy beyond single-level manager
25. Leave approval delegation when manager is absent
26. Resend employee invite email
27. Organization suspension / account management
28. Multiple organizations per admin user

---

*End of MVP Product Specification & API Blueprint*

---

**Document Metadata**

| Field | Value |
|-------|-------|
| Status | Frozen — MVP Definition |
| Total APIs | 41 |
| Total Business Rules | 30 |
| Total Domain Entities | 9 |
| Total Modules | 7 |
| Total Milestones | 8 |
| Post-MVP Backlog Items | 28 |
