import logging
import socket
import os

from microBrew import Server, TempLogger, TempRange, DecisionModule

def get_temp_logger():
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_username = os.environ['DB_USERNAME']
    db_password = os.environ['DB_PASSWORD']
    db_database = os.environ['DB_DATABASE']
    return TempLogger(db_host, db_port, db_username, db_password, db_database)

def get_temp_range():
    return TempRange()

def get_decision_module():
    return DecisionModule()

def main():
    temp_loger = get_temp_logger()
    temp_range = get_temp_range()
    decision_module = get_decision_module()
    srv = Server(temp_loger, temp_range, decision_module)
    srv.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

