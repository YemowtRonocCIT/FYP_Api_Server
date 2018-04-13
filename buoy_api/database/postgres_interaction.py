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
        NODE_ID_INDEX = 0

        value = True

        node_id = None
        rows = self.retrieve_node_by_sigfox_id(sigfox_id)
        for row in rows:
            node_id = row[NODE_ID_INDEX]

        sql = """DELETE FROM node
        WHERE sigfox_id = %s;"""
        data = (sigfox_id, )
        if not self.execute(sql, data):
            value = False

        sql = """DELETE FROM node_buoy
        WHERE node_id = %s"""
        data = (node_id, )
        if value == True and node_id is not None:
            if not self.execute(sql, data):
                value = False
        
        return value

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
    
    def retrieve_node_by_buoy_id(self, buoy_id):
        """
        Retrieves specific node from database which is attached to the buoy
        with the given ID

        buoy_id (int): ID of buoy as given by the database
        """
        sql = """SELECT n.node_id, n.sigfox_id, n.active
        FROM node AS n, node_buoy AS nb
        WHERE nb.buoy_id = %s
        AND nb.node_id = n.node_id"""
        data = (buoy_id, )
        rows = self.select(sql, data)
        return rows

    def retrieve_latest_node_id(self):
        """
        Retrieves the latest node_id which was added to the system. This
        can be used to find the most recently added node.
        """
        sql = """SELECT MAX(node_id)
        FROM node"""
        rows = self.select(sql)
        for row in rows:
            node_id = row[0]
        
        return node_id

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

    def retrieve_location_by_name(self, name):
        """
        Retrieves locations from database with the matching name parameter

        name (str): Name of the location
        """
        sql = """SELECT location_id, location_name, location_type
        FROM location
        WHERE location_name = %s"""
        data = (name, )
        rows = self.select(sql, data)
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
        
    def remove_location(self, location_id):
        """
        Removes location from database with given location ID

        location_id (int): ID given to location by database
        """
        BUOY_ID_INDEX = 0

        value = True

        buoy_ids = []
        rows = self.retrieve_buoys_by_location_id(location_id)
        for row in rows:
            buoy_ids.append(row[BUOY_ID_INDEX])
        
        for buoy_id in buoy_ids:
            self.remove_buoy_by_id(buoy_id)

        sql = """DELETE FROM location
        WHERE location_id = %s"""
        data = (location_id, )
        if not self.execute(sql, data):
            value = False

        if value == True:
            sql = """DELETE FROM buoy_location
            WHERE location_id = %s"""
            if not self.execute(sql, data):
                value = False
            
        return value

    def retrieve_all_buoys(self):
        """
        Retrieve all buoys from the database. This will also retrieve the 
        name of the location where it is along with the GPS co ordinates of 
        the exact location of the buoy.
        """
        sql = """SELECT b.buoy_id, b.at_location, b.time_checked, l.location_name, 
            bl.latitude, bl.longitude
        FROM buoy AS b, location AS l, buoy_location AS bl
        WHERE b.buoy_id = bl.buoy_id
        AND bl.location_id = l.location_id"""
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

    def remove_buoy_by_id(self, buoy_id):
        """
        Removes buoy with given buoy ID from the database

        buoy_id (int): ID of buoy to be deleted
        """
        SIGFOX_ID_INDEX = 1

        working = True

        sigfox_id = None
        rows = self.retrieve_node_by_buoy_id(buoy_id)
        for row in rows:
            sigfox_id = row[SIGFOX_ID_INDEX]
        
        if sigfox_id is not None:
            if not self.set_node_status(False, sigfox_id):
                working = False

        if working == True:
            sql = """DELETE FROM buoy
            WHERE buoy_id = %s"""
            data = (buoy_id, )
            if not self.execute(sql, data):
                working = False
        
        if working == True:
            sql = """DELETE FROM buoy_location
            WHERE buoy_id = %s"""
            if not self.execute(sql, data):
                working = False
        
        if working == True:
            sql = """DELETE FROM node_buoy
            WHERE buoy_id = %s"""
            if not self.execute(sql, data):
                working = False

        return working
    
    def update_buoy_checked(self, buoy_id):
        """
        Updates the latest time checked on buoy with given ID

        buoy_id (int): ID given to buoy by database
        """
        sql = """UPDATE buoy
        SET time_checked = current_timestamp
        WHERE buoy_id = %s"""
        data = (buoy_id, )
        return self.execute(sql, data)

    def retrieve_buoys_by_location_id(self, location_id):
        """
        Retrieves all buoys that are connected to the given location ID

        location_id (int): ID given to the location by the database
        """
        sql = """SELECT buoy.buoy_id, at_location, time_checked, l.location_name,
            bl.latitude, bl.longitude
        FROM buoy, buoy_location AS bl, location AS l
        WHERE bl.location_id = %s
        AND buoy.buoy_id = bl.buoy_id
        AND bl.location_id = l.location_id"""
        data = (location_id, )
        rows = self.select(sql, data)
        return rows

    def retrieve_all_messages(self):
        """
        Retrieves all the messages from each node that are in the database
        """
        sql = """SELECT node_id, message_text, time_sent
        FROM message"""
        rows = self.select(sql)
        return rows

    def retrieve_messages_by_node_id(self, node_id):
        """
        Retrieve all messages from the database sent by the given node

        node_id (str): ID of node as given by the database
        """
        sql = """SELECT node_id, message_text, time_sent
        FROM message
        WHERE node_id = %s"""
        data = (node_id, )
        rows = self.select(sql,data)
        return rows

    def get_latest_buoy_id(self):
        """
        Retrieves latest added ID for a buoy from the database.
        """
        sql = """SELECT MAX(buoy_id)
        FROM buoy"""
        rows = self.select(sql)
        for row in rows:
            return row[0]

    def add_buoy_location(self, location_id, latitude, longitude, buoy_id):
        """
        Adds the relation between a buoy and a location to the buoy_location
        table

        location_id (int): Given location ID by database
        latitude (float): Latitude of buoy location
        longitude (float): Longitude of buoy location
        buoy_id (int): ID of buoy as given by the database
        """
        sql = """INSERT INTO buoy_location (location_id, buoy_id, latitude, longitude)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (buoy_id) DO UPDATE
        SET location_id = %s,
            latitude = %s,
            longitude = %s"""
        data = (location_id, buoy_id, latitude, longitude, location_id, 
                                                    latitude, longitude)
        if self.execute(sql, data):
            return True
        else:
            return False
    
    def add_buoy_node_connection(self, node_id, buoy_id):
        """
        Adds relationship between a node and a buoy to the database.

        node_id (int): Integer ID to point to a given node in the database
        buoy_id (int): Integer ID to point to a given buoy in the database
        """
        sql = """INSERT INTO node_buoy (node_id, buoy_id)
        VALUES (%s, %s)"""
        data = (node_id, buoy_id)

        if self.execute(sql, data):
            return True
        else:
            return False