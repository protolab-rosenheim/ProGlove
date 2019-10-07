import logging
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import yaml

from proglove.opcua_stuff.opcua_server import OPCUAServer
from proglove.proglove_communicator import ProgloveCommunicator
from proglove.webserver.webserver import Webservice

if __name__ == '__main__':
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file_name = os.path.join(directory, 'conf', 'prod.yaml')

    if not os.path.exists(config_file_name):
        config_file_name = os.path.join(directory, 'conf', 'dev.yaml')
    with open(config_file_name, 'r') as ymlfile:
        config = yaml.load(ymlfile)

    root = logging.getLogger()
    if config['general']['logging_level'] == 'debug':
        root.setLevel(logging.DEBUG)
    elif config['general']['logging_level'] == 'info':
        root.setLevel(logging.INFO)
    elif config['general']['logging_level'] == 'warning':
        root.setLevel(logging.WARNING)
    elif config['general']['logging_level'] == 'error':
        root.setLevel(logging.ERROR)

    check_threads_sleep_time = 5
    opcua_server = None
    thread_list = []

    # Start proglove communicator if true
    if config['modules']['proglove']:
        proglove_com = ProgloveCommunicator(config)
        proglove_com.start_communicator()
        thread_list.append(proglove_com.thread)

    # Starting OPCUAServer if true
    #if config['modules']['opcua_server']:
    #    opcua_server = OPCUAServer(config['opcua_server']['ip_address'], config['opcua_server']['port'], True)
    #    opcua_server.start_server()
    #    thread_list.append(opcua_server.thread)

    # Start webserver if true
    if config['modules']['webserver']:
        webserver = Webservice(config, proglove_com)
        webserver.start_webservice()

    logging.info('-------------------- Proglove started --------------------')

    # Run till every thread has finished
    while thread_list:
        time.sleep(check_threads_sleep_time)
        for thread in thread_list:
            if not thread.isAlive():
                thread_list.remove(thread)
