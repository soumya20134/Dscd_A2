class Client:
    def __init__(self, curr_leader_id, nodes):
        ip = "localhost"
        port = 5000
        nodes = [] # (ip, port)
        curr_leader_id = curr_leader_id

    def send_get_request(self, key):
        # send get request to leader
        # with IP
        pass

    def send_set_request(self, key, value , term):
        # send set request to leader
        pass