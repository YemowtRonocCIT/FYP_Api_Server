from flask import Flask
from flask import jsonify
from buoy_api.postgres_interaction import PostgresInteraction
from buoy_api.node import Node
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





if __name__ == '__main__':
    app.run()