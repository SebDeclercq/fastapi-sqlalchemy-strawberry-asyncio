from fastapi import Depends, FastAPI
import pydantic
from ._private.pydantic import Config as _PydanticConfig
from .db import MyDb
from .db.models import Standard


__all__: list[str] = ["start_api", "MyAPI"]


async def start_api(db: MyDb) -> FastAPI:
    api: MyAPI = MyAPI(api=FastAPI(), db=db)
    await api.setup()
    return api  # type: ignore # this isn't true with MyAPI.__call__


class MyAPI(pydantic.BaseModel):
    api: FastAPI
    db: MyDb

    Config = _PydanticConfig

    def __call__(self) -> FastAPI:
        return self.api

    async def setup(self) -> None:
        await self._setup_handlers()
        await self._setup_routes()

    async def _setup_handlers(self) -> None:
        self.api.add_event_handler("startup", self._startup)
        self.api.add_event_handler("shutdown", self._shutdown)

    async def _setup_routes(self) -> None:
        @self.api.get("/hello/{name}")
        async def hello(name: str = "stranger") -> str:
            return f"Hello {name.title()}!"

        @self.api.get("/standard/{numdos}")
        async def get_standard(
            numdos: str, depends=Depends(self.db.get_session)
        ) -> str:
            standard: Standard | None = await self.db.get_standard(numdos)
            return str(standard)

    async def _startup(self) -> None:
        await self.db.connect()

    async def _shutdown(self) -> None:
        await self.db.close()
