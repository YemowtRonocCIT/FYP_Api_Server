class Buoy(dict):

    def __init__(self, buoy_id, at_location, time_checked):
        dict.__init__(self, buoy_id=buoy_id, at_location=at_location, 
                                            time_checked=time_checked)