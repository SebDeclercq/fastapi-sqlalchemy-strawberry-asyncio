import strawberry
from strawberry.types import ExecutionContext
from .types import StandardType
from ..db import MyDb
from ..db.models import Standard


@strawberry.type
class Query:
    @strawberry.field
    async def standard(
        self, info: ExecutionContext, numdos: str = ""
    ) -> StandardType | None:
        db: MyDb = info.context["db"]
        standard: Standard | None = await db.get_standard(numdos)
        return standard
