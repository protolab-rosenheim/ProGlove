import datetime
import time

import flask
from flask import request, jsonify, abort
from flask_cors import CORS


class Webservice:
    def __init__(self, config, proglove_com):
        self.config = config
        self.proglove_com = proglove_com

    def start_webservice(self):
        # Create the Flask application
        app = flask.Flask(self.config['webserver']['name'])
        app.config['DEBUG'] = bool(self.config['webserver']['debug'])

        api_version_string = '/api/v1'

        @app.route(api_version_string + '/setlocation', methods=['POST'])
        def set_location():
            api_call_params = request.get_json()

            if 'location' in api_call_params:
                location = api_call_params['location']
            else:
                location = None

            try:
                self.proglove_com.last_data['location'] = location

            except Exception as e:
                abort(500)

            finally:
                return jsonify(
                    status=200
                )

        @app.route(api_version_string + '/lastaction', methods=['GET'])
        def get_lastaction():
            # Timeout for longpolling requests in ms
            lp_timeout = request.args.get('lpTimeout')

            result_json = self.proglove_com.last_data

            if lp_timeout:
                lp_exp_timestamp = datetime.datetime.now() + datetime.timedelta(milliseconds=int(lp_timeout))
                proglove_counter = self.proglove_com.scan_count
                # While not reached timeout for long polling, check every 0.2 seconds for new data
                while datetime.datetime.now() < lp_exp_timestamp:
                    if proglove_counter < self.proglove_com.scan_count:
                        result_json = self.proglove_com.last_data
                        break

                    time.sleep(0.2)

            return jsonify(
                num_results=1,
                objects=result_json,
                page=1,
                total_pages=1
            )

        @app.route(api_version_string + '/reorder', methods=['GET'])
        def get_reorder():
            result_json = self.proglove_com.partnumber
            self.proglove_com.partnumber =-1
            return jsonify(
                num_results=1,
                objects=result_json,
                page=1,
                total_pages=1
            )


        cors = CORS(app)

        # start the flask loop
        app.run(host=self.config['webserver']['hostname'], port=int(self.config['webserver']['port']), threaded=True)
