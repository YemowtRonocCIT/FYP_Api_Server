class Location(dict):

    def __init__(self, location_id, name, location_type):
        dict.__init__(self, location_id=location_id, location_name=name, location_type=location_type)