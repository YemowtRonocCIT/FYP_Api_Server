from buoy_api.json_model.message import LatestMessage, Message
from buoy_api.json_model.node import Node
from buoy_api.json_model.location import Location
from buoy_api.json_model.buoy import Buoy

class DatabaseParser(object):
    """
    This class will be used to convert returned data from the Database to 
    the domain level classes that will be used by the program.
    """

    def convert_to_latest_message(self, row):
        """
        Convert a row from a latest message response to the LatestMessage domain class.

        row: Single row returned from SELECT
        """
        NODE_ID_INDEX = 0
        BUTTON_PRESSED_INDEX = 1
        TEMPERATURE_INDEX = 2
        VIBRATION_INDEX = 3
        TEMPERATURE_SENSED_INDEX = 4
        VIBRATION_SENSED_INDEX = 5
        TIME_INDEX = 6

        message = LatestMessage(row[BUTTON_PRESSED_INDEX], row[TEMPERATURE_SENSED_INDEX],
            row[VIBRATION_SENSED_INDEX], row[TEMPERATURE_INDEX], 
            row[VIBRATION_INDEX], row[NODE_ID_INDEX], row[TIME_INDEX])

        return message

    def convert_to_node(self, row):
        """
        Convert a row from a node response to the Node domain class.

        row: Single row returned from SELECT
        """
        NODE_ID_INDEX = 0
        SIGFOX_ID_INDEX = 1
        ACTIVE_INDEX = 2

        node = Node(row[NODE_ID_INDEX], row[SIGFOX_ID_INDEX], row[ACTIVE_INDEX])

        return node

    def convert_to_location(self, row):
        """
        Convert a row from a location response to the location domain class.

        row: Single row returned from SELECT
        """
        ID_INDEX = 0
        NAME_INDEX = 1
        TYPE_INDEX = 2

        location = Location(row[ID_INDEX], row[NAME_INDEX], row[TYPE_INDEX])

        return location

    def convert_to_buoy(self, row):
        """
        Convert a row from a buoy response to the buoy domain class.

        row: Single row returned from SELECT
        """
        ID_INDEX = 0
        IS_THERE_INDEX = 1
        TIME_INDEX = 2
        LOCATION_NAME_INDEX = 3
        LATITUDE_INDEX = 4
        LONGITUDE_INDEX = 5

        buoy = Buoy(row[ID_INDEX], row[IS_THERE_INDEX], row[TIME_INDEX], 
            row[LOCATION_NAME_INDEX], row[LATITUDE_INDEX], row[LONGITUDE_INDEX])
        
        return buoy

    def convert_to_message(self, row):
        """
        Convert a row from a message response to the message domain class.

        row: Single row returned from SELECT
        """
        NODE_ID_INDEX = 0
        MESSAGE_INDEX = 1
        TIME_INDEX = 2

        message = Message(row[NODE_ID_INDEX], row[MESSAGE_INDEX], row[TIME_INDEX])

        return message