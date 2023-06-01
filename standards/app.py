from typing import Any
import pydantic
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from ._private.pydantic import Config as _PydanticConfig
from .db import MyDb
from .db.models import File, Standard


__all__: list[str] = ["MyApp"]


class MyApp(pydantic.BaseModel):
    api: FastAPI
    db: MyDb
    graphql_schema: strawberry.Schema

    Config = _PydanticConfig

    @classmethod
    async def start(
        cls, fastapi: FastAPI, db: MyDb, schema: strawberry.Schema
    ) -> FastAPI:
        self: MyApp = cls(api=fastapi, db=db, graphql_schema=schema)
        await self.setup()
        return self  # type: ignore # mypy shouldn't warn with MyAPI.__call__

    def __call__(self) -> FastAPI:
        return self.api

    async def setup(self) -> None:
        await self._setup_handlers()
        await self._setup_routes()
        await self._setup_graphql()

    async def _setup_handlers(self) -> None:
        self.api.add_event_handler("startup", self._startup)
        self.api.add_event_handler("shutdown", self._shutdown)

    async def _setup_routes(self) -> None:
        @self.api.get("/hello/{name}")
        async def hello(name: str = "stranger") -> str:
            return f"Hello {name.title()}!"

        @self.api.get("/standard/{numdos}")
        async def get_standard(numdos: str) -> dict[str, Any]:
            standard: Standard | None = await self.db.get_standard(numdos)
            return {**standard} if standard else {}

        @self.api.get("/standards")
        async def get_standards() -> list[dict[str, Any]]:
            standards: list[Standard] = await self.db.get_standards()
            return [{**standard} for standard in standards]

        @self.api.get("/file")
        async def get_file(numdos: str, numdosvl: str) -> dict[str, Any]:
            file: File | None = await self.db.get_file(numdos, numdosvl)
            return {**file} if file else {}

        @self.api.get("/files")
        async def get_files() -> list[dict[str, Any]]:
            files: list[File] = await self.db.get_files()
            return [{**file} for file in files]

    async def _setup_graphql(self):
        self.api.include_router(
            GraphQLRouter(self.graphql_schema, context_getter=lambda: {"db": self.db}),
            prefix=r"/graphql",
        )

    async def _startup(self) -> None:
        await self.db.connect()

    async def _shutdown(self) -> None:
        await self.db.close()
