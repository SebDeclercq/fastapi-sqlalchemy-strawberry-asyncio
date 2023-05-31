from __future__ import annotations
from abc import abstractmethod
from typing import ClassVar, Iterable
from sqlalchemy import CheckConstraint, Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from traitlets import Any


__all__: list[str] = ["Base", "File", "Standard"]


class Base(DeclarativeBase):
    def __iter__(self):
        for key in self.keys():
            yield key, getattr(self, key)

    def __getitem__(self, item: Any) -> Any:
        return getattr(self, item)

    @abstractmethod
    def keys(self) -> list[str]:
        raise NotImplemented()


class Standard(Base):
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
    __tablename__: str = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    numdosvl: Mapped[str]
    numdos: Mapped[str] = mapped_column(ForeignKey("standards.numdos"))
    standard: Mapped[Standard] = relationship(back_populates="files")

    __table_args__: tuple[CheckConstraint, ...] = tuple(
        CheckConstraint(
            "SUBSTRING(numdosvl, 2, 1) = SUBSTRING(numdos, 2, 1)",
        )
    )

    def keys(self) -> list[str]:
        return ["id", "name", "numdos", "numdosvl", "standard"]

    def __repr__(self) -> str:
        return f"File(numdos={self.numdos}, numdosvl={self.numdosvl}, name={self.name})"
