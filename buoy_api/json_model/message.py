class LatestMessage(dict):

    def __init__(self, button_pressed, temp_sensed, vibration_sensed,
                                    temp_value, vibration_value, node_id, time):
        
        dict.__init__(self, button_pressed=button_pressed, 
            temperature_sensed=temp_sensed, vibration_sensed=vibration_sensed,
            temperature_value=temp_value, vibration_value=vibration_value, 
            node_id=node_id, time=time)

class Message(dict):

    def __init__(self, node_id, message_text, time_sent):
        dict.__init__(self, node_id=node_id, message=message_text, 
                                                time_sent=time_sent)
