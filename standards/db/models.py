from __future__ import annotations
from abc import abstractmethod
from typing import Any
from sqlalchemy import CheckConstraint, Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from .._private.enum import FileFormat, FileLanguage


__all__: list[str] = ["Base", "File", "Standard"]


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.

    Provides common methods and attributes for models.
    """

    def __iter__(self):
        """
        Iterates over the model attributes.

        Yields:
            A tuple containing the attribute name and its value.
        """
        for key in self.keys():
            yield key, getattr(self, key)

    def __getitem__(self, item: str) -> Any:
        """
        Retrieves the value of an attribute using the subscript notation.

        Args:
            item: The attribute name.

        Returns:
            The value of the attribute.
        """
        return getattr(self, item)

    @abstractmethod
    def keys(self) -> list[str]:
        """
        Returns a list of attribute names for the model.

        This method must be implemented by subclasses.

        Returns:
            A list of attribute names.
        """
        raise NotImplemented()


class Standard(Base):
    """
    Represents a standard in the database.

    Attributes:
        numdos: The numdos column of the standard.
        files: The relationship to the files associated with the standard.
    """

    __tablename__: str = "standards"

    numdos: Column = Column(
        String, CheckConstraint(r"numdos REGEXP '^[A-Z]{2}\d+$'"), primary_key=True
    )
    files: Mapped[list[File]] = relationship(
        back_populates="standard", cascade="all, delete-orphan"
    )

    def keys(self) -> list[str]:
        return ["numdos", "files"]

    def __repr__(self) -> str:
        return f"Standard(numdos={self.numdos}, files={self.files})"


class File(Base):
    """
    Represents a file in the database.

    Attributes:
        id: The ID column of the file.
        name: The name column of the file.
        numdosvl: The numdosvl column of the file.
        numdos: The numdos column of the file.
        standard: The relationship to the standard associated with the file.
        format: The format of the file, one of FileFormat.
        language: The language of the file, one of FileLanguage.
    """

    __tablename__: str = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    numdosvl: Mapped[str]
    numdos: Mapped[str] = mapped_column(ForeignKey("standards.numdos"))
    standard: Mapped[Standard] = relationship(back_populates="files")
    format: Mapped[FileFormat]
    language: Mapped[FileLanguage]

    __table_args__: tuple[CheckConstraint, ...] = tuple(
        CheckConstraint(
            r"""
            (SUBSTRING(numdosvl, 1, 1) || substring(numdosvl, 3))
            =
            (SUBSTRING(numdos, 1, 1) || substring(numdos, 3))
            """
        )
    )

    def keys(self) -> list[str]:
        return ["id", "name", "numdos", "numdosvl", "standard", "format", "language"]

    def __repr__(self) -> str:
        return (
            f"File(numdos={self.numdos}, numdosvl={self.numdosvl}, name={self.name}, "
            f"format={self.format}, language={self.language})"
        )
