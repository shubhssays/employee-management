"""
Organization ORM model.

Table: organizations
Owner: Organization module
Tenant role: This IS the tenant — it has no organization_id column.

Implementation: Phase 2
"""

# TODO (Phase 2): Implement Organization ORM model.
#
# Fields to implement per technical blueprint §9.2:
#   id           UUID PK (inherited from Base)
#   name         TEXT, globally unique (case-insensitive)
#   slug         TEXT, unique, URL-friendly identifier
#   timezone     TEXT, IANA timezone (e.g., "Asia/Kolkata"), required, immutable via API
#   is_active    BOOL, default True
#   created_at   TIMESTAMPTZ (inherited from Base)
#   updated_at   TIMESTAMPTZ (inherited from Base)
#
# Constraints:
#   - name must be globally unique (enforce with LOWER(name) index)
#   - timezone is required and may not be changed after creation
#
# Relationships:
#   - Parent of all other entities (all tenant-scoped tables have FK → organizations.id)
#
# Example skeleton:
#
# from sqlalchemy import Boolean, String, UniqueConstraint
# from sqlalchemy.orm import Mapped, mapped_column
# from app.db.base_model import Base
#
# class Organization(Base):
#     __tablename__ = "organizations"
#     __table_args__ = (UniqueConstraint("name", name="uq_organizations_name"),)
#
#     name:     Mapped[str]  = mapped_column(String, nullable=False)
#     slug:     Mapped[str]  = mapped_column(String, nullable=False, unique=True)
#     timezone: Mapped[str]  = mapped_column(String, nullable=False, default="UTC")
#     is_active:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
