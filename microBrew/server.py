import socket
import logging
import struct

rcv_msg_size = 16
listen_port = 52100

class Server(object):
    def __init__(self, temp_logger, decision_module):
        self.__temp_logger = temp_logger
        self.__decision_module = decision_module

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', listen_port))
        sock.listen(1)

        while True:
            logging.info('Waiting for connections')
            connection, address = sock.accept()
            logging.info(f'Connection accepted from: {address}')

            brew_id, beer_temp, ambient_temp, heater_state, cooler_state = Server.__receive_message(connection)

            # Decision module will tell us whether the heater needs to be turned on or off.
            # But, together with that we'll send the temp ranges to the controller.
            # This will ensure that the controller will be able to maintaing the temperature even if the network connection has been proken.
            desired_heater_state, min_temp, max_temp = self.__decision_module.get_desired_state(brew_id, float(beer_temp), float(ambient_temp), bool(heater_state))
            self.__temp_logger.log(brew_id, beer_temp, ambient_temp, bool(heater_state), desired_heater_state)

            Server.__send_message(connection, brew_id, desired_heater_state, False, min_temp, max_temp)
            connection.close()

    @staticmethod
    def __receive_message(sock):
        received_bytes = 0
        chunks = []
        while received_bytes < rcv_msg_size:
            chunk = sock.recv(rcv_msg_size - received_bytes)
            chunks.append(chunk)
            received_bytes = received_bytes + len(chunk)

        # Message comes in in the following binary format and the byte order is little-endian
        # |--brew id--|--beer temp--|--ambient temp--|--heater state--|--cooler state--|
        # |--4 bytes--|--4 bytes----|--4 bytes-------|--2 bytes-------|--2 bytes-------|
        # |--integer--|--float------|--float---------|--bool----------|--bool----------|
        brew_id, beer_temp, ambient_temp, heater_state, cooler_state = struct.unpack('<IffHH', b''.join(chunks))
        return (str(brew_id), float(beer_temp), float(ambient_temp), bool(heater_state), bool(cooler_state))

    @staticmethod
    def __send_message(sock, brew_id, heater_state, cooler_state, min_temp, max_temp):
        # Message comes in in the following binary format and the byte order is little-endian
        # |--brew id--|--heater state--|--cooler state--|--min temp--|--max temp--|
        # |--4 bytes--|--2 bytes-------|--2 bytes-------|--4 bytes---|--4 bytes---|
        # |--integer--|--bool----------|--bool----------|--float-----|--float-----|
        msg = struct.pack('<IHHff', int(brew_id), heater_state, cooler_state, min_temp, max_temp)
        sock.sendall(msg)