import socket
import logging

listen_port = 52100
brew_id = 'brew-1' # Hardcoded for now

class Server(object):
    def __init__(self, temp_logger, decision_module):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__listen = False
        self.__temp_logger = temp_logger
        self.__decision_module = decision_module

    def start(self):
        self.__sock.bind(('', listen_port))
        self.__sock.listen(1)
        self.__listen = True

        while self.__listen:
            logging.info('Waiting for connections')
            connection, _ = self.__sock.accept()
            logging.info('Connection accepted')

            received_msg = []
            continue_reading = True
            while continue_reading:
                data = connection.recv(16)
                if data:
                    received_msg.append(data)
                else:
                    beer_temp, ambient_temp, heater_state = b''.join(received_msg).decode('utf-8').split(',')
                    logging.info(f'Beer temp: {beer_temp}   Ambient temp: {ambient_temp}')

                    # Decision module will tell us whether the heater needs to be turned on or off.
                    # But, together with that we'll send the temp ranges to the controller.
                    # This will ensure that the controller will be able to maintaing the temperature even if the network connection has been proken.
                    desired_heater_state, min_temp, max_temp = self.__decision_module.get_desired_state(brew_id, float(beer_temp), float(ambient_temp), bool(heater_state))
                    self.__temp_logger.log(brew_id, beer_temp, ambient_temp, bool(heater_state), desired_heater_state)
                    msg = f'{1 if desired_heater_state else 0},{min_temp},{max_temp}'

                    # Send response (heating on/off)
                    connection.send(msg.encode('utf-8'))
                    logging.debug(f'Response: {msg}')

                    continue_reading = False

    def stop(self):
        self.__listen = False