import os
from . import TempLogger
from . import BrewRepository
from . import DecisionModule
from . import Server


def __get_temp_logger():
    db_host = os.environ['TS_DB_HOST']
    db_port = os.environ['TS_DB_PORT']
    db_username = os.environ['TS_DB_USERNAME']
    db_password = os.environ['TS_DB_PASSWORD']
    db_database = os.environ['TS_DB_DATABASE']
    return TempLogger(db_host, db_port, db_username, db_password, db_database)


def __get_brew_repository():
    db_host = os.environ['BR_DB_HOST']
    db_port = os.environ['BR_DB_PORT']
    db_username = os.environ['BR_DB_USERNAME']
    db_password = os.environ['BR_DB_PASSWORD']
    db_database = os.environ['BR_DB_DATABASE']
    return BrewRepository(db_host, db_port, db_username, db_password, db_database)


def create_server():
    temp_logger = __get_temp_logger()
    brew_repo = __get_brew_repository()
    decision_module = DecisionModule(brew_repo)
    return Server(temp_logger, decision_module)
