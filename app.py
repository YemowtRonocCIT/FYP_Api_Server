from flask import Flask
from flask import jsonify
from buoy_api.postgres_interaction import PostgresInteraction
from buoy_api.node import Node
from buoy_api.message import Message
from login_details import DB_USER, DB_NAME, DB_PASSWORD, HOST

app = Flask(__name__)
database = PostgresInteraction(DB_NAME, DB_USER, DB_PASSWORD, HOST)

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

MESSAGE_ID_INDEX = 0
NODE_ID_INDEX = 1
BUTTON_PRESSED_INDEX = 2
TEMPERATURE_INDEX = 3
VIBRATION_INDEX = 4
TEMPERATURE_SENSED_INDEX = 5
VIBRATION_SENSED_INDEX = 6

@app.route('/message')
def messages_page():
    rows = database.retrieve_messages_by_sigfox_id('1D1BF9')
    messages = []
    for row in rows:
        message = Message(row[BUTTON_PRESSED_INDEX], row[VIBRATION_INDEX],
            row[TEMPERATURE_INDEX], row[TEMPERATURE_SENSED_INDEX], 
            row[VIBRATION_SENSED_INDEX])

        messages.append(message)

    return jsonify(messages)

if __name__ == '__main__':
    app.run()