from typing import TypeAlias
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


__all__: list[str] = ["AsyncSessionMaker"]


AsyncSessionMaker: TypeAlias = async_sessionmaker[AsyncSession]
