class Message(dict):

    def __init__(self, button_pressed, temp_sensed, vibration_sensed,
                                                 temp_value, vibration_value):
        
        dict.__init__(self, button_pressed=button_pressed, 
            temperature_sensed=temp_sensed, vibration_sensed=vibration_sensed,
            temperature_value=temp_value, vibration_value=vibration_value)
