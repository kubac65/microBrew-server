import logging
import datetime
from influxdb import InfluxDBClient


time_series_name = 'temperature'
db_connection_retry_count = 10


class TempLogger(object):
    """
    Temperature logger, responsible for persiting temperature readings in influx db
    """

    def __init__(self, db_host: str, db_port: int, db_username: str, db_password: str, db_database: str):
        """
        Creates an instance of the TempLogger
        """

        self.__client = InfluxDBClient(db_host, db_port, db_username, db_password, db_database, retries=db_connection_retry_count)
        self.__client.create_database(db_database)
        self.__client.switch_database(db_database)

    def log(self, brew_id: int, beer_temp: float, ambient_temp: float, initial_heater_state: bool, final_heater_state: bool, initial_cooler_state: bool, final_cooler_state: bool):
        """
        Persists the reading in influx db
        """

        logging.info(f'Brew id: {brew_id}')
        logging.info(f'Beer temp: {beer_temp}')
        logging.info(f'Ambient temp: {ambient_temp}')
        logging.info(f'Heater state: {initial_heater_state}->{final_heater_state}')
        logging.info(f'Cooler state: {initial_cooler_state}->{final_cooler_state}')

        self.__client.write_points([{
            "measurement": time_series_name,
            "time": datetime.datetime.now().isoformat(),
            "tags": {
                "brew": brew_id
            },
            "fields": {
                "beer_temp": beer_temp,
                "ambient_temp": ambient_temp,
                "initial_heater_state": initial_heater_state,
                "final_heater_state": final_heater_state,
                "initial_cooler_state": initial_cooler_state,
                "final_cooler_state": final_cooler_state,
            }
        }])
