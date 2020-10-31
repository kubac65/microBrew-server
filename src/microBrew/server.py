import logging
import struct
from collections import namedtuple
from socket import socket, AF_INET, SOCK_STREAM
from .decision_module import DecisionModule
from .temp_logger import TempLogger
from .device_manager import DeviceManager
from .brew_repository import BrewRepository
from .exceptions import MicroBrewError


RCV_MSG_SIZE = 32
LISTEN_PORT = 52100
CONNECTION_LIMIT = 10

SensorMessage = namedtuple(
    "SensorMessage",
    [
        "mac_address",
        "beer_temp",
        "ambient_temp",
        "heater_state",
        "cooler_state",
    ],
)


class Server(object):
    def __init__(
        self,
        device_manager: DeviceManager,
        brew_repository: BrewRepository,
        temp_logger: TempLogger,
        decision_module: DecisionModule,
    ):
        self.__device_manager = device_manager
        self.__brew_repository = brew_repository
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
                self.__handle_connection(connection, address[0])
                connection.close()
                logging.info(f"Closed connection from: {address[0]}")
            except MicroBrewError:
                logging.error("Error occured")
            except:
                logging.exception("Unhandled exception occured")

    def __handle_connection(self, sock: socket, ip_address: str):
        received_msg = Server.__receive_message(sock)

        # Update device status in devices DB and get device's active brew
        is_new_device = self.__device_manager.update_status(
            received_msg.mac_address, ip_address
        )

        if is_new_device:
            Server.__send_message_to_unasigned_device(sock)
            return

        active_brew_info = self.__brew_repository.get_device_active_brew(
            received_msg.mac_address
        )

        if active_brew_info == None:
            Server.__send_message_to_unasigned_device(sock)
            return

        # Decision module will tell us whether the heater needs to be turned on or off.
        # But, together with that we'll send the temp ranges to the controller.
        # This will ensure that the controller will be able to maintaing the temperature even if the network connection has been proken.
        target_state = self.__decision_module.get_target_state(
            received_msg.beer_temp,
            received_msg.ambient_temp,
            received_msg.heater_state,
            received_msg.cooler_state,
            active_brew_info,
        )

        self.__temp_logger.log(
            active_brew_info.id,
            received_msg.beer_temp,
            received_msg.ambient_temp,
            received_msg.heater_state,
            target_state.heater_state,
            received_msg.cooler_state,
            target_state.cooler_state,
        )

        Server.__send_message(
            sock,
            heater_state=target_state.heater_state,
            cooler_state=target_state.cooler_state,
            min_temp=active_brew_info.min_temp,
            max_temp=active_brew_info.max_temp,
        )

    @staticmethod
    def __receive_message(sock: socket) -> SensorMessage:
        received_bytes = 0
        chunks = []
        while received_bytes < RCV_MSG_SIZE:
            chunk = sock.recv(RCV_MSG_SIZE - received_bytes)
            chunks.append(chunk)
            received_bytes = received_bytes + len(chunk)

        msg = b"".join(chunks)
        logging.debug(f"Received msg: {msg}")

        # Message comes in the following binary format and the byte order is little-endian
        # |--mac address--|--padding--|--beer temp--|--ambient temp--|--heater state--|--cooler state--|--padding--|
        # |--17 bytes-----|--3 bytes--|--4 bytes----|--4 bytes-------|--1 byte--------|--1 byte--------|--2 bytes--|
        # |--string-------|-----------|--float------|--float---------|--bool----------|--bool----------|-----------|

        (
            mac_address,
            beer_temp,
            ambient_temp,
            heater_state,
            cooler_state,
        ) = struct.unpack("<17s3xff??xx", msg)

        mac_address = mac_address.decode()
        return SensorMessage(
            mac_address,
            float(beer_temp),
            float(ambient_temp),
            bool(heater_state),
            bool(cooler_state),
        )

    @staticmethod
    def __send_message(
        sock: socket,
        heater_state: bool,
        cooler_state: bool,
        min_temp: float,
        max_temp: float,
    ):
        # Response is sent back to the controller in the following binary format and the byte order is little-endian
        # |--min temp--|--max temp--|--heater state--|--cooler state--|
        # |--4 bytes---|--4 bytes---|--2 bytes-------|--2 bytes-------|
        # |--float-----|--float-----|--bool----------|--bool----------|
        logging.debug(
            f"Sending messge to device {heater_state=}, {cooler_state=}, {min_temp=}, {max_temp=}"
        )
        msg = struct.pack("<ff??", min_temp, max_temp, heater_state, cooler_state)
        logging.debug(f"Sent msg: {msg}")
        sock.sendall(msg)

    @staticmethod
    def __send_message_to_unasigned_device(sock: socket):
        Server.__send_message(
            sock,
            heater_state=False,
            cooler_state=False,
            min_temp=0,
            max_temp=0,
        )
