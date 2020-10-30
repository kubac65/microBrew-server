import logging
from datetime import datetime
from cloudant.client import CouchDB

STATUS_CREATED = "created"
STATUS_UPDATED = "updated"


class DeviceManager:
    def __init__(self, couch_db_client: CouchDB, db_name: str):
        self.__client = couch_db_client
        try:
            self.__db = self.__client[db_name]
            logging.info(f"Connected to existing db {db_name=}")
        except KeyError:
            self.__db = self.__client.create_database(db_name)
            logging.info(f"Created new db {db_name=}")

    def update_status(self, mac_address: str, ip_address: str):
        last_seen = datetime.now().isoformat()
        if mac_address in self.__db:
            logging.info(
                f"Updating device record {mac_address=}, {ip_address=}, {last_seen}"
            )
            record = self.__db[mac_address]
            record["last_network_address"] = ip_address
            record["last_seen"] = last_seen
            record.save()
            return mac_address
        else:
            logging.info(
                f"Creating device record {mac_address=}, {ip_address=}, {last_seen}"
            )
            self.__db.create_document(
                {
                    "_id": mac_address,
                    "last_network_address": ip_address,
                    "last_seen": datetime.now().isoformat(),
                }
            )
            return None
