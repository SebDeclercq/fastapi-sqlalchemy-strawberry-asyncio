import asyncio
import os
import pydantic
import strawberry
import typer
import uvicorn
from fastapi import FastAPI
from ._private.pydantic import Config as _PydanticConfig
from .app import MyApp
from .commands.random_populate import random_populate
from .db import MyDb
from .graphql import get_schema

__all__: list[str] = ["main"]


class StandardsCLI(pydantic.BaseModel):
    app: typer.Typer = typer.Typer()

    Config = _PydanticConfig

    def runserver(
        self,
        host: str = typer.Option(
            "0.0.0.0", "--host", "-h", help="Host to bind the server to"
        ),
        port: int = typer.Option(
            8000, "--port", "-p", help="Port for the server to listen on"
        ),
    ) -> None:
        uvicorn.run(
            asyncio.run(self._runserver()),
            host=host,
            port=port,
        )

    async def _runserver(self) -> MyApp:
        api: FastAPI = FastAPI()
        db_url: str = os.getenv("DB_URL", "sqlite+aiosqlite://")
        db: MyDb = await MyDb.start(db_url=db_url)
        schema: strawberry.Schema = get_schema()
        return await MyApp.start(api, db, schema)

    def random_populate(
        self,
        db_url: str = typer.Option(
            os.getenv("DB_URL", ""), "--db-url", help="Database URL"
        ),
        amount: int = typer.Option(
            10, "--amount", help="Number of records to populate"
        ),
    ) -> None:
        asyncio.run(random_populate(db_url=db_url, amount=amount))

    def callback(self) -> None:
        pass

    def run(self):
        self.app.command()(self.runserver)
        self.app.command()(self.random_populate)
        self.app.callback()(self.callback)
        self.app()


if __name__ == "__main__":
    cli = StandardsCLI()
    cli.run()
