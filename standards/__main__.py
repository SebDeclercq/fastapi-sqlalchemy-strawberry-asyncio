import asyncio
import os
import uvicorn
from .api import start_api
from .db import MyDb, start_db

__all__: list[str] = []


if __name__ == "__main__":
    default_db_url: str = "sqlite+aiosqlite://"
    db_url: str = os.getenv("DB_URL", default_db_url)
    in_memory_db: bool = db_url == default_db_url

    db: MyDb = asyncio.run(start_db(db_url=db_url, in_memory_db=in_memory_db))

    uvicorn.run(asyncio.run(start_api()), host="0.0.0.0", port=8000)
