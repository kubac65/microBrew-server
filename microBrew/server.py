import socket
import logging

listen_port = 52100
brew_id = 'brew-1' # Hardcoded for now

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

            while True:
                data = connection.recv(1024)
                if not data:
                    break

                beer_temp, ambient_temp, heater_state = data.decode('ascii').split(',')
                logging.info(f'Beer temp: {beer_temp}')
                logging.info(f'Ambient temp: {ambient_temp}')

                # Decision module will tell us whether the heater needs to be turned on or off.
                # But, together with that we'll send the temp ranges to the controller.
                # This will ensure that the controller will be able to maintaing the temperature even if the network connection has been proken.
                desired_heater_state, min_temp, max_temp = self.__decision_module.get_desired_state(brew_id, float(beer_temp), float(ambient_temp), bool(heater_state))
                self.__temp_logger.log(brew_id, beer_temp, ambient_temp, bool(heater_state), desired_heater_state)

                rsp = f'{1 if desired_heater_state else 0},{min_temp},{max_temp}'.encode('ascii')
                connection.sendall(rsp)

            connection.close()