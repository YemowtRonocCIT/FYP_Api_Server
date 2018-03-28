class Node(dict):

    def __init__(self, id, sigfox_id, active):
        dict.__init__(self, id=id, sigfox_id=sigfox_id, active=active)

    