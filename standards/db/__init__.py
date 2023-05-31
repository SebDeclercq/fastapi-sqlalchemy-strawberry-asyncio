from __future__ import annotations
from typing import Self
import pydantic
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import selectinload
from .models import Standard
from .._private.pydantic import Config as _PydanticConfig
from .._private.types import AsyncSessionMaker


__all__: list[str] = ["MyDb", "start_db"]


async def start_db(db_url: str, in_memory_db: bool) -> MyDb:
    db: MyDb = MyDb(db_url=db_url)
    await db.connect()
    return db


class MyDb(pydantic.BaseModel):
    db_url: str
    engine: AsyncEngine | None = None
    sessionmaker: AsyncSessionMaker | None = None
    expire_on_commit: bool = False

    Config = _PydanticConfig

    async def connect(self) -> Self:
        self.engine: AsyncEngine = create_async_engine(self.db_url)
        self.sessionmaker: AsyncSessionMaker = async_sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        return self

    async def get_session(self) -> AsyncSession:
        if not self.sessionmaker:
            await self.connect()
        assert self.sessionmaker is not None
        return self.sessionmaker()

    async def close(self) -> None:
        ...

    async def get_standard(self, numdos: str) -> Standard:
        session: AsyncSession = await self.get_session()
        standard: Result = await session.execute(
            select(Standard)
            .options(selectinload(Standard.files))
            .where(Standard.numdos == numdos)
        )
        try:
            return standard.scalars().first()
        except AttributeError:
            return None
