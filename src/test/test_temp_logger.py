import pytest
from mock import patch
from microBrew.temp_logger import TempLogger


@pytest.fixture
def db_host():
    return "localhost"


@pytest.fixture
def db_port():
    return 90


@pytest.fixture
def db_username():
    return "user"


@pytest.fixture
def db_password():
    return "password"


@pytest.fixture
def db_name():
    return "db"


@patch("microBrew.temp_logger.InfluxDBClient")
def test_constructor(
    mock_influx_client, db_host, db_port, db_username, db_password, db_name
):
    TempLogger(db_host, db_port, db_username, db_password, db_name)

    mock_influx_client.assert_called_with(
        db_host, db_port, db_username, db_password, db_name, retries=10
    )
    mock_influx_client().create_database.assert_called_with(db_name)
    mock_influx_client().switch_database.assert_called_with(db_name)


@patch("microBrew.temp_logger.InfluxDBClient")
def test_log_happy_path(
    mock_influx_client, db_host, db_port, db_username, db_password, db_name
):
    temp_logger = TempLogger(db_host, db_port, db_username, db_password, db_name)
