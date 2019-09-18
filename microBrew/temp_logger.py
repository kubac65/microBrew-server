from influxdb import InfluxDBClient

class TempLogger(object):
    def __init__(self, db_host, db_port, db_username, db_password, db_database):
        self.__client = InfluxDBClient(db_host, db_port, db_username, db_password, db_database)
        self.__client.create_database(db_database)

    def log(self, temp):
        self.__client.write({"temp": temp})
