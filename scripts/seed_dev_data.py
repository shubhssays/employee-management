"""
Development data seeding script.

Usage:
    uv run python scripts/seed_dev_data.py

Seeds the development database with:
  - One test organization
  - One Admin user
  - One Manager user
  - Two Employee users

ONLY run against the development database.
NEVER run against production.
"""

import asyncio
import sys

# Guard against accidental production use
if "--production" not in sys.argv:
    print("Seeding development data...")
    print("WARNING: Only use this against the development database.")
    print("To confirm, pass --development flag explicitly.\n")

    if "--development" not in sys.argv:
        print("Aborting. Pass --development to seed the dev database.")
        sys.exit(1)

# TODO (Phase 4): Implement seeding after organization, auth, and employee
# modules are implemented.
#
# Seed data structure:
#   Organization: "Acme Corp", timezone="Asia/Kolkata"
#   Admin: admin@acme.com / TestPassword123!
#   Manager: manager@acme.com / TestPassword123! (reports to Admin)
#   Employee 1: alice@acme.com / TestPassword123! (reports to Manager)
#   Employee 2: bob@acme.com / TestPassword123! (reports to Manager)

print("Seed script placeholder — implement after Phase 4.")
