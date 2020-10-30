import logging
from collections import namedtuple
from cloudant.client import CouchDB


BrewInfo = namedtuple("BrewInfo", ["brew_id", "active", "min_temp", "max_temp"])


class BrewRepository(object):
    def __init__(
        self,
        couch_db_client: CouchDB,
        db_name: str,
    ):
        self.__client = couch_db_client
        self.__db = self.__client.create_database(db_name)

    def get_brew_info(self, brew_id: int) -> BrewInfo:
        logging.info(f"Getting brew info for {brew_id=}")
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
            return None
