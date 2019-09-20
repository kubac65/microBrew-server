import datetime
from influxdb import InfluxDBClient

time_series_name = 'temperature'
client_retries = 10

class TempLogger(object):
    def __init__(self, db_host, db_port, db_username, db_password, db_database):
        self.__client = InfluxDBClient(db_host, db_port, db_username, db_password, db_database, retries=client_retries)
        self.__client.create_database(db_database)
        self.__client.switch_database(db_database)

    def log(self, beer_temp, ambient_temp, initial_heater_state, final_heater_state):
        self.__client.write_points([{
            "measurement": time_series_name,
            "time": datetime.datetime.now().isoformat(),
            "fields": {
                "initial_heater_state": initial_heater_state,
                "final_heater_state": final_heater_state,
                "beer_temp": beer_temp,
                "ambient_temp": ambient_temp
            }
        }])
