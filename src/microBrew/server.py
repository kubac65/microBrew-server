import logging
import struct
from collections import namedtuple
from socket import socket, AF_INET, SOCK_STREAM
from .decision_module import DecisionModule
from .temp_logger import TempLogger
from .exceptions import MalformedMessageError


RCV_MSG_SIZE = 36
LISTEN_PORT = 52100
CONNECTION_LIMIT = 10

SensorMessage = namedtuple(
    "SensorMessage",
    [
        "mac_address",
        "brew_id",
        "beer_temp",
        "ambient_temp",
        "heater_state",
        "cooler_state",
    ],
)


class Server(object):
    def __init__(self, temp_logger: TempLogger, decision_module: DecisionModule):
        self.__temp_logger = temp_logger
        self.__decision_module = decision_module

    def start(self):
        """
        Starts listening for incoming connections
        """

        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(("", LISTEN_PORT))
        sock.listen(CONNECTION_LIMIT)

        while True:
            try:
                logging.info("Waiting for connections")
                connection, address = sock.accept()
                logging.info(f"Accepted connection from: {address[0]}")
                self.__handle_connection(connection)
            except MalformedMessageError:
                logging.error("Error occured")

    def __handle_connection(self, sock: socket):
        received_msg = Server.__receive_message(sock)

        # Update device status in devices DB and get device's active brew

        active_brew_info = None

        if active_brew_info == None:
            logging.info(
                f"Sensor: {received_msg.mac_address}, currently not assigned to an active brew"
            )
            Server.__send_message(
                sock,
                brew_id=0,
                heater_state=False,
                cooler_state=False,
                min_temp=0,
                max_temp=100,
            )
            return

        # Decision module will tell us whether the heater needs to be turned on or off.
        # But, together with that we'll send the temp ranges to the controller.
        # This will ensure that the controller will be able to maintaing the temperature even if the network connection has been proken.
        heater_target_state, cooler_target_state = (False, False)

        self.__temp_logger.log(
            brew_id,
            beer_temp,
            ambient_temp,
            heater_current_state,
            heater_desired_state,
            cooler_current_state,
            cooler_desired_state,
        )

        Server.__send_message(
            sock,
            brew_id=active_brew_info.brew_id,
            heater_state=heater_target_state,
            cooler_state=cooler_target_state,
            min_temp=active_brew_info.min_temp,
            max_temp=active_brew_info.max_temp,
        )
        sock.close()
        logging.info(f"Closed connection from: {address}")

    @staticmethod
    def __receive_message(sock: socket):
        received_bytes = 0
        chunks = []
        while received_bytes < RCV_MSG_SIZE:
            chunk = sock.recv(RCV_MSG_SIZE - received_bytes)
            chunks.append(chunk)
            received_bytes = received_bytes + len(chunk)

        # Message comes in the following binary format and the byte order is little-endian
        # |--brew id--|--beer temp--|--ambient temp--|--heater state--|--cooler state--|
        # |--4 bytes--|--4 bytes----|--4 bytes-------|--2 bytes-------|--2 bytes-------|
        # |--integer--|--float------|--float---------|--bool----------|--bool----------|

        (
            mac_address,
            brew_id,
            beer_temp,
            ambient_temp,
            heater_state,
            cooler_state,
        ) = struct.unpack("<20sIffHH", b"".join(chunks))

        return SensorMessage(
            mac_address, brew_id, beer_temp, ambient_temp, heater_state, cooler_state
        )

    @staticmethod
    def __send_message(
        sock: socket,
        brew_id: int,
        heater_state: bool,
        cooler_state: bool,
        min_temp: float,
        max_temp: float,
    ):
        # Response is sent back to the controller in the following binary format and the byte order is little-endian
        # |--brew id--|--min temp--|--max temp--|--heater state--|--cooler state--|
        # |--4 bytes--|--4 bytes---|--4 bytes---|--2 bytes-------|--2 bytes-------|
        # |--integer--|--float-----|--float-----|--bool----------|--bool----------|
        logging.debug(
            f"Sending messge to sensor {brew_id=}, {heater_state=}, {cooler_state=}, {min_temp=}, {max_temp=}"
        )
        msg = struct.pack(
            "<IffHH", brew_id, min_temp, max_temp, heater_state, cooler_state
        )
        sock.sendall(msg)
