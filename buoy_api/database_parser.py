from buoy_api.message import Message
from buoy_api.node import Node

class DatabaseParser(object):
    """
    This class will be used to convert returned data from the Database to 
    the domain level classes that will be used by the program.
    """

    def convert_to_message(self, row):
        """
        Convert a row from a messages response to the Message domain class.

        row: Single row returned from SELECT
        """
        NODE_ID_INDEX = 1
        BUTTON_PRESSED_INDEX = 2
        TEMPERATURE_INDEX = 3
        VIBRATION_INDEX = 4
        TEMPERATURE_SENSED_INDEX = 5
        VIBRATION_SENSED_INDEX = 6
        TIME_INDEX = 7

        message = Message(row[BUTTON_PRESSED_INDEX], row[TEMPERATURE_SENSED_INDEX],
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