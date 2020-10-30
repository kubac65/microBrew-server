import logging
import pytest

logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(message)s")


@pytest.fixture
def db_name():
    return "db_name"


@pytest.fixture
def mac_address():
    "xx:xx:xx:xx:xx"
