"""
Organization service — business logic layer.

Responsibilities:
  - Validate organization name uniqueness globally
  - Create organization atomically with Admin user + Employee record
  - Enforce timezone-immutability business rule
  - Return organization data to router

Cross-module coordination:
  - On org registration: calls AuthService.create_admin_user()
    (Auth module; implemented in Phase 3)

Implementation: Phase 2
"""

# TODO (Phase 2): Implement OrganizationService.
#
# Public methods:
#   register(request: OrganizationRegisterRequest) → OrganizationWithTokenResponse
#   get_settings(org_id: UUID) → OrganizationResponse
#   update_settings(org_id: UUID, request: OrganizationUpdateRequest) → OrganizationResponse
#
# Business rules:
#   - Organization name must be globally unique (case-insensitive)
#   - Timezone is immutable after creation — raise TimezoneChangeNotSupportedError
#   - Registration creates Organization + User(ADMIN) + Employee atomically
