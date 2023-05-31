from __future__ import annotations
from sqlalchemy import CheckConstraint, Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


__all__: list[str] = ["Base", "File", "Standard"]


class Base(DeclarativeBase):
    pass


class Standard(Base):
    __tablename__: str = "standards"

    numdos: Column = Column(String, CheckConstraint("numdos ~ '^[A-Z]\d+$"))
    files: Mapped[list[File]] = relationship(
        back_populates="standard", cascade="all, delete-orphan"
    )


class File(Base):
    __tablename__: str = "files"

    name: Mapped[str]
    numdosvl: Mapped[str]
    numdos: Mapped[str] = mapped_column(ForeignKey("standard.numdos"))
    standard: Mapped[Standard] = relationship(back_populates="files")

    __table_args__: CheckConstraint = CheckConstraint(
        "SUBSTRING(numdosvl, 2, 1) = SUBSTRING(numdos, 2, 1)",
    )
