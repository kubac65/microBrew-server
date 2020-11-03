import logging
import os

from cloudant.adapters import HTTPAdapter
from cloudant.client import CouchDB

from .brew_repository import BrewRepository
from .decision_module import DecisionModule
from .device_manager import DeviceManager
from .server import Server
from .temp_logger import TempLogger


def create_server() -> Server:
    couch_db = __get_couch_db_client()
    temp_logger = __get_temp_logger()
    brew_repo = __get_brew_repository(couch_db)
    device_manager = __get_device_manager(couch_db)
    decision_module = DecisionModule()
    return Server(device_manager, brew_repo, temp_logger, decision_module)


def __get_temp_logger() -> TempLogger:
    db_host = os.environ["INFLUX_DB_HOST"]
    db_port = int(os.environ["INFLUX_DB_PORT"])
    db_username = os.environ["INFLUX_DB_USERNAME"]
    db_password = os.environ["INFLUX_DB_PASSWORD"]
    db_name = f"{__get_db_name_prefix()}_temperature"
    logging.info(f"Initialising TempLogger with {db_host=}, {db_port=}, {db_name=}")
    return TempLogger(db_host, db_port, db_username, db_password, db_name)


def __get_device_manager(couch_db: CouchDB) -> DeviceManager:
    db_name = f"{__get_db_name_prefix()}_devices"
    logging.info(f"Initialising DeviceManager with {db_name=}")
    return DeviceManager(couch_db, db_name)


def __get_brew_repository(couch_db: CouchDB) -> BrewRepository:
    db_name = f"{__get_db_name_prefix()}_brews"
    logging.info(f"Initialising BrewRepository with {db_name=}")
    return BrewRepository(couch_db, db_name)


def __get_couch_db_client() -> CouchDB:
    db_host = os.environ["COUCH_DB_HOST"]
    db_port = os.environ["COUCH_DB_PORT"]
    db_username = os.environ["COUCH_DB_USERNAME"]
    db_password = os.environ["COUCH_DB_PASSWORD"]
    url = f"http://{db_host}:{db_port}"

    logging.info(f"Initialising CouchDB client using {url=}")
    return CouchDB(
        db_username,
        db_password,
        url=url,
        connect=True,
        auto_renew=True,
        adapter=HTTPAdapter(max_retries=10),
    )


def __get_db_name_prefix() -> str:
    # CloudDB doesn't accept capitals in the db names, therefore it needs to converted to lower case letters
    return os.environ["DB_NAME_PREFIX"].lower()
