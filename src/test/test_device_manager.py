import context
import pytest
from datetime import datetime
from mock import MagicMock, call
from freezegun import freeze_time

from microBrew.device_manager import DeviceManager


@pytest.fixture
def ip_address():
    return "ip address"


def test_constructor_db_exists(db_name):
    mock_couch_db_client = MagicMock()
    DeviceManager(mock_couch_db_client, db_name)

    mock_couch_db_client.create_database.assert_not_called()


def test_constructor_db_does_not_exist(db_name):
    mock_couch_db_client = MagicMock()
    mock_couch_db_client.__getitem__.side_effect = KeyError
    DeviceManager(mock_couch_db_client, db_name)

    mock_couch_db_client.create_database.assert_called_with(db_name)


@freeze_time("2020-01-01")
def test_update_status_device_does_not_exist(db_name, mac_address, ip_address):
    mock_couch_db = MagicMock()
    mock_couch_db.__contains__.return_value = False
    mock_couch_db_client = MagicMock()
    mock_couch_db_client.__getitem__.return_value = mock_couch_db

    dm = DeviceManager(mock_couch_db_client, db_name)
    result = dm.update_status(mac_address, ip_address)

    assert result

    expected_parameter = {
        "_id": mac_address,
        "last_network_address": ip_address,
        "last_seen": datetime.now().isoformat(),
    }
    mock_couch_db.create_document.assert_called_with(expected_parameter)


@freeze_time("2020-01-01")
def test_update_status_device_exists(db_name, mac_address, ip_address):
    existing_record = MagicMock()

    mock_couch_db = MagicMock()
    mock_couch_db.__contains__.return_value = True
    mock_couch_db.__getitem__.return_value = existing_record
    mock_couch_db_client = MagicMock()
    mock_couch_db_client.__getitem__.return_value = mock_couch_db

    dm = DeviceManager(mock_couch_db_client, db_name)
    result = dm.update_status(mac_address, ip_address)

    assert result is None

    expected_record_calls = [
        call("last_network_address", ip_address),
        call("last_seen", datetime.now().isoformat()),
    ]

    assert existing_record.__setitem__.mock_calls == expected_record_calls
    existing_record.save.assert_called()
