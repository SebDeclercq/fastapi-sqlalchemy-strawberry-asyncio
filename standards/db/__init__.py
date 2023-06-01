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
from .models import File, Standard
from .._private.pydantic import Config as _PydanticConfig
from .._private.types import AsyncSessionMaker


__all__: list[str] = ["MyDb"]


class MyDb(pydantic.BaseModel):
    db_url: str
    engine: AsyncEngine | None = None
    sessionmaker: AsyncSessionMaker | None = None
    expire_on_commit: bool = False

    Config = _PydanticConfig

    @classmethod
    async def start(cls, db_url: str) -> MyDb:
        self: MyDb = cls(db_url=db_url)
        await self.connect()
        return self

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

    async def get_standards(self) -> list[Standard]:
        session: AsyncSession = await self.get_session()
        result: Result[tuple[Standard, ...]] = await session.execute(
            select(Standard).options(selectinload(Standard.files))
        )
        return [std for (std,) in result.all()]

    async def get_files(self) -> list[File]:
        session: AsyncSession = await self.get_session()
        result: Result[tuple[File, ...]] = await session.execute(
            select(File).options(selectinload(File.standard))
        )
        return [file for (file,) in result.all()]

    async def get_standard(self, numdos: str) -> Standard | None:
        session: AsyncSession = await self.get_session()
        result: Result[tuple[Standard, ...]] = await session.execute(
            select(Standard)
            .options(selectinload(Standard.files))
            .where(Standard.numdos == numdos)
        )
        try:
            return result.scalars().first()
        except AttributeError:
            return None

    async def get_file(self, numdos: str = "", numdosvl: str = "") -> File | None:
        session: AsyncSession = await self.get_session()
        result: Result[tuple[File, ...]] = await session.execute(
            select(File)
            .options(selectinload(File.standard))
            .where(File.numdos == numdos)
            .where(File.numdosvl == numdosvl)
        )
        try:
            return result.scalars().first()
        except AttributeError:
            return None
