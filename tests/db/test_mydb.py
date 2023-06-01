"""
MAINLY DEVELOPED BY CHATGPT
"""

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from standards._private.enum import FileFormat, FileLanguage
from standards.db.models import Base, Standard, File
from standards.db import MyDb
from standards._private.types import AsyncSessionMaker


@pytest_asyncio.fixture
def database_url() -> str:
    return "sqlite+aiosqlite://"


@pytest_asyncio.fixture
async def engine(database_url: str) -> AsyncEngine:
    engine: AsyncEngine = create_async_engine(database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
def session(engine: AsyncEngine) -> AsyncSessionMaker:
    session: AsyncSessionMaker = async_sessionmaker(bind=engine, class_=AsyncSession)
    yield session


@pytest_asyncio.fixture
async def setup(session: AsyncSessionMaker) -> None:
    async with session() as s:
        async with s.begin():
            await s.execute(text("DELETE FROM files;"))
            await s.execute(text("DELETE FROM standards;"))
            await s.flush()


@pytest.mark.asyncio
async def test_my_db_start(database_url: str, setup: None) -> None:
    db: MyDb = await MyDb.start(database_url)
    assert db.engine is not None
    assert db.sessionmaker is not None


@pytest.mark.asyncio
async def test_my_db_connect(database_url: str, setup: None) -> None:
    db: MyDb = MyDb(db_url=database_url)
    await db.connect()
    assert db.engine is not None
    assert db.sessionmaker is not None


@pytest.mark.asyncio
async def test_my_db_get_session(database_url: str, setup: None) -> None:
    db: MyDb = MyDb(db_url=database_url)
    session = await db.get_session()
    assert session is not None


@pytest.mark.asyncio
async def test_my_db_close(database_url: str, setup: None) -> None:
    db: MyDb = MyDb(db_url=database_url)
    await db.close()
    assert db.engine is None
    assert db.sessionmaker is None


@pytest_asyncio.fixture
async def db(database_url: str) -> MyDb:
    db: MyDb = await MyDb.start(database_url)
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return db


@pytest.mark.asyncio
async def test_my_db_get_standards(db: MyDb) -> None:
    standards: list[Standard] = await db.get_standards()
    assert isinstance(standards, list)
    assert all(isinstance(standard, Standard) for standard in standards)


@pytest.mark.asyncio
async def test_my_db_get_files(db: MyDb) -> None:
    files: list[File] = await db.get_files()
    assert isinstance(files, list)
    assert all(isinstance(file, File) for file in files)


@pytest.mark.asyncio
async def test_my_db_get_standard(db: MyDb) -> None:
    standard: Standard = Standard(numdos="AB123456")
    session: AsyncSession = await db.get_session()
    session.add(standard)
    await session.commit()

    result = await db.get_standard("AB123456")
    assert isinstance(result, Standard)
    assert result.numdos == "AB123456"

    result = await db.get_standard("NonExistent")
    assert result is None


@pytest.mark.asyncio
async def test_my_db_get_file(db: MyDb, setup: None) -> None:
    file = File(
        numdos="AB123456",
        numdosvl="AB123456",
        name="test.pdf",
        format=FileFormat.PDF,
        language=FileLanguage.FR,
    )
    session: AsyncSession = await db.get_session()
    session.add(file)
    await session.commit()

    result = await db.get_file(numdos="AB123456", numdosvl="AB123456")
    assert isinstance(result, File)
    assert result.numdos == "AB123456"
    assert result.numdosvl == "AB123456"

    result = await db.get_file(numdos="NonExistent")
    assert result is None
