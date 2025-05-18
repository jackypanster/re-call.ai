import pytest
from unittest.mock import patch, MagicMock
from app.services.database import DatabaseService

@patch("app.services.database.create_client")
def test_database_service_init(mock_create_client):
    mock_client = MagicMock()
    mock_create_client.return_value = mock_client
    service = DatabaseService()
    assert service.client == mock_client

@patch("app.services.database.create_client")
def test_insert_record(mock_create_client):
    mock_client = MagicMock()
    mock_create_client.return_value = mock_client
    service = DatabaseService()
    mock_table = mock_client.table.return_value
    mock_insert = mock_table.insert.return_value
    mock_insert.execute.return_value = {"data": "ok"}
    result = service.insert_record("test_table", {"foo": "bar"})
    assert result == {"data": "ok"}

@patch("app.services.database.create_client")
def test_get_records(mock_create_client):
    mock_client = MagicMock()
    mock_create_client.return_value = mock_client
    service = DatabaseService()
    mock_table = mock_client.table.return_value
    mock_select = mock_table.select.return_value
    mock_select.execute.return_value = {"data": ["row1", "row2"]}
    result = service.get_records("test_table")
    assert result == {"data": ["row1", "row2"]} 