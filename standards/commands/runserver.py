import strawberry
from fastapi import FastAPI
from ..app import MyApp
from ..db import MyDb
from ..graphql import get_schema


__all__: list[str] = ["runserver"]


async def runserver(db_url: str) -> MyApp:
    api: FastAPI = FastAPI()
    db: MyDb = await MyDb.start(db_url=db_url)
    schema: strawberry.Schema = get_schema()
    return await MyApp.start(api, db, schema)
