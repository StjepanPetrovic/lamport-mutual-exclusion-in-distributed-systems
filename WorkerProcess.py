import json
import socket
import time
from multiprocessing import Process


class WorkerProcess:
    def __init__(self, id_process, clock, times_to_critical_section, number_of_other_processes):
        self.id = id_process
        self.clock = clock
        self.times_to_critical_section = times_to_critical_section
        self.number_of_other_processes = number_of_other_processes
        self.socket = self.create_server_socket()
        self.need_to_crtical_section = False

        self.list_of_requests = []
        self.list_of_responses = []

        self.process = Process(target=self.work)
        time.sleep(2)
        self.process.start()

    def critical_section(self):
        self.send_request_messages_to_all_processes()

        self.list_of_requests.append([self.id, self.clock])

        while (len(self.list_of_responses) < self.number_of_other_processes) or self.list_of_requests[0][0] != self.id:

            print(f'P{self.id} ceka na odgovore')

            data, sender_process_id = self.receive_message()

            if data['type'] == 'request':

                print(f'P{self.id} primio Z({sender_process_id}, {data["clock"]}) od P{sender_process_id}')

                self.update_clock()

                self.list_of_responses.append([sender_process_id, data['clock']])

                if sender_process_id == 3:
                    self.send_message(sender_process_id, 'response')

            elif data['type'] == 'release':

                print(f'P{self.id} primio I({sender_process_id}, {data["clock"]}) od P{sender_process_id}')

                self.list_of_requests.remove([sender_process_id, data['clock']])

            else:

                print(f'P{self.id} primio O({sender_process_id}, {data["clock"]}) od P{sender_process_id}')

                self.update_clock()

        self.list_of_requests.pop(0)
        self.list_of_responses = []

        print(f'P{self.id} usao u kriticni odsjecak')

        time.sleep(3)

        self.need_to_crtical_section = False

        print(f'P{self.id} izasao iz kriticnog odsjecka')

        self.send_release_messages_to_all_processes()

    def work(self):
        while True:
            if any(self.clock >= time_to_critical_section for time_to_critical_section in
                   self.times_to_critical_section):
                self.need_to_crtical_section = True

            while self.need_to_crtical_section:
                self.critical_section()

            time.sleep(1)

            self.clock += 1

            data, sender_process_id = self.receive_message()

            if data['type'] == 'request':
                print(f'P{self.id} primio Z({sender_process_id}, {data["clock"]}) od P{sender_process_id}')

                self.update_clock()

                self.list_of_requests.append([sender_process_id, data['clock']])

                self.send_message(sender_process_id, 'response')
            elif data['type'] == 'release':
                print(f'P{self.id} primio I({sender_process_id}, {data["clock"]}) od P{sender_process_id}')

                self.list_of_requests.remove([sender_process_id, data['clock']])

    def join(self):
        self.process.join()

    def create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', 8000 + self.id)
        server_socket.bind(server_address)

        return server_socket

    def send_message(self, process, response_type):
        address = ('localhost', 8000 + process)

        response = {
            'type': response_type,
            'clock': self.clock
        }

        response = json.dumps(response)

        self.socket.sendto(response.encode(), address)

    def receive_message(self):
        data, address = self.socket.recvfrom(4096)

        data = json.loads(data.decode())

        _, port = address

        sender_process_id = port % 10

        return data, sender_process_id

    def send_request_messages_to_all_processes(self):
        for i in range(self.number_of_other_processes + 1):
            if (i + 1) != self.id:
                self.send_message(i + 1, 'request')
                print(f'P{self.id} poslao Z({self.id}, {self.clock}) k P{i + 1}')

    def send_release_messages_to_all_processes(self):
        for i in range(self.number_of_other_processes + 1):
            if (i + 1) != self.id:
                self.send_message(i + 1, 'release')
                print(f'P{self.id} poslao I({self.id}, {self.clock}) k P{i + 1}')

    def update_clock(self):
        self.clock += 1
        # print("Dogadaj " + self.id)
        print(f"T({self.id}) = {self.clock}")
