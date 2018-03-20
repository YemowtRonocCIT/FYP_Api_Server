class Node(dict):

    def __init__(self, id, sigfox_id, active):
        self.id = id
        self.sigfox_id = sigfox_id
        self.active = active
        dict.__init__(self, id=self.id, sigfox_id=self.sigfox_id, active=self.active)

    