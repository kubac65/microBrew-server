import logging
from collections import namedtuple
from cloudant.client import CouchDB


BrewInfo = namedtuple(
    "BrewInfo", ["id", "active", "min_temp", "max_temp", "device_mac_address"]
)


class BrewRepository(object):
    def __init__(self, couch_db_client: CouchDB, db_name: str):
        self.__client = couch_db_client
        try:
            self.__db = self.__client[db_name]
            logging.info(f"Connected to existing db {db_name=}")
        except KeyError:
            self.__db = self.__client.create_database(db_name)
            logging.info(f"Created new db {db_name=}")

    def get_device_active_brew(self, mac_address: str) -> BrewInfo:
        logging.info(f"Getting brew info for device: {mac_address}")
        results = self.__db.get_query_result(
            selector={"device_mac_address": mac_address, "active": True}
        )

        # QueryResult does not include length...so this is just a simple workaround
        found_results = len(results[:])
        if found_results > 1:
            logging.warning(
                f"Inconclusive. Device {mac_address} is assigned to {found_results} active brews"
            )
            return None

        if found_results == 0:
            logging.info(
                f"Device: {mac_address}, currently not assigned to an active brew"
            )
            return None

        return BrewInfo(
            results[0][0]["_id"],
            results[0][0]["active"],
            results[0][0]["temperature"]["min"],
            results[0][0]["temperature"]["max"],
            results[0][0]["device_mac_address"],
        )
