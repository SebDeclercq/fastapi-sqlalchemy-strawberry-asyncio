from enum import Enum


__all__: list[str] = ["FileFormat", "FileLanguage"]


class FileFormat(Enum):
    XML = "xml"
    XMLRL = "xmlrl"
    PDF = "pdf"
    PDFRL = "pdfrl"


class FileLanguage(Enum):
    FR = "fr"
    EN = "en"
