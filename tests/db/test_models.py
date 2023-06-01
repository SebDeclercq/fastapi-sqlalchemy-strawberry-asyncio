"""
MAINLY DEVELOPED BY CHATGPT
"""

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)
from standards.db.models import Base, Standard, File
from standards._private.enum import FileFormat, FileLanguage
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
async def test_file_format_enum(setup: None) -> None:
    assert isinstance(FileFormat.PDF, FileFormat)


@pytest.mark.asyncio
async def test_file_language_enum(setup: None) -> None:
    assert isinstance(FileLanguage.EN, FileLanguage)


@pytest.mark.asyncio
async def test_standard(session: AsyncSessionMaker, setup: None) -> None:
    async with session() as s:
        standard = Standard(
            numdos="AB123456",
            files=[
                File(
                    name="file.txt",
                    numdosvl="AB123456",
                    numdos="AB123456",
                    format=FileFormat.PDF,
                    language=FileLanguage.EN,
                )
            ],
        )
        s.add(standard)
        await s.flush()

        assert standard.numdos == "AB123456"
        assert "files" in dict(**standard)
        assert isinstance(dict(**standard).get("files", [])[0], File)


@pytest.mark.asyncio
async def test_file(session: AsyncSessionMaker, setup: None) -> None:
    async with session() as s:
        standard = Standard(numdos="AB123456")
        file = File(
            name="file.txt",
            numdosvl="AB123456",
            numdos="AB123456",
            standard=standard,
            format=FileFormat.PDF,
            language=FileLanguage.EN,
        )
        s.add(file)
        await s.flush()

        assert file.name == "file.txt"
        assert file.numdosvl == "AB123456"
        assert file.numdos == "AB123456"
        assert file.standard == standard
        assert file.format == FileFormat.PDF
        assert file.language == FileLanguage.EN

        assert "numdosvl" in dict(**file)
