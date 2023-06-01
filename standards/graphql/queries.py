import strawberry
from strawberry.types import ExecutionContext
from .types import FileType, StandardType
from ..db import MyDb
from ..db.models import File, Standard


@strawberry.type
class Query:
    """
    Represents the root query for the GraphQL schema.

    Contains resolver methods for retrieving standard and file data.
    """

    @strawberry.field
    async def standard(
        self, info: ExecutionContext, numdos: str = ""
    ) -> StandardType | None:
        """
        Resolver method to retrieve a standard by numdos.

        Args:
            info: The execution context.
            numdos: The numdos of the standard to retrieve (optional).

        Returns:
            The retrieved standard, or None if not found.
        """
        db: MyDb = info.context["db"]
        standard: Standard | None = await db.get_standard(numdos)
        return StandardType(**standard) if standard else None

    @strawberry.field
    async def file(
        self, info: ExecutionContext, numdos: str = "", numdosvl: str = ""
    ) -> FileType | None:
        """
        Resolver method to retrieve a file by numdos and numdosvl.

        Args:
            info: The execution context.
            numdos: The numdos of the file to retrieve.
            numdosvl: The numdosvl of the file to retrieve.

        Returns:
            The retrieved file, or None if not found.
        """
        db: MyDb = info.context["db"]
        file: File | None = await db.get_file(numdos, numdosvl)
        return FileType(**file) if file else None

    @strawberry.field
    async def standards(self, info: ExecutionContext) -> list[StandardType]:
        """
        Resolver method to retrieve all standards.

        Args:
            info: The execution context.

        Returns:
            The list of all standards.
        """
        db: MyDb = info.context["db"]
        standards: list[Standard] = await db.get_standards()
        return [StandardType(**std) for std in standards]

    @strawberry.field
    async def files(self, info: ExecutionContext) -> list[FileType]:
        """
        Resolver method to retrieve all files.

        Args:
            info: The execution context.

        Returns:
            The list of all files.
        """
        db: MyDb = info.context["db"]
        files: list[File] = await db.get_files()
        return [FileType(**file) for file in files]
