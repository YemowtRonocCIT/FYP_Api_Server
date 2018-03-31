from buoy_api.database.postgres_interface import PostgresInterface

class PostgresInteraction(PostgresInterface):

    def __init__(self, db_name, db_user, db_password, host):
        """
        Constructor for PostgresInteraction class. It requires the details to
        connect to the database, and will use the PostgresInterface() class
        to simplify interactions.

        db_name (str): The name of the database that will be used
        db_user (str): The username to connect to the database, to allow the 
        correct permissions to each user of the database.
        db_password (str): The password to authenticate the users access to the
        database.
        host (str): IP address of database system, to allow remote connections
        """
        super().__init__(db_name, db_user, db_password, host)

    def add_node(self, sigfox_id, is_active):
        """
        Inserts a node into the database, with the given sigfox ID and status.

        sigfox_id (str): Given Sigfox ID, to identify the node
        is_active (bool): True if the node is currently being listened for,
        False if the node is disabled.
        """
        sql = """INSERT INTO node (node_id, sigfox_id, active)
        VALUES (default, %s, %s)
        ON CONFLICT (sigfox_id) DO UPDATE
        SET active = %s"""
        data = (sigfox_id, is_active, is_active)
        if self.execute(sql, data):
            return True
        else:
            return False

    def set_node_status(self, status, sigfox_id):
        """
        Change the status of the node with the given Sigfox ID.

        status (bool): Status of the node.
        sigfox_id (str): Given sigfox ID for node.
        """
        sql = """UPDATE node
        SET active = %s
        WHERE sigfox_id = %s"""
        data = (status, sigfox_id)
        if self.execute(sql, data):
            return True
        else:
            return False

    def remove_node(self, sigfox_id):
        """
        Removes the node from the database with the given Sigfox ID.

        sigfox_id (str): Given Sigfox ID for the node
        """
        sql = """DELETE FROM node
        WHERE sigfox_id = %s;"""
        data = (sigfox_id, )
        if self.execute(sql, data):
            return True
        else:
            return False

    def retrieve_all_nodes(self):
        """
        Gets all nodes from the database.
        """
        sql =  """SELECT node_id, sigfox_id, active
        FROM node"""
        rows = self.select(sql)
        return rows

    def retrieve_node_by_sigfox_id(self, sigfox_id):
        """
        Retrieves specific node from database with given Sigfox ID.

        sigfox_id (str): Given sigfox ID
        """
        sql = """SELECT node_id, sigfox_id AS s_id, active
        FROM node
        WHERE sigfox_id = %s"""
        data = (sigfox_id, )
        rows = self.select(sql, data)
        return rows

    def add_latest_message(self, node_id, button_pressed, temperature_sensed, 
                                vibration_sensed, temperature, vibration):
        """
        Adds message details to database. The details of each sensor are 
        decoded before being inserted into the database.

        node_id (int): ID of node as given by the database
        button_pressed (bool): True if the button is currently being pressed
        temperature (character): Encoded character value to be converted
        vibration (character): Encoded character value to be converted
        """
        sql = """INSERT INTO last_message(node_id, button_press, 
            temp_sensed, vib_sensed, temperature, vibration, 
            time_entered) 
        VALUES (%s, %s, %s, %s, %s, %s, time.now())
        ON CONFLICT (node_id) DO UPDATE
        SET button_press = %s,
            temp_sensed = %s,
            vib_sensed = %s,
            temperature = %s,
            vibration = %s
            time_entered = time.now()"""
        data = (node_id, button_pressed, temperature, vibration,
                button_pressed, temperature, vibration, button_pressed, 
                temperature, vibration, button_pressed, temperature, vibration)
        if self.execute(sql, data):
            return True
        else:
            return False

    def retrieve_all_latest_messages(self):
        """
        Retrieves all messages from the database
        """
        sql = """SELECT m.node_id, m.button_press, 
            m.temperature, m.vibration, m.temp_sensed, 
            m.vib_sensed, m.time_entered
        FROM last_message AS m, node
        WHERE m.node_id = node.node_id
        ORDER BY m.time_entered ASC;
        """
        rows = self.select(sql)
        return rows

    def retrieve_latest_message_by_sigfox_id(self, sigfox_id):
        """
        Retrieves all messages from the database that are linked to the given
        sigfox_id

        sigfox_id (str): ID as given by sigfox
        """
        sql = """SELECT m.node_id, m.button_press, m.temperature, m.vibration, 
            m.temp_sensed, m.vib_sensed, m.time_entered
        FROM last_message AS m, node
        WHERE m.node_id = node.node_id
        AND node.sigfox_id = %s"""
        data = (sigfox_id, )
        rows = self.select(sql, data)
        return rows

    def retrieve_all_locations(self):
        """
        Retrieves all locations from the database
        """
        sql = """SELECT location_id, location_name, location_type
        FROM location;
        """
        rows = self.select(sql)
        return rows

    def add_location(self, location_name, location_type):
        """
        Adds location to database using the given parameters

        location_name (str): Name of the location
        location_type (str): Type of location (Urban, rural, etc.) 
        """
        sql = """INSERT INTO location (location_id, location_name, location_type)
        VALUES (default, %s, %s)
        """
        data = (location_name, location_type)
        if self.execute(sql, data):
            return True
        else:
            return False

    def retrieve_all_buoys(self):
        """
        Retrieve all buoys from the database
        """
        sql = """SELECT buoy_id, at_location, time_checked
        FROM buoy"""
        rows = self.select(sql)
        return rows

    def add_buoy(self, is_there):
        """
        Adds a buoy to the database with the given parameters

        is_there (bool): Indicates if a buoy is on location
        """
        sql = """INSERT INTO buoy (buoy_id, at_location, time_checked)
        VALUES (default, %s, current_timestamp)"""
        data = (is_there, )
        if self.execute(sql, data):
            return True
        else:
            return False