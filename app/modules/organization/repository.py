"""
Organization repository.

Owns all database queries for the Organization entity.
Tenant isolation note: Organization is the tenant root — it has no
organization_id filter. All other repositories MUST include one.

Implementation: Phase 2
"""

# TODO (Phase 2): Implement OrganizationRepository.
#
# Methods to implement:
#   get_by_id(id: UUID) → Organization | None
#   get_by_name(name: str) → Organization | None   (case-insensitive)
#   get_by_slug(slug: str) → Organization | None
#   create(data: dict) → Organization
#   update(org: Organization, data: dict) → Organization
#
# All methods receive an AsyncSession as a constructor argument.
