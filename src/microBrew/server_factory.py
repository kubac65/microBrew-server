import os
import logging
from .temp_logger import TempLogger
from .brew_repository import BrewRepository
from .decision_module import DecisionModule
from .server import Server

from cloudant.client import CouchDB
from cloudant.adapters import HTTPAdapter


def __get_temp_logger():
    db_host = os.environ["INFLUX_DB_HOST"]
    db_port = os.environ["INFLUX_DB_PORT"]
    db_username = os.environ["INFLUX_DB_USERNAME"]
    db_password = os.environ["INFLUX_DB_PASSWORD"]
    db_name = f"{os.environ['DB_NAME_PREFIX']}-temperature"
    logging.info(f"Initialising TempLogger with {db_host=}, {db_port=}, {db_name=}")
    return TempLogger(db_host, db_port, db_username, db_password, db_name)


def __get_brew_repository(couch_db: CouchDB):
    db_name = f"{os.environ['DB_NAME_PREFIX']}-brews"
    logging.info(f"Initialising BrewRepository with {db_name=}")
    return BrewRepository(couch_db, db_name)


def __get_couch_db_client():
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
        adapter=HTTPAdapter(max_retries=10),
    )


def create_server():
    couch_db = __get_couch_db_client()
    temp_logger = __get_temp_logger()
    brew_repo = __get_brew_repository(couch_db)
    decision_module = DecisionModule(brew_repo)
    return Server(temp_logger, decision_module)
