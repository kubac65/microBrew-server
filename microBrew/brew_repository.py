from cloudant.client import CouchDB
from cloudant.adapters import HTTPAdapter

class BrewRepository(object):
    def __init__(self, db_host, db_port, db_username, db_password, db_database):
        url = f'http://{db_host}:{db_port}'
        self.__client = CouchDB(db_username, db_password, url=url, connect=True, adapter = HTTPAdapter(max_retries=10))
        self.__db = self.__client.create_database(db_database)


    def get_brew_info(self, brew_id):
        return self.__db[brew_id]

    def get_temp_range(self, brew_id):
        brew = self.__db[brew_id]
        min = brew['temp']['min']
        max = brew['temp']['max']
        return (min, max)
