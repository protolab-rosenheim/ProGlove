from threading import Thread
import logging
import json

import serial
import requests
from proglove.opcua_stuff.opcua_client import OPCUAClient


class ProgloveCommunicator:
    def __init__(self, config):
        self.config = config
        self.thread_run_ok = True
        self.thread = Thread(target=self._run_communication, args=())
        self.last_data = {}
        self.scan_count = 0
        self.location = None
        self.partnumber = -1

    def _run_communication(self):
        try:
            ser = serial.Serial(self.config['proglove']['com_port'])
        except Exception as e:
            logging.critical('Error: {}'.format(e))
        else:
            logging.info('ProgloveCommunicator thread started')
            while self.thread_run_ok:
                line = ser.readline().decode("utf-8")
                try:
                    data = json.loads(line)
                except ValueError:
                    logging.error('Received data is no valid json')
                    continue
                logging.debug('Got data: {}'.format(data))

                if isinstance(data, list):
                    logging.debug('Received data is a list - nothing implemented yet')
                elif isinstance(data, dict):
                    logging.debug('Received data is a dict')

                    # Check-in proglove on machine/zelle
                    if data['action'] == 'check-in' and data['device'] == 'proglove' and data['location'] is not None:
                        self.last_data = data
                        self.scan_count += 1
                        self.location = data['location']
                        logging.info('Checked proglove in at location {}'.format(self.location))
                    # Check-in/out devices like irk in location
                    elif data['action'] == 'check-in_check-out' and data['device'] is not None:
                        self.last_data = data
                        self.scan_count += 1
                        # Get current location from carriage
                        r = requests.get('http://' + data['device'] + ':5000/api/v1/carriage')
                        if r.status_code not in range(200, 300):
                            raise Exception('Get request failed with status code ' + str(r.status_code))

                        device = r.json()['objects'][0]
                        if device['current_location'] == self.location:
                            device['current_location'] = 'na'
                        else:
                            device['current_location'] = self.location

                        # Update carriage
                        r = requests.put('http://' + data['device'] + ':5000/api/v1/carriage/1', json=device)
                        if r.status_code not in range(200, 300):
                            raise Exception('Put request failed with status code ' + str(r.status_code))
                        else:
                            opcua_url = 'opc.tcp://' + data['device'] + ':4840/'
                            OPCUAClient.illuminate_all(opcua_url, 'green', 3)

                elif isinstance(data, int):
                    self.partnumber = int(data)
                    logging.debug('Received data is an int')
                    try:
                        OPCUAClient.send_barcode('opc.tcp://' + str(self.config['con_container']['hostname']) + ':' +
                                                 str(self.config['con_container']['port']) + '/',
                                                 int(data),
                                                 ['0:Objects', '2:iot_ready_kit', '2:find_part'])
                    except:
                        logging.error('OPCUA Connection to host' + str(self.config['con_container']['hostname']) +
                                      'with port' + str(self.config['con_container']['port']) +
                                      'could not be established')

            ser.close()

    def start_communicator(self):
        self.thread_run_ok = True
        self.thread.start()

    def stop_communication(self):
        self.thread_run_ok = False
