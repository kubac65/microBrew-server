import pytest
from mock import MagicMock

from microBrew.brew_repository import BrewRepository


@pytest.fixture
def couch_db_response(mac_address):
    return {
        "_id": "1",
        "device_mac_address": mac_address,
        "active": True,
        "temperature": {"min": 20.1, "max": 27.2},
    }


def test_constructor_db_exists(db_name):
    mock_couch_db_client = MagicMock()
    BrewRepository(mock_couch_db_client, db_name)

    mock_couch_db_client.create_database.assert_not_called()


def test_constructor_db_does_not_exist(db_name):
    mock_couch_db_client = MagicMock()
    mock_couch_db_client.__getitem__.side_effect = KeyError
    BrewRepository(mock_couch_db_client, db_name)

    mock_couch_db_client.create_database.assert_called_with(db_name)


def test_get_device_active_brew_too_many_results(db_name, mac_address):
    mock_couch_db_client = MagicMock()
    mock_couch_db_client.get_query_result.return_value = [MagicMock(), MagicMock()]

    repository = BrewRepository(mock_couch_db_client, db_name)
    result = repository.get_device_active_brew(mac_address)

    assert result is None


def test_get_device_active_no_results(db_name, mac_address):
    mock_couch_db_client = MagicMock()
    mock_couch_db_client.get_query_result.return_value = []

    repository = BrewRepository(mock_couch_db_client, db_name)
    result = repository.get_device_active_brew(mac_address)

    assert result is None


def test_get_device_active_valid_happy_path(db_name, mac_address, couch_db_response):
    mock_couch_db = MagicMock()
    mock_couch_db.get_query_result.return_value = [[couch_db_response]]
    mock_couch_db_client = MagicMock()
    mock_couch_db_client.__getitem__.return_value = mock_couch_db

    repository = BrewRepository(mock_couch_db_client, db_name)
    result = repository.get_device_active_brew(mac_address)

    assert result
    assert result.id == couch_db_response["_id"]
    assert result.active is True
    assert result.min_temp == couch_db_response["temperature"]["min"]
    assert result.max_temp == couch_db_response["temperature"]["max"]
    assert result.device_mac_address == couch_db_response["device_mac_address"]
