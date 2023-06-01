"""
MAINLY DEVELOPED BY CHATGPT
"""

import pytest
import pytest_asyncio
from strawberry.types import ExecutionContext
from standards.graphql import Query, get_schema
from standards.graphql.types import FileType, StandardType
from standards.db import MyDb
from standards.db.models import File, Standard


class MockDb(MyDb):
    async def get_standard(self, numdos: str) -> Standard | None:
        return Standard(numdos="numdos")

    async def get_file(self, numdos: str, numdosvl: str) -> File | None:
        return File(numdos="numdos", numdosvl="numdosvl")

    async def get_standards(self) -> list[Standard]:
        return [Standard(numdos="A"), Standard(numdos="B")]

    async def get_files(self) -> list[File]:
        return [File(numdos="A", numdosvl="1"), File(numdos="B", numdosvl="2")]


@pytest_asyncio.fixture
async def mock_db() -> MockDb:
    return MockDb(db_url="sqlite+aiosqlite://")


@pytest.mark.asyncio
async def test_query_standard(mock_db):
    query = Query()
    context = {"db": mock_db}
    result = await query.standard(
        ExecutionContext(r"{ standard(numdos: 'A') { numdos } }", get_schema(), context)
    )
    assert isinstance(result, StandardType)
    assert result.numdos == "numdos"


@pytest.mark.asyncio
async def test_query_file(mock_db):
    query = Query()
    context = {"db": mock_db}
    result = await query.file(
        ExecutionContext(r"{ file(numdos: 'A') { numdos } }", get_schema(), context)
    )
    assert isinstance(result, FileType)
    assert result.numdos == "numdos"
    assert result.numdosvl == "numdosvl"


@pytest.mark.asyncio
async def test_query_standards(mock_db):
    query = Query()
    context = {"db": mock_db}
    result = await query.standards(
        ExecutionContext(r"{ standards }", get_schema(), context)
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(std, StandardType) for std in result)


@pytest.mark.asyncio
async def test_query_files(mock_db):
    query = Query()
    context = {"db": mock_db}
    result = await query.files(ExecutionContext(r"{ files }", get_schema(), context))
    assert isinstance(result, list)
