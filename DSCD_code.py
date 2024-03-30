import random
from threading import Thread
import socket
import traceback
import utils

# client sends a message to a function in main here 
# if the current node is the leafd

def run_thread(fn, args):
    my_thread = Thread(target=fn, args=args)
    my_thread.daemon = True
    my_thread.start()
    return my_thread

def wait_for_server_startup(ip, port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((str(ip), int(port)))
            return sock
                
        except Exception as e:
            traceback.print_exc(limit=1000)

class Node:
  def __init__(self,id, election_timer):
    self.ID = id
    self.election_timer = random.randint(5,10)
    self.current_term = 0
    self.votedFor = None
    self.log = []
    self.commitLength = 0
    self.currentRole = "follower"
    self.currentLeader = None
    self.votesRecieved = set()
    self.sentLength = []
    self.ackedLength = []

  # 1/9
  def RecoverCrash(self, next_node):
    self.currentRole = "follower"
    self.currentLeader = None
    self.votesRecieved = {}
    self.sentLength = []
    self.ackedLength = []
  
  def ElectLeader(self):
    self.current_term +=1
    self.currentRole = "candidate"
    self.votedFor = self.ID
    self.votesRecieved.add(self.ID)
    lastTerm = 0
    if(len(self.log) > 0):
      lastTerm = self.log[len(self.log)-1][1]
    
    # Send vote requests in parallel
    threads = []
    for j in range(5):
        if j != self.ID:
           t =  utils.run_thread(fn=self.request_vote, args=(j,))
           threads += [t]
    
    # Wait for completion of request flow
    for t in threads:
        t.join()
    
    return True
    msg = ("Vote",self.ID,self.current_term,len(self.log),lastTerm)
    for i in range(1,6):
      #use grpc to send message
      print("message sent to Node",i)
    
    # self.election_timer = set this out
      
  # 2/9
  def RecieveVote(self, VoteReg, cID,cTerm, cLogLength, cLogTerm):
        if(cTerm>self.current_term):
            self.current_term = cTerm
            self.currentRole = "follower"
            self.votedFor = None
        
        lastTerm = 0
        if(len(self.log) > 0):
            lastTerm = self.log[len(self.log)-1][1]

        logOk = (cLogTerm>lastTerm) or ((cLogTerm == lastTerm) and (cLogLength >= len(self.log)))

        if (cTerm == self.current_term and logOk and (self.votedFor == cID or self.votedFor == None)):
           self.votedFor = cID
           # send (VoteResponse, nodeId, currentTerm,true) to node cId

        else:
           #send (VoteResponse, nodeId, currentTerm, false) to node cId
           print("false")

  # 3/9
  def collect_vote(self, term, granted, voterID):
    if self.currentRole == "candidate" and self.current_term == term and granted:
        self.votesRecieved.add(voterID)
        if len(self.votesRecieved) > (5+1)/2:
            self.currentRole = "leader"
            self.currentLeader = self.ID
            # cancel election timer 
            for i in range(1,6):
               if(i == self.ID):
                  continue
               else:
                  self.sentLength[i] = len(self.log)
                  self.ackedLength[i] = 0
                  self.ReplicateLog(self.ID,i)

        elif term > self.current_term:
            self.current_term = term
            self.votedFor = None
            self.currentRole = "follower"
            # cancel election timer

  # 4/9
  def requestBroadcast(self,msg):
    if self.currentLeader == "leader":
       #append to log current term and msg
      self.ackedLength[self.ID] = len(self.log)
      for i in range(1,6):
        if(i == self.ID):
          continue
        else:
          self.ReplicateLog(self.ID,i)
    else:
       for node in nodes:
          if node.currentRole == "leader":
            node.requestBroadcast(msg)

    #periodically
    if self.currentLeader == "leader":
       for i in range(1,6):
        if(i == self.ID):
          continue
        else:
          self.ReplicateLog(self.ID,i)

  # 5/9
  def ReplicateLog(self,leaderID, followerID):
      prefixLen = self.sentLength[followerID]
      suffix = self.log[prefixLen:] 
      prefixTerm = 0
      if prefixLen > 0:
        prefixTerm = self.log[prefixLen-1][1]
#         send (LogRequest, leaderId, currentTerm, prefixLen,
#                 prefixTerm, commitLength, suffix ) to followerId


 # 6/9
  def RecieveMessage(self,LogRequest, leaderId, term, prefixLen, prefixTerm,leaderCommit, suffix):   #INCOMPLETE
       if(term>self.current_term):
          self.current_term = term
          self.votedFor = None
          # cancel election timer

       if(term == self.current_term):
          self.currentRole = "follower"
          self.currentLeader = leaderId
        
       logOk = ((len(self.log) >= prefixLen) and ((prefixLen == 0) or (self.log[prefixLen])))
       # incomplete
       if(term == self.current_term and logOk):
          self.AppendEntries(prefixLen,leaderCommit,suffix)
          ack = prefixLen + len(suffix)
          # send (LogResponse, nodeId, currentTerm, ack,true) to leaderId
       else:
          # send (LogResponse, nodeId, currentTerm, 0, false) to leaderId
          print("need to send")
  
            
  
      


  # 7/9
  def AppendEntries(self, prefixLen,LeaderCommit,suffix):
    if(len(suffix)>0 and len(self.log)>prefixLen):
      index = min(len(self.log),prefixLen + len(suffix)) -1
      if self.log[index][1] != suffix[index - prefixLen][1]:
         self.log = self.log[0:prefixLen]
    
    if (prefixLen + len(suffix)> len(self.log)):
       for i in range(len(self.log)-prefixLen, len(suffix)-1):
          self.log.append(suffix[i])
    
    if LeaderCommit > self.commitLength :
       for i in range(self.commitLength, LeaderCommit -1):
          # deliver log[i].msg to the application
          print(i)

       self.commitLength = LeaderCommit
    
  # 8/9
  def leader_recv_ack(self, follower, term, ack, success):
    if self.currentTerm == term and self.currentRole == "leader":
      if success and ack >= self.ackedLength[follower]:
        self.sentLength[follower] = ack
        self.ackedLength[follower] = ack
        self.CommitLogEntries()
      
      elif self.sentLength[follower] > 0:
        self.sentLength[follower] -= 1
        self.ReplicateLog(self.ID, follower)  

    elif term > self.currentTerm:
      self.currentTerm = term
      self.currentRole = "follower"
      self.votedFor = None
      self.currentLeader = None
      # cancel election timer

  # 9/9
  # def acks(self,length):
  #    ans = 0 
  #    for i in range(0,5):
  #       if(self.ackedLength[i]>length):
  #         ans+=1
  #    return ans
        
  # def CommitLogEntries(self):
  #    minAcks = (5+1)/2
  #    ready = set()
  #    max_ready = 0
  #    for i in range(1,len(self.log)+1):
  #       if(self.acks(i)>=minAcks):
  #          ready.add(i)
  #          max_ready = i
          
  #    if (len(ready) != 0) and (max_ready > self.commitLength) and (self.log[max_ready - 1][1] == self.current_term):

  def CommitLogEntries(self):
     while self.commitLength < len(self.log):
        acks = 0
        for i in range(1,6):
          if self.ackedLength[i] >= self.commitLength:
            acks += 1
        
        if acks > (5+1)/2:
          self.commitLength += 1
          # deliver log[commitLength].msg to the application
          print("delivered")
        else:
           break
        

class HashTable:
    def __init__(self):
        self.map = {}

    def set(self, key, value, req_id):
          if key not in self.map or self.map[key][1] < req_id:
              self.map[key] = (value, req_id)
              return 1
          return -1
    
    def get_value(self, key):
          if key in self.map:
              return self.map[key][0]
          return None


def main():
  node1 = Node()
  node2 = Node()
  node3 = Node()
  node4 = Node()
  node5 = Node()

  curr_leader = node1
  nodes = [node1,node2,node3,node4,node5]
  nodes_withIP = {node1:"IP1",node2:"IP2",node3:"IP3",node4:"IP4",node5:"IP5"}


  ourDB = HashTable()
  # get a req from Client (op,IP,key,term)
  op = "get" # just for no error - remove
  if op == "get":
    IP,key = 0,0 # just for no error - remove
    if(nodes_withIP[curr_leader]==IP):
      ourDB.get_value(key)
      print("SUCESS")
    else:
      # send the client (current_leader and failure)
      print("FAILURE")

  else:
    # get a set-req from Client (IP,key,value)
    IP,key,value,term = 0,0,0,0 # just for no error - remove
    if(nodes_withIP[curr_leader]==IP):
      ourDB.set_value(key,value,term)
      print("SUCESS")
    else:
      # send the client (current_leader and failure)
      print("FAILURE")





