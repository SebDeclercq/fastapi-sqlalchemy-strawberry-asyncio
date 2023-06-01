from unittest.mock import MagicMock
from fastapi import FastAPI
import pytest
from pytest_mock import MockerFixture
from standards.app import MyApp
from standards.db import MyDb
from standards.__main__ import main


@pytest.mark.asyncio
async def test_main(mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DB_URL", "hahaha")
    mock_start_db: MagicMock = mocker.patch.object(MyDb, "start")
    mock_app: MagicMock = mocker.patch.object(FastAPI, "__init__", return_value=None)
    mock_setup: MagicMock = mocker.patch.object(MyApp, "start")

    await main()

    mock_start_db.assert_called_once_with(db_url="hahaha")
    mock_app.assert_called_once_with()
    mock_setup.assert_called_once()  # not with due to multiple mocks and it's boring
