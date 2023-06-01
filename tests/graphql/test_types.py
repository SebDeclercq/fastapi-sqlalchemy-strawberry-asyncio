"""
MAINLY DEVELOPED BY CHATGPT
"""

import pytest
from standards._private.enum import FileFormat, FileLanguage
from standards.graphql.types import FileType, StandardType


@pytest.fixture
def file_type() -> FileType:
    return FileType(
        id=1,
        name="Example File",
        numdosvl="12345",
        numdos="ABCDE",
        standard=StandardType(numdos="ABCDE", files=[]),
        format=FileFormat.PDF,
        language=FileLanguage.EN,
    )


def test_file_type(file_type: FileType):
    assert file_type.id == 1
    assert file_type.name == "Example File"
    assert file_type.numdosvl == "12345"
    assert file_type.numdos == "ABCDE"
    assert isinstance(file_type.standard, StandardType)
    assert file_type.format == FileFormat.PDF
    assert file_type.language == FileLanguage.EN


@pytest.fixture
def standard_type() -> StandardType:
    return StandardType(
        numdos="ABCDE",
        files=[
            FileType(
                id=1,
                name="Example File 1",
                numdosvl="12345",
                numdos="ABCDE",
                standard=StandardType(numdos="ABCDE", files=[]),
                format=FileFormat.PDF,
                language=FileLanguage.EN,
            ),
            FileType(
                id=2,
                name="Example File 2",
                numdosvl="67890",
                numdos="ABCDE",
                standard=StandardType(numdos="ABCDE", files=[]),
                format=FileFormat.XML,
                language=FileLanguage.FR,
            ),
        ],
    )


def test_standard_type(standard_type: StandardType):
    assert standard_type.numdos == "ABCDE"
    assert len(standard_type.files) == 2
    assert isinstance(standard_type.files[0], FileType)
    assert isinstance(standard_type.files[1], FileType)


def test_standard_type_empty_files():
    standard_type = StandardType(numdos="ABCDE", files=None)
    assert standard_type.numdos == "ABCDE"
    assert standard_type.files is None


@pytest.mark.asyncio
async def test_file_type_async():
    file_type = FileType(
        id=1,
        name="Example File",
        numdosvl="12345",
        numdos="ABCDE",
        standard=StandardType(numdos="ABCDE", files=[]),
        format=FileFormat.PDF,
        language=FileLanguage.EN,
    )
    assert file_type.id == 1
    assert file_type.name == "Example File"
    assert file_type.numdosvl == "12345"
    assert file_type.numdos == "ABCDE"
    assert isinstance(file_type.standard, StandardType)
    assert file_type.format == FileFormat.PDF
    assert file_type.language == FileLanguage.EN
