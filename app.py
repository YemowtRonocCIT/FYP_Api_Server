from flask import Flask
from flask import jsonify
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
SIGFOX_ID = '<sigfox_id>/'

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