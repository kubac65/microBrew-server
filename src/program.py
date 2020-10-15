import logging
import socket
import os
from microBrew import server_factory


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(clientip)s %(user)-8s %(message)s")
    srv = server_factory.create_server()
    srv.start()

if __name__ == '__main__':
    main()
