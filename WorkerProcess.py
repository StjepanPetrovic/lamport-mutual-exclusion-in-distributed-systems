import socket
from multiprocessing import Process


class WorkerProcess:
    def __init__(self, port, clock, time_to_work):
        self.port = port
        self.clock = clock
        self.time_to_work = time_to_work
        self.process = Process(target=self.work)
        self.process.start()
        self.socket = self.create_server_socket()

    def work(self):
        while True:
            data, _ = self.socket.recvfrom(4096)

    def join(self):
        self.process.join()

    def create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', self.port)
        server_socket.bind(server_address)

        return server_socket
