import logging
import time

from opcua import Client


class OPCUAClient:
    @staticmethod
    def illuminate_all(opcua_url, color, duration_sec):
        try:
            client = Client(opcua_url)
            client.connect()
            root_node = client.get_root_node()

            illuminate_all = root_node.get_child(['0:Objects', '3:art_net', '3:node_1_illuminate_all'])

            if illuminate_all:
                root_node.call_method(illuminate_all, color)
            else:
                logging.error('Could not find illuminate_all method on opcua server')

            time.sleep(duration_sec)

            all_off = root_node.get_child(['0:Objects', '3:art_net', '3:node_1_all_off'])
            if all_off:
                root_node.call_method(all_off)
            else:
                logging.error('Could not find all_off method on opcua server')
        except Exception as e:
            logging.error('Error while illuminate_all/all_off: {}'.format(e))
        finally:
            client.disconnect()

    @staticmethod
    def send_barcode(opcua_url, part_number, node):
        try:
            client = Client(opcua_url)
            client.connect()
            root_node = client.get_root_node()

            all_off = root_node.get_child(['0:Objects', '3:art_net', '3:node_1_all_off'])
            if all_off:
                root_node.call_method(all_off)
            else:
                logging.error('Could not find all_off method on opcua server')

            # Sleep, otherwise the led gets turned on and then off sometimes -> timing problem with upd packets?
            time.sleep(0.5)

            method_to_call = root_node.get_child(node)
            if method_to_call:
                res_call = root_node.call_method(method_to_call, part_number)
                return res_call
            else:
                return False
        except Exception as e:
            logging.ERROR("Error while send_barcode: {0}".format(e))
        finally:
            client.disconnect()
