from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Response
import pytest
import pytest_asyncio
from pytest_mock import MockerFixture
from standards.app import MyApp
from standards.db import MyDb
from standards.db.models import Base, Standard
from standards.graphql import get_schema


@pytest_asyncio.fixture
async def app() -> MyApp:
    db: MyDb = await MyDb.start(db_url="sqlite+aiosqlite://")
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    app: MyApp = await MyApp.start(fastapi=FastAPI(), db=db, schema=get_schema())
    yield app
    await app.db.close()


@pytest.fixture
def client(app: MyApp) -> TestClient:
    yield TestClient(app.api)


class TestMyApp:
    def test_api_hello(self, client: TestClient) -> None:
        response: Response = client.get("/hello/me")
        assert response.json() == "Hello Me!"

    def test_api_standard(self, mocker: MockerFixture, client: TestClient) -> None:
        mock: MagicMock = mocker.patch(
            "standards.db.MyDb.get_standard", return_value=None
        )
        client.get("/standard/abc")
        mock.assert_called_once_with("abc")

    def test_api_standards(self, mocker: MockerFixture, client: TestClient) -> None:
        values: list[Standard] = [Standard(numdos="numdos")]
        mock: MagicMock = mocker.patch(
            "standards.db.MyDb.get_standards", return_value=values
        )
        resp: Response = client.get("/standards")
        mock.assert_called_once_with()
        assert resp.json() == [{**values[0]}]

    def test_api_file(self, mocker: MockerFixture, client: TestClient) -> None:
        mock: MagicMock = mocker.patch("standards.db.MyDb.get_file", return_value=None)
        client.get("/file?numdos=abc&numdosvl=def")
        mock.assert_called_once_with("abc", "def")

    def test_api_files(self, mocker: MockerFixture, client: TestClient) -> None:
        mock: MagicMock = mocker.patch("standards.db.MyDb.get_files", return_value=[])
        resp: Response = client.get("/files")
        mock.assert_called_once_with()
        assert resp.json() == []
