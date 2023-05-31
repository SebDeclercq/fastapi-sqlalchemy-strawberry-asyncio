from __future__ import annotations
import strawberry


@strawberry.type
class StandardType:
    numdos: str
    files: list[FileType]


@strawberry.type
class FileType:
    id: int
    name: str
    numdosvl: str
    numdos: str
    standard: StandardType
