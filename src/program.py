import logging
import socket
import os
from microBrew import server_factory


def main():
    logging.basicConfig(level=logging.DEBUG)
    srv = server_factory.create_server()
    srv.start()


if __name__ == "__main__":
    main()
