from threading import Thread
import time
import logging
from opcua import ua, Server


class OPCUAServer:
    def __init__(self, ip_address, port, proglove_com=False):
        self.logger = logging.getLogger(__name__)
        self.proglove_com = proglove_com
        self.port = str(port)
        self.ip_address = str(ip_address)
        self.last_barcode = None
        self.thread_run_ok = True
        self.thread = Thread(target=self.server, args=())

    def server(self):
        # Now setup our server
        server = Server()
        server.set_endpoint("opc.tcp://" + self.ip_address + ":" + self.port + "/")
        server.set_server_name("Proglove OPCUA-Server")

        # Setup namespaces
        carriage_ns = server.register_namespace("carriage")
        artnet_ns = server.register_namespace("artnet")
        proglove_ns = server.register_namespace("proglove")

        if self.proglove_com:
            proglove_obj = server.nodes.objects.add_object(proglove_ns, "proglove")
            self.last_barcode = proglove_obj.add_variable(proglove_ns, "last_barcode", '-')
            #self.last_barcode = proglove_obj.get_child(["4:proglove", "4:last_barcode"])
            #carriage_obj.add_variable(carriage_ns, "carriage_status", rest_client.get_carriage().carriage_status)
            #carriage_obj.add_method(carriage_ns, "carriage_import_order_data", DataImporter.import_data_opcua_call,
            #                        [ua.VariantType.String])


        # Start server
        try:
            server.start()
            self.logger.info("opcua_stuff-Server started")

            while self.thread_run_ok:
                time.sleep(2)

            server.stop()
            self.logger.info("opcua_stuff-Server stopped")
        except OSError as e:
            self.thread_run_ok = False
            self.logger.critical("OS error: {0}".format(e))

    def start_server(self):
        self.thread_run_ok = True
        self.thread.start()

    def stop_server(self):
        self.thread_run_ok = False
