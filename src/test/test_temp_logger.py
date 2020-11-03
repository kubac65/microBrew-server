import datetime

import pytest
from freezegun import freeze_time
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
def brew_id():
    return 1


@pytest.fixture
def beer_temp():
    return 22.2


@pytest.fixture
def ambient_temp():
    return 14.6


@pytest.fixture
def initial_heater_state():
    return True


@pytest.fixture
def final_heater_state():
    return False


@pytest.fixture
def initial_cooler_state():
    return False


@pytest.fixture
def final_cooler_state():
    return False


@pytest.fixture
@freeze_time("2020-01-01")
def expected_influx_log_record(
    brew_id,
    beer_temp,
    ambient_temp,
    initial_heater_state,
    final_heater_state,
    initial_cooler_state,
    final_cooler_state,
):
    return [
        {
            "measurement": "temperature",
            "time": datetime.datetime.now().isoformat(),
            "tags": {"brew": brew_id},
            "fields": {
                "beer_temp": beer_temp,
                "ambient_temp": ambient_temp,
                "initial_heater_state": initial_heater_state,
                "final_heater_state": final_heater_state,
                "initial_cooler_state": initial_cooler_state,
                "final_cooler_state": final_cooler_state,
            },
        }
    ]


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


@freeze_time("2020-01-01")
@patch("microBrew.temp_logger.InfluxDBClient")
def test_log_happy_path(
    mock_influx_client,
    db_host,
    db_port,
    db_username,
    db_password,
    db_name,
    brew_id,
    beer_temp,
    ambient_temp,
    initial_heater_state,
    final_heater_state,
    initial_cooler_state,
    final_cooler_state,
    expected_influx_log_record,
):
    temp_logger = TempLogger(db_host, db_port, db_username, db_password, db_name)
    temp_logger.log(
        brew_id,
        beer_temp,
        ambient_temp,
        initial_heater_state,
        final_heater_state,
        initial_cooler_state,
        final_cooler_state,
    )

    mock_influx_client().write_points.assert_called_with(expected_influx_log_record)
