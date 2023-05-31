import asyncio
import os
from fastapi import FastAPI
import strawberry
import uvicorn
from .app import start_app
from .db import MyDb, start_db
from .graphql import get_schema

__all__: list[str] = []


if __name__ == "__main__":
    api: FastAPI = FastAPI()

    db_url: str = os.getenv("DB_URL", "sqlite+aiosqlite://")
    db: MyDb = asyncio.run(start_db(db_url=db_url))

    schema: strawberry.Schema = get_schema()

    uvicorn.run(asyncio.run(start_app(api, db, schema)), host="0.0.0.0", port=8000)
