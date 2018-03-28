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

@app.route('/')
def index_page():
    return "Hello World"

@app.route('/nodes')
def nodes_page():
    nodes = database.retrieve_all_nodes()
    node_objects = []
    for node in nodes:
        current_node = Node(node[0], node[1], node[2])
        node_objects.append(current_node)

    return jsonify(node_objects)

@app.route('/message')
def messages_page():
    rows = database.retrieve_all_messages()
    messages = []
    for row in rows:
        message = database_parser.convert_to_message(row)
        messages.append(message)
    
    return jsonify(messages)

@app.route('/message/<sigfox_id>')
def messages_by_sigfox_id_page(sigfox_id):
    rows = database.retrieve_messages_by_sigfox_id(sigfox_id)
    messages = []
    for row in rows:
        message = database_parser.convert_to_message(row)
        messages.append(message)

    return jsonify(messages)

if __name__ == '__main__':
    app.run()