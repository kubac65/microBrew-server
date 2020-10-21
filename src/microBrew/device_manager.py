import logging
from datetime import datetime
from cloudant.client import CouchDB


class DeviceManager:
    def __init__(self, db_client: CouchDB, db_name: str):
        self.__client = db_client
        self.__client.create_database()

    def update_device_status(self, mac_address: str, address):
        {
            "mac_address": mac_address,
            "last_network_address": address,
            "last_seen": datetime.now().isoformat(),
        }
