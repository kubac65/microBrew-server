import socket
import logging

listen_port = 52400

class Server(object):
    def __init__(self, temp_logger, temp_range, decision_module):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__listen = False
        self.__temp_range = temp_range
        self.__temp_logger = temp_logger
        self.__decision_module = decision_module

    def start(self):
        self.__sock.bind(('', listen_port))
        self.__sock.listen(1)
        self.__listen = True

        while self.__listen:
            connection, client_address = self.__sock.accept()
            logging.info('Controller connection accepted')


            received_msg = []
            continue_reading = True
            while continue_reading:
                data = connection.recv(16)
                if data:
                    received_msg.append(data)
                else:
                    temp = b''.join(received_msg).decode('utf-8')
                    self.__temp_logger.log(temp)
                    logging.info(f'Reported temperature: {temp}')

                    # Send to decision module
                    heater_on = self.__decision_module.get_heater_desired_state(temp)
                    min_temp = self.__temp_range.min()
                    max_temp = self.__temp_range.max()
                    msg = f'{heater_on},{min_temp},{max_temp}'

                    # Send response (heating on/off)
                    connection.send(msg.encode('utf-8'))
                    logging.debug(f'Controller response: {msg}')

                    continue_reading = False
    def stop(self):
        self.__listen = False