from typing import TYPE_CHECKING, Any

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker, create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.store.database import BaseModel

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application") -> None:
        self.app = app

        self.engine: AsyncEngine | None = None
        self._db: type[DeclarativeBase] = BaseModel
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def connect(self, *args: Any, **kwargs: Any) -> None:
        # raise NotImplementedError
        db_config = self.app.config.database

        self.engine = create_async_engine(
            URL.create(
                drivername="postgresql+asyncpg",
                host=db_config.host,
                port=db_config.port,
                database=db_config.database,
                username=db_config.user,
                password=db_config.password,
            ),
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        # raise NotImplementedError
        await self.engine.dispose()
