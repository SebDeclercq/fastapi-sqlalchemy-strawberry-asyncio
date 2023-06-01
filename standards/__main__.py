import asyncio
import os
from fastapi import FastAPI
import strawberry
import uvicorn
from .app import MyApp
from .db import MyDb
from .graphql import get_schema

__all__: list[str] = ["main"]


async def main() -> FastAPI:
    """
    Main function to start the FastAPI application.

    Returns:
        FastAPI: The initialized FastAPI application.
    """
    api: FastAPI = FastAPI()

    db_url: str = os.getenv("DB_URL", "sqlite+aiosqlite://")
    db: MyDb = await MyDb.start(db_url=db_url)

    schema: strawberry.Schema = get_schema()

    return await MyApp.start(api, db, schema)


if __name__ == "__main__":
    uvicorn.run(
        asyncio.run(main()),
        host="0.0.0.0",
        port=8000,
    )
