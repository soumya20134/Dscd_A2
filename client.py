import grpc
from generated_code import client_pb2 
from generated_code import client_pb2_grpc
import concurrent.futures as futures
import logging 
import time

class ClientServiceServicer(client_pb2_grpc.ClientServiceServicer):
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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    client_pb2_grpc.add_MarketServiceServicer_to_server(ClientServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    logging.info("Market Server started. Listening on port 50051...")
    try:
        while True:
            time.sleep(86400)  # Sleep indefinitely
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
