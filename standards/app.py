from __future__ import annotations
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
    """
    Represents the main application.

    Attributes:
        api: The FastAPI instance.
        db: The MyDb instance for database operations.
        graphql_schema: The Strawberry GraphQL schema.
    """

    api: FastAPI
    db: MyDb
    graphql_schema: strawberry.Schema

    Config = _PydanticConfig

    @classmethod
    async def start(
        cls, fastapi: FastAPI, db: MyDb, schema: strawberry.Schema
    ) -> MyApp:
        """
        Start the application and return the FastAPI instance.

        Args:
            fastapi: The FastAPI instance.
            db: The MyDb instance for database operations.
            schema: The Strawberry GraphQL schema.

        Returns:
            The initialized FastAPI instance.
        """
        self: MyApp = cls(api=fastapi, db=db, graphql_schema=schema)
        await self.setup()
        return self

    def __call__(self) -> FastAPI:
        """
        Callable method to retrieve the FastAPI instance.

        Returns:
            The FastAPI instance.
        """
        return self.api

    async def setup(self) -> None:
        """
        Setup the application by adding event handlers, routes, and GraphQL endpoint.
        """
        await self._setup_handlers()
        await self._setup_routes()
        await self._setup_graphql()

    async def _setup_handlers(self) -> None:
        """
        Setup event handlers for startup and shutdown.
        """
        self.api.add_event_handler("startup", self._startup)
        self.api.add_event_handler("shutdown", self._shutdown)

    async def _setup_routes(self) -> None:
        """
        Setup routes for the API endpoints.
        """

        @self.api.get(r"/hello/{name}")
        async def hello(name: str = "stranger") -> str:
            """
            Endpoint: /hello/{name}

            A simple greeting endpoint that returns a personalized greeting.

            Args:
                name: The name parameter in the path.

            Returns:
                A string containing the personalized greeting.
            """
            return f"Hello {name.title()}!"

        @self.api.get(r"/standard/{numdos}")
        async def get_standard(numdos: str) -> dict[str, Any]:
            """
            Endpoint: /standard/{numdos}

            Retrieve a standard by its numdos value.

            Args:
                numdos: The numdos parameter in the path.

            Returns:
                A dictionary containing the attributes of the standard, or an
                empty dictionary if not found.
            """
            standard: Standard | None = await self.db.get_standard(numdos)
            return {**standard} if standard else {}

        @self.api.get(r"/standards")
        async def get_standards() -> list[dict[str, Any]]:
            """
            Endpoint: /standards

            Retrieve all standards.

            Returns:
                A list of dictionaries containing the attributes of the standards.
            """
            standards: list[Standard] = await self.db.get_standards()
            return [{**standard} for standard in standards]

        @self.api.get(r"/file")
        async def get_file(numdos: str, numdosvl: str) -> dict[str, Any]:
            """
            Endpoint: /file

            Retrieve a file by its numdos and numdosvl values.

            Args:
                numdos: The numdos parameter in the query.
                numdosvl: The numdosvl parameter in the query.

            Returns:
                A dictionary containing the attributes of the file, or an empty dictionary if not found.
            """
            file: File | None = await self.db.get_file(numdos, numdosvl)
            return {**file} if file else {}

        @self.api.get(r"/files")
        async def get_files() -> list[dict[str, Any]]:
            """
            Endpoint: /files

            Retrieve all files.

            Returns:
                A list of dictionaries containing the attributes of the files.
            """
            files: list[File] = await self.db.get_files()
            return [{**file} for file in files]

    async def _setup_graphql(self):
        """
        Setup the GraphQL endpoint using Strawberry and FastAPI.
        """
        self.api.include_router(
            GraphQLRouter(self.graphql_schema, context_getter=lambda: {"db": self.db}),
            prefix=r"/graphql",
        )

    async def _startup(self) -> None:
        """
        Perform startup tasks when a HTTP request comes in.
        Connect to the database.
        """
        await self.db.connect()

    async def _shutdown(self) -> None:
        """
        Perform startup tasks when a HTTP request comes in.
        Close to connection to the database.
        """
        await self.db.close()
