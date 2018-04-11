from flask import Flask
from flask import jsonify
from flask import request
from buoy_api.database.postgres_interaction import PostgresInteraction
from buoy_api.database.database_parser import DatabaseParser
from buoy_api.website_input.buoy_input import BuoyInput
from login_details import DB_USER, DB_NAME, DB_PASSWORD, HOST

app = Flask(__name__)
database = PostgresInteraction(DB_NAME, DB_USER, DB_PASSWORD, HOST)
database_parser = DatabaseParser()

NODE_SUFFIX = '/node/'
LAST_MESSAGE_SUFFIX = '/last_message/'
MESSAGE_SUFFIX = '/message/'
LOCATION_SUFFIX = '/location/'
BUOY_SUFFIX = '/buoy/'

SIGFOX_ID = '<sigfox_id>/'
NODE_ID = '<node_id>/'
LOCATION_ID = '<location_id>/'
BUOY_ID = '<buoy_id>/'

SIGFOX_ID_KEY = 'sigfox_id'
BUOY_ID_KEY = 'buoy_id'

LOCATION_NAME_KEY = 'location_name'
LOCATION_TYPE_KEY = 'location_type'

BUOY_THERE_KEY = 'at_location'

LATITUDE_KEY = 'latitude'
LONGITUDE_KEY = 'longitude'
BUOY_LOCATION_KEY = 'buoy_location'
LOCATION_ID_KEY = 'location_id'

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
    buoy_id = request.form.get(BUOY_ID_KEY)
    if sigfox_id is not None:
        if database.add_node(sigfox_id, True):
            value = "True"
        
        if buoy_id is not None:
            node_id = database.retrieve_latest_node_id()
            if database.add_buoy_node_connection(node_id, buoy_id):
                value += "Add buoy/node connection"
    
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

@app.route(MESSAGE_SUFFIX, methods=['GET'])
def messages():
    rows = database.retrieve_all_messages()
    messages = []
    for row in rows:
        message = database_parser.convert_to_message(row)
        messages.append(message)
    
    return jsonify(messages)

@app.route(MESSAGE_SUFFIX + NODE_ID, methods=['GET'])
def messages_by_node_id(node_id):
    rows = database.retrieve_messages_by_node_id(node_id)
    messages = []
    for row in rows:
        message = database_parser.convert_to_message(row)
        messages.append(message)

    return jsonify(messages)

@app.route(BUOY_SUFFIX, methods=['GET'])
def get_buoys():
    rows = database.retrieve_all_buoys()
    buoys = []
    for row in rows:
        buoy = database_parser.convert_to_buoy(row)
        buoys.append(buoy)

    return jsonify(buoys)

@app.route(BUOY_SUFFIX, methods=['POST'])
def add_buoy():
    value = "Not added"
    is_there = request.form.get(BUOY_THERE_KEY)
    buoy_input = BuoyInput()

    is_there = buoy_input.convert_yes_no_boolean(is_there)
    
    latitude = request.form.get(LATITUDE_KEY)
    latitude = buoy_input.convert_to_coordinate(latitude)

    longitude = request.form.get(LONGITUDE_KEY)
    longitude = buoy_input.convert_to_coordinate(longitude)

    location_name = request.form.get(BUOY_LOCATION_KEY)

    if (location_name is not None) and (is_there is not None) and \
        (latitude is not None) and (longitude is not None):
        rows = database.retrieve_location_by_name(location_name)
        for row in rows:
            location = database_parser.convert_to_location(row)
            location_id = location[LOCATION_ID_KEY]    

        if is_there is not None:
            if database.add_buoy(is_there):
                value = "Added Buoy"

        buoy_id = database.get_latest_buoy_id()    
        if database.add_buoy_location(location_id, latitude, longitude, buoy_id):
            value += "Added buoy location"
    
    return value

@app.route(BUOY_SUFFIX + BUOY_ID, methods=['DELETE'])
def remove_node(buoy_id):
    result = "Not Deleted"
    if database.remove_buoy_by_id(buoy_id):
        result = "Deleted"
    
    return result        

@app.route(LAST_MESSAGE_SUFFIX, methods=['GET'])
def messages_page():
    rows = database.retrieve_all_latest_messages()
    messages = []
    for row in rows:
        message = database_parser.convert_to_latest_message(row)
        messages.append(message)
    
    return jsonify(messages)

@app.route(LAST_MESSAGE_SUFFIX + SIGFOX_ID, methods=['GET'])
def messages_by_sigfox_id_page(sigfox_id):
    rows = database.retrieve_latest_message_by_sigfox_id(sigfox_id)
    messages = []
    for row in rows:
        message = database_parser.convert_to_latest_message(row)
        messages.append(message)

    return jsonify(messages)


@app.route(BUOY_SUFFIX + LOCATION_ID, methods=['GET'])
def buoys_by_location_id(location_id):
    rows = database.retrieve_buoys_by_location_id(location_id)
    buoys = []
    for row in rows:
        buoy = database_parser.convert_to_buoy(row)
        buoys.append(buoy)

    return jsonify(buoys)
        
        
if __name__ == '__main__':
    app.run()