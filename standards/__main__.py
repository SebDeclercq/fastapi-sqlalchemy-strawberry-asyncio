import asyncio
import uvicorn
from .api import start_api

__all__: list[str] = []


if __name__ == "__main__":
    uvicorn.run(asyncio.run(start_api()), host="0.0.0.0", port=8000)
