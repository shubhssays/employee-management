from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.reset_token.models import ResetToken
from app.modules.reset_token.schemas import EmployeeToken


class ResetTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by(self, id_or_token: int | str | None, emp_token: EmployeeToken | None) -> ResetToken | None:
        if id_or_token is None and emp_token is None:
            raise ValueError("Provide either id_or_token or emp_token, anyone of them")

        if id_or_token is not None and emp_token is not None:
            raise ValueError("Provide either id_or_token or emp_token, not both")

        # is_active filter is directly applied because even if we don't add
        # this filter here we will need to check it on service layer and
        # return invalid token error, which is the same error we will
        # send to end user in case the token is wrong

        conditions = [ResetToken.id == id_or_token, ResetToken.is_active == True]

        if id_or_token is not None and type(id_or_token) is str:
            conditions = [ResetToken.token == id_or_token, ResetToken.is_active == True]

        if emp_token is not None:
            conditions = [
                ResetToken.emp_id == emp_token["emp_id"],
                ResetToken.token == emp_token["token"],
                ResetToken.is_active == True,
            ]

        result = await self.db.execute(select(ResetToken).where(*conditions))
        return result.scalar_one_or_none()

    async def get_unused(self, emp_id: int) -> Any | None:
        conditions = [
            ResetToken.emp_id == emp_id,
            ResetToken.is_active == True,
            ResetToken.used_at.is_(None),
            ResetToken.expiry_at > datetime.now(timezone.utc),
        ]

        result = await self.db.execute(select(ResetToken).where(*conditions))
        return result.scalar_one_or_none()

    async def create(self, reset_token: ResetToken) -> ResetToken:
        self.db.add(reset_token)
        await self.db.flush()
        await self.db.refresh(reset_token)
        return reset_token

    async def update(self, reset_token: ResetToken, data: dict) -> ResetToken:
        for field, value in data.items():
            setattr(reset_token, field, value)
        await self.db.flush()
        return reset_token
