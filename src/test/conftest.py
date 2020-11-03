import logging
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(message)s")


@pytest.fixture
def db_name():
    return "db_name"


@pytest.fixture
def mac_address():
    "xx:xx:xx:xx:xx"
