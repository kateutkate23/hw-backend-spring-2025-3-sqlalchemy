import hashlib
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        admin_config = app.config.admin
        email = admin_config.email
        password = admin_config.password

        if not await self.get_by_email(email):
            await self.create_admin(email, password)

    async def get_by_email(self, email: str) -> AdminModel | None:
        async with self.app.database.session() as session:
            return await session.scalar(select(AdminModel).where(AdminModel.email == email))

    async def create_admin(self, email: str, password: str) -> AdminModel:
        admin = await self.get_by_email(email)
        if admin:
            return admin

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        admin = AdminModel(email=email, password=hashed_password)

        async with self.app.database.session() as session:
            session.add(admin)
            await session.commit()

            return admin
