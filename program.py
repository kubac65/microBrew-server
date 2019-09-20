import logging
import socket
import os

from microBrew import server_factory

def main():
    srv = server_factory.create_server()
    srv.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
