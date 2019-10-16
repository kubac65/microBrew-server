import socket
import logging
import struct
from .decision_module import DecisionModule
from .temp_logger import TempLogger


# Size of the expected message
rcv_msg_size = 16

# Socket port used to listen for incoming connections
listen_port = 52100

connection_limit = 10

class Server(object):
    def __init__(self, temp_logger: TempLogger, decision_module: DecisionModule):
        self.__temp_logger = temp_logger
        self.__decision_module = decision_module

    def start(self):
        """
        Starts listening for incoming connections
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', listen_port))
        sock.listen(connection_limit)

        while True:
            logging.info('Waiting for connections')
            connection, address = sock.accept()
            logging.info(f'Connection accepted from: {address}')

            brew_id, beer_temp, ambient_temp, heater_current_state, cooler_current_state = Server.__receive_message(connection)

            # Decision module will tell us whether the heater needs to be turned on or off.
            # But, together with that we'll send the temp ranges to the controller.
            # This will ensure that the controller will be able to maintaing the temperature even if the network connection has been proken.
            heater_desired_state, cooler_desired_state, min_temp, max_temp = self.__decision_module.get_desired_state(brew_id, beer_temp, ambient_temp, heater_current_state, cooler_current_state)
            self.__temp_logger.log(brew_id, beer_temp, ambient_temp, heater_current_state, heater_desired_state, cooler_current_state, cooler_desired_state)

            Server.__send_message(connection, brew_id, heater_desired_state, cooler_desired_state, min_temp, max_temp)
            connection.close()

    @staticmethod
    def __receive_message(sock: socket):
        received_bytes = 0
        chunks = []
        while received_bytes < rcv_msg_size:
            chunk = sock.recv(rcv_msg_size - received_bytes)
            chunks.append(chunk)
            received_bytes = received_bytes + len(chunk)

        # Message comes in the following binary format and the byte order is little-endian
        # |--brew id--|--beer temp--|--ambient temp--|--heater state--|--cooler state--|
        # |--4 bytes--|--4 bytes----|--4 bytes-------|--2 bytes-------|--2 bytes-------|
        # |--integer--|--float------|--float---------|--bool----------|--bool----------|
        brew_id, beer_temp, ambient_temp, heater_state, cooler_state = struct.unpack('<IffHH', b''.join(chunks))
        return (int(brew_id), float(beer_temp), float(ambient_temp), bool(heater_state), bool(cooler_state))

    @staticmethod
    def __send_message(sock, brew_id: int, heater_state: bool, cooler_state: bool, min_temp: float, max_temp: float):
        # Response is sent back to the controller in the following binary format and the byte order is little-endian
        # |--brew id--|--min temp--|--max temp--|--heater state--|--cooler state--|
        # |--4 bytes--|--4 bytes---|--4 bytes---|--2 bytes-------|--2 bytes-------|
        # |--integer--|--float-----|--float-----|--bool----------|--bool----------|
        msg = struct.pack('<IffHH', brew_id, min_temp, max_temp, heater_state, cooler_state)
        sock.sendall(msg)