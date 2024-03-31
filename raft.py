import random
class Node:
    def __init__(self,id):
        self.ID = id
        self.election_timer = None
        self.current_term = 0
        self.votedFor = None
        self.log = []
        self.commitLength = 0
        self.currentRole = "follower"
        self.currentLeader = None
        self.votesRecieved = set()
        self.sentLength = []
        self.ackedLength = [] 

    def init(self):
        # set initial election timeout
        self.set_election_timeout()

        # Check for election timeout in the background
        utils.run_thread(fn=self.on_election_timeout, args=())

        # Sync logs or send heartbeats from leader to all servers in the background
        utils.run_thread(fn=self.leader_send_append_entries, args=())


def main():
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)

    Nodes = [node1,node2,node3,node4,node5]
    