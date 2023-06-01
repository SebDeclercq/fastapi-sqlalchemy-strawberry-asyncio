from __future__ import annotations
import strawberry


@strawberry.type
class StandardType:
    """
    Represents a standard.

    Attributes:
        numdos: The numdos attribute of the standard type.
        files: The list of files associated with the standard type.
    """

    numdos: str
    files: list[FileType]


@strawberry.type
class FileType:
    """
    Represents a file type.

    Attributes:
        id: The ID of the file type.
        name: The name of the file type.
        numdosvl: The numdosvl attribute of the file type.
        numdos: The numdos attribute of the file type.
        standard: The associated standard type.
    """

    id: int
    name: str
    numdosvl: str
    numdos: str
    standard: StandardType
