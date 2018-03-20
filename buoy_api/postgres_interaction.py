from buoy_api.database_interface import DatabaseInterface

class PostgresInteraction(DatabaseInterface):

    def __init__(self, db_name, db_user, db_password, host):
        super().__init__(db_name, db_user, db_password, host)

    def add_node(self, sigfox_id, is_active):
        sql = """INSERT INTO node (node_id, sigfox_id, active)
        VALUES (default, %s, %s)"""
        data = (sigfox_id, is_active)
        if self.execute(sql, data):
            return True
        else:
            return False

    def set_node_status(self, status, sigfox_id):
        sql = """UPDATE node
        SET active = %s
        WHERE sigfox_id = %s"""
        data = (status, sigfox_id)
        if self.execute(sql, data):
            return True
        else:
            return False

    def remove_node(self, sigfox_id):
        sql = """DELETE FROM node
        WHERE sigfox_id = %s"""
        data = (sigfox_id)
        if self.execute(sql, data):
            return True
        else:
            return False

    def retrieve_all_nodes(self):
        sql =  """SELECT node_id, sigfox_id, active
        FROM node"""
        rows = self.select(sql)
        return rows

    def retrieve_node_by_sigfox_id(self, sigfox_id):
        sql = """SELECT node_id, sigfox_id AS s_id, active
        FROM node
        WHERE s_id = %s"""
        data = (sigfox_id)
        rows = self.select(sql, data)
        return rows

    def add_message(self, node_id, button_pressed, temperature, vibration):
        sql = """INSERT INTO messages(message_id, node_id, button_pressed, temperature, vibration) 
        VALUES (default, %s, %s, %s, %s)"""
        data = (node_id, button_pressed, temperature, vibration)
        if self.execute(sql, data):
            return True
        else:
            return False