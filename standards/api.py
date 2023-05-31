from fastapi import FastAPI
import pydantic
from ._pydantic import Config as _PydanticConfig


__all__: list[str] = ["start_api", "MyAPI"]


async def start_api() -> FastAPI:
    api: MyAPI = MyAPI(api=FastAPI())
    await api.setup_routes()
    return api  # type: ignore # this isn't true with MyAPI.__call__


class MyAPI(pydantic.BaseModel):
    api: FastAPI

    Config = _PydanticConfig

    def __call__(self) -> FastAPI:
        return self.api

    async def setup_routes(self) -> None:
        @self.api.get("/hello/{name}")
        async def hello(name: str = "stranger") -> str:
            return f"Hello {name.title()}!"
