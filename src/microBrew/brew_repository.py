import logging
from collections import namedtuple
from cloudant.client import CouchDB
from cloudant.adapters import HTTPAdapter


# BrewInfo = namedtuple("BrewInfo", ["brew_id", "active", "min_temp", "max_temp"])


class BrewInfo(object):
    def __init__(self, brew_id: int, active: bool, min_temp: float, max_temp: float):
        self.brew_id = brew_id
        self.active = active
        self.min_temp = min_temp
        self.max_temp = max_temp


class BrewRepository(object):
    def __init__(
        self,
        db_host: str,
        db_port: int,
        db_username: str,
        db_password: str,
        db_database: str,
    ):
        url = f"http://{db_host}:{db_port}"
        self.__client = CouchDB(
            db_username,
            db_password,
            url=url,
            connect=True,
            adapter=HTTPAdapter(max_retries=10),
        )
        self.__db = self.__client.create_database(db_database)

    def get_brew_info(self, brew_id: int) -> BrewInfo:
        try:
            brew = self.__db[str(brew_id)]
            return BrewInfo(
                int(brew["_id"]),
                brew["active"],
                brew["temp"]["min"],
                brew["temp"]["max"],
            )
        except KeyError:
            logging.warning(f"Brew: {brew_id} not found in the DB")
