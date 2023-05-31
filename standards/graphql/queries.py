import strawberry
from strawberry.types import ExecutionContext
from .types import FileType, StandardType
from ..db import MyDb
from ..db.models import File, Standard


@strawberry.type
class Query:
    @strawberry.field
    async def standard(
        self, info: ExecutionContext, numdos: str = ""
    ) -> StandardType | None:
        db: MyDb = info.context["db"]
        standard: Standard | None = await db.get_standard(numdos)
        return StandardType(**standard) if standard else None

    @strawberry.field
    async def file(
        self, info: ExecutionContext, numdos: str = "", numdosvl: str = ""
    ) -> FileType | None:
        db: MyDb = info.context["db"]
        file: File | None = await db.get_file(numdos, numdosvl)
        return FileType(**file) if file else None

    @strawberry.field
    async def standards(self, info: ExecutionContext) -> list[StandardType]:
        db: MyDb = info.context["db"]
        standards: list[Standard] = await db.get_standards()
        return [StandardType(**std) for std in standards]

    @strawberry.field
    async def files(self, info: ExecutionContext) -> list[FileType]:
        db: MyDb = info.context["db"]
        files: list[File] = await db.get_files()
        return [FileType(**file) for file in files]
