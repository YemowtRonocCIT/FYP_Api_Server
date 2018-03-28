from buoy_api.message import Message

class DatabaseParser(object):

    def convert_to_message(self, row):
        NODE_ID_INDEX = 1
        BUTTON_PRESSED_INDEX = 2
        TEMPERATURE_INDEX = 3
        VIBRATION_INDEX = 4
        TEMPERATURE_SENSED_INDEX = 5
        VIBRATION_SENSED_INDEX = 6

        message = Message(row[BUTTON_PRESSED_INDEX], row[VIBRATION_INDEX],
            row[TEMPERATURE_INDEX], row[TEMPERATURE_SENSED_INDEX], 
            row[VIBRATION_SENSED_INDEX], row[NODE_ID_INDEX])

        return message