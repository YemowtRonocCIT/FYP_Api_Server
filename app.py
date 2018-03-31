from flask import Flask
from flask import jsonify
from flask import request
from buoy_api.postgres_interaction import PostgresInteraction
from buoy_api.node import Node
from buoy_api.message import Message
from buoy_api.database_parser import DatabaseParser
from login_details import DB_USER, DB_NAME, DB_PASSWORD, HOST

app = Flask(__name__)
database = PostgresInteraction(DB_NAME, DB_USER, DB_PASSWORD, HOST)
database_parser = DatabaseParser()

NODE_SUFFIX = '/node/'
LAST_MESSAGE_SUFFIX = '/last_message/'
LOCATION_SUFFIX = '/location/'
BUOY_SUFFIX = '/buoy/'

SIGFOX_ID = '<sigfox_id>/'

SIGFOX_ID_KEY = 'sigfox_id'

LOCATION_NAME_KEY = 'location_name'
LOCATION_TYPE_KEY = 'location_type'

@app.route('/', methods=['GET'])
def index_page():
    return "Hello World"

@app.route(NODE_SUFFIX, methods=['GET'])
def nodes_page():
    rows = database.retrieve_all_nodes()
    nodes = []
    for row in rows:
        node = database_parser.convert_to_node(row)
        nodes.append(node)

    return jsonify(nodes)

@app.route(NODE_SUFFIX, methods=['POST'])
def add_nodes():
    value = "False"
    sigfox_id = request.form.get(SIGFOX_ID_KEY)
    if sigfox_id is not None:
        if database.add_node(sigfox_id, True):
            value = "True"
    
    return value

@app.route(LOCATION_SUFFIX, methods=['GET'])
def locations():
    rows = database.retrieve_all_locations()
    locations = []
    for row in rows:
        location = database_parser.convert_to_location(row)
        locations.append(location)

    return jsonify(locations)

@app.route(LOCATION_SUFFIX, methods=['POST'])
def add_location():
    value = "False"
    location_name = request.form.get(LOCATION_NAME_KEY)
    location_type = request.form.get(LOCATION_TYPE_KEY)

    if location_name is not None and location_type is not None:
        if database.add_location(location_name, location_type):
            value = "True"
        
    return value

@app.route(BUOY_SUFFIX, methods=['GET'])
def get_buoys():
    rows = database.retrieve_all_buoys()
    buoys = []
    for row in rows:
        buoy = database_parser.convert_to_buoy(row)
        buoys.append(buoy)

    return jsonify(buoys)

@app.route(LAST_MESSAGE_SUFFIX, methods=['GET'])
def messages_page():
    rows = database.retrieve_all_latest_messages()
    messages = []
    for row in rows:
        message = database_parser.convert_to_message(row)
        messages.append(message)
    
    return jsonify(messages)

@app.route(LAST_MESSAGE_SUFFIX + SIGFOX_ID, methods=['GET'])
def messages_by_sigfox_id_page(sigfox_id):
    rows = database.retrieve_latest_message_by_sigfox_id(sigfox_id)
    messages = []
    for row in rows:
        message = database_parser.convert_to_message(row)
        messages.append(message)

    return jsonify(messages)

if __name__ == '__main__':
    app.run()