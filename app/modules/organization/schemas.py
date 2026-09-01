"""
Organization Pydantic schemas.

Implementation: Phase 2

Schemas to implement:
  OrganizationRegisterRequest  — POST /api/v1/organizations/register
  OrganizationResponse         — response for all org endpoints
  OrganizationUpdateRequest    — PATCH /api/v1/organizations/me
"""

# TODO (Phase 2): Implement schemas.
#
# Key fields from blueprint §12 and §9.2:
#
# OrganizationRegisterRequest:
#   organization_name: str (2-100 chars, globally unique)
#   admin_full_name:   str
#   admin_email:       EmailStr
#   password:          str (min 8 chars)
#
# OrganizationResponse:
#   id, name, slug, timezone, created_at, employee_count
#
# OrganizationUpdateRequest:
#   organization_name: str | None  (optional, 2-100 chars)
